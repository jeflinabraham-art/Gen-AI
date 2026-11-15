import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from src.embeddings import get_embedding_model
from src.loaders import load_documents, split_documents

load_dotenv()

# Specifies where your FAISS database will be saved.
DEFAULT_VECTORSTORE_DIR = Path("data/vectorstore")

# Specifies where your uploaded PDF and DOCX files are stored.
DEFAULT_DOCUMENTS_DIR = Path("data/documents")

INDEX_NAME = "index"


def vectorstore_exists(persist_directory: str|Path   = DEFAULT_VECTORSTORE_DIR) -> bool:
    folder = Path(persist_directory)
    return (folder / f"{INDEX_NAME}.faiss").exists() and (folder / f"{INDEX_NAME}.pkl").exists()
    # FAISS uses two important pieces of information:
    #     index.faiss: It stores the numerical vector data and the search index.
    #     index.pkl: Stores the actual document data and mappings between vector IDs and documents.


# It performs the complete indexing process:
#     1. Loads documents.
#     2. Counts source files.
#     3. Splits documents into chunks.
#     4. Generates embeddings.
#     5. Creates a FAISS vector store.
#     6. Saves the vector store locally.
def build_vectorstore(
    documents_dir: str|Path   = DEFAULT_DOCUMENTS_DIR,
    persist_directory: str|Path   = DEFAULT_VECTORSTORE_DIR,
    chunk_size: int|None   = None,
    chunk_overlap: int|None   = None,
) -> tuple[FAISS, int, int]:
    
    selected_chunk_size = chunk_size or int(os.getenv("CHUNK_SIZE", "1000"))
    selected_chunk_overlap = chunk_overlap or int(os.getenv("CHUNK_OVERLAP", "150"))

    # 1) Load raw documents from disk.
    documents = load_documents(str(documents_dir))

    # Count unique source files.
    # Because one PDF can produce multiple Documents (one per page). We want to count original uploaded files, not extracted pages.
    unique_filenames = set()
    for doc in documents:
        filename = doc.metadata.get("filename")
        unique_filenames.add(filename)
    num_files = len(unique_filenames)

    # 2) Split into chunks before embedding.
    chunks = split_documents(
        documents,
        chunk_size=selected_chunk_size,
        chunk_overlap=selected_chunk_overlap,
    )

    # 3) Create embeddings and store them in FAISS.
    try:
        embeddings = get_embedding_model()

        # Behind the scenes, LangChain does the following:
        #     1. Extracts the text from each chunk.
        #     2. Sends the texts to the embedding model.
        #     3. Receives numerical vectors.
        #     4. Creates a FAISS index.
        #     5. Adds the vectors to the index.
        #     6. Stores the associated Documents and mappings.
        vectorstore = FAISS.from_documents(
            documents=chunks, 
            embedding=embeddings
        )

    # from exc: Preserves the original exception as the cause.
    except Exception as exc:
        raise RuntimeError(
            "Failed to create embeddings or build the FAISS index."
        ) from exc

    # 4) Persist the index so we can reload it later without rebuilding.
    persist_path = Path(persist_directory)

    # Creates the directory if it doesn't already exist.
    # parents=True: Create missing parent directories too.
    # exist_ok=True: Don't raise an error if the directory already exists
    persist_path.mkdir(parents=True, exist_ok=True)

    # This saves your FAISS vector store to the local filesystem.
    # Why save them?
    # By saving the index, you can load the existing knowledge base instead of rebuilding the FAISS index every time the application starts.
    vectorstore.save_local(str(persist_path), index_name=INDEX_NAME)

    return vectorstore, num_files, len(chunks)


# When your application starts again, you don't want to regenerate all embeddings. Instead, you want to load the saved database. That's exactly what load_vectorstore() does.
def load_vectorstore(persist_directory: str|Path   = DEFAULT_VECTORSTORE_DIR) -> FAISS:
    if not vectorstore_exists(persist_directory):
        raise FileNotFoundError(
            "No knowledge base found. Please build the knowledge base first."
        )

    try:
        # Initializes the same embedding model used when building the vector store. Why?
        # Because when a user searches, their query must be converted into vectors that are compatible with the stored document vectors. Using a different model or embedding dimension can make retrieval fail or produce invalid comparisons.
        embeddings = get_embedding_model()

        vectorstore = FAISS.load_local(
            str(persist_directory),
            embeddings,
            index_name=INDEX_NAME,

            # index.pkl → Stores document data and mappings.
            # The .pkl file uses Python's pickle format to save Python objects.
            # When loading the vector store, LangChain needs to deserialize (convert the saved data back into Python objects) the pickle file.
            # However, pickle files can contain malicious code that executes during deserialization.
            # Therefore, LangChain blocks this operation by default unless you explicitly allow it.
            allow_dangerous_deserialization=True,
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to load the FAISS knowledge base. Try rebuilding the knowledge base."
        ) from exc

    return vectorstore


# This function is used when you want to completely rebuild your knowledge base. 
# For example:
# - You removed some documents.
# - You uploaded updated policies.
# - You want to recreate the index from the current documents folder.
def rebuild_vectorstore(
    documents_dir: str|Path   = DEFAULT_DOCUMENTS_DIR,
    persist_directory: str|Path   = DEFAULT_VECTORSTORE_DIR,
) -> tuple[FAISS, int, int]:
    clear_vectorstore(persist_directory)
    return build_vectorstore(documents_dir, persist_directory)


# This function deletes the existing saved vector store.
def clear_vectorstore(persist_directory: str|Path   = DEFAULT_VECTORSTORE_DIR) -> None:
    folder = Path(persist_directory)
    if folder.exists():
        # shutil.rmtree() deletes a directory and everything inside it.
        shutil.rmtree(folder)
    # Creates the directory again.
    folder.mkdir(parents=True, exist_ok=True)


def get_retriever(vectorstore: FAISS, k: int|None   = None,) -> VectorStoreRetriever:
    top_k = k or int(os.getenv("TOP_K", "4"))

    # Convert the FAISS vector store into a retriever for similarity search.
    return vectorstore.as_retriever(search_kwargs={"k": top_k})


# This function returns the total number of vectors stored in your FAISS index.
def get_chunk_count(persist_directory: str|Path = DEFAULT_VECTORSTORE_DIR) -> int:
    if not vectorstore_exists(persist_directory):
        return 0

    try:
        vectorstore = load_vectorstore(persist_directory)
        # FAISS exposes the number of stored vectors through the index object.
        # In your application, each vector generally corresponds to one embedded chunk.
        return int(vectorstore.index.ntotal)
    except Exception:
        return 0


def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "No relevant context was retrieved."

    parts = []
    for i, doc in enumerate(docs, start=1):

        # loaders module standardized the metadata so that every Document has filename/page field.
        # For DOCX documents, page field is None.
        filename = doc.metadata.get("filename")
        page = doc.metadata.get("page")
        location = f"{filename}"
        if page is not None:
            location = f"{filename} (page {page})"
        parts.append(f"[Source {i}: {location}]\n{doc.page_content}")

    return "\n\n".join(parts)
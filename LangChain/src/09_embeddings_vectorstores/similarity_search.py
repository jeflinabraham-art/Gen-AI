from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.helpers import print_separator, print_title

load_dotenv()


def main() -> None:

    # The goal is to retrieve the most relevant information from similarity.txt based on a user's question.
    print_title("Similarity Search")

    # Specifies the location of your text file.
    file_path = PROJECT_ROOT / "data" / "input" / "similarity.txt"

    # Creates a loader object to read the file.
    loader = TextLoader(file_path)

    # Reads the file and returns a list of LangChain Document objects.
    # A Document contains page_content (actual text) and metadata (additional information about the document).
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )

    # split_documents(): Splits the loaded documents into smaller Document objects (chunks).
    chunks = splitter.split_documents(documents)

    # initializes Google's embedding model. Its job is to convert text into numerical vectors.
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    # FAISS is a library used to efficiently store and search numerical vectors based on similarity.
    # What does FAISS.from_documents() do?
    # It takes your document chunks and embedding model and performs the following operations:
    #     1. Extracts the text from each chunk.
    #     2. Sends the text to Gemini's embedding model.
    #     3. Receives numerical vectors for each chunk.
    #     4. Stores those vectors in a FAISS index.
    #     5. Keeps the associated document content and metadata available for retrieval.

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    query = "I am unable to access my account after entering the wrong password several times."

    print(f"User Query:\n{query}")

    print_separator()

    # similarity_search():
    # The query is converted into an embedding using the same embedding model.
    # FAISS compares the query vector with the vectors stored in its index.
    # It identifies the closest vectors.
    # It retrieves the corresponding document chunks.
    results = vector_store.similarity_search(
        query=query,
        k=3,
    )

    for index, document in enumerate(results, start=1):

        print(f"Retrieved Chunk {index}")

        print(document.page_content)

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# Similarity Search retrieves documents based on semantic meaning rather
# than exact keyword matches.
#
# The user's query is first converted into an embedding. The vector
# database then finds the document chunks whose embeddings are closest
# to the query embedding.
#
# This is the core retrieval mechanism used in almost every RAG system.
# =============================================================================
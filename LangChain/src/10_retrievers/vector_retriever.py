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
    print_title("Vector Store Retriever")

    file_path = PROJECT_ROOT / "data" / "input" / "similarity.txt"
    loader = TextLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )

    chunks = splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    # as_retriever(): Converts your FAISS vector store into a retriever.
    # You're configuring your retriever to return the top 2 matching chunks whenever someone asks a question.
    # A retriever is a component that takes a user query and returns relevant documents from a knowledge source. 
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )

    query = "Where is my package? It hasn't arrived yet."
    documents = retriever.invoke(query)

    print(f"Query:\n{query}")

    print_separator()


    for index, document in enumerate(documents, start=1):

        print(f"Retrieved Document {index}\n")

        print(document.page_content)

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# A Retriever sits on top of a vector database.
#
# Instead of manually performing similarity search, we simply provide a
# query and the retriever returns the most relevant documents.
#
# In most RAG applications, the retriever is responsible for fetching
# context before sending it to the LLM.
# =============================================================================
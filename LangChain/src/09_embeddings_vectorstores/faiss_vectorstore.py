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
    print_title("FAISS Vector Store")

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

    print(f"Documents Indexed : {len(chunks)}")

    print_separator()

    query = "I was charged without receiving an order confirmation."

    results = vector_store.similarity_search(
        query=query,
        k=2,
    )

    print(f"Query:\n{query}")

    print_separator()

    for index, document in enumerate(results, start=1):

        print(f"Result {index}\n")

        print(document.page_content)

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# FAISS is a high-performance vector database developed by Meta.
#
# It stores embeddings in memory and performs very fast similarity search,
# making it ideal for local RAG applications and experimentation.
#
# Unlike Chroma, FAISS focuses on fast vector search and does not provide
# built-in persistence or metadata management by default.
# =============================================================================
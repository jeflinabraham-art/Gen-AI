from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import (LLMChainExtractor,)
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm_client import get_llm
from utils.helpers import print_separator, print_title

load_dotenv()


def main() -> None:
    print_title("Contextual Compression Retriever")

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
        chunks,
        embeddings,
    )

    # base_retriever: The original retriever that searches the vector store and fetches relevant documents based on the user's query.
    base_retriever = vector_store.as_retriever()

    # compressorL: An LLM-powered component that examines the retrieved documents and extracts only the information relevant to the user's query.
    compressor = LLMChainExtractor.from_llm(
        get_llm()
    )

    # Combines the base retriever and compressor into one retriever.
    retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor,
    )
    # First retrieve documents, then compress them to keep only the information relevant to the user's question.


    query = "Why is my account locked?"
    documents = retriever.invoke(query)

    print(f"Query:\n{query}")

    print_separator()


    print(f"Retrieved {len(documents)} Compressed Documents\n")

    print_separator()

    for index, document in enumerate(documents, start=1):
        print(f"Document {index}\n")
        print(document.page_content)
        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# Contextual Compression retrieves documents first and then removes
# irrelevant information using an LLM.
#
# Instead of sending entire document chunks to the LLM, only the
# most relevant content is retained.
#
# This helps reduce token usage and improves answer quality.
# =============================================================================
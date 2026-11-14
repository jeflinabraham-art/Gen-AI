from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import WebBaseLoader

from utils.helpers import print_separator, print_title


def main() -> None:
    print_title("Web Loader")

    # WebBaseLoader()
    #     - WebBaseLoader is a LangChain document loader.
    #     - It loads content from web pages.
    #     - It uses the provided URLs to fetch the webpage content.
    loader = WebBaseLoader(

        # It accepts multiple URLs.
        web_paths=(
            "https://python.langchain.com/docs/introduction/",
        )
    )

    # loader.load()
        # Visits the provided webpage.
        # Fetches its HTML content.
        # Extracts the page content as text.
        # Converts it into a LangChain Document object
        # Returns a list of Document objects. (1 webpage = 1 document)
    documents = loader.load()

    print(f"Total Documents Loaded : {len(documents)}")

    print_separator()

    document = documents[0]

    print("Document Metadata:\n")
    print(document.metadata)

    print_separator()

    print("Document Content (First 1000 Characters):\n")
    print(document.page_content[:1000])


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# WebBaseLoader fetches content directly from web pages and converts
# it into LangChain Document objects.
#
# This is useful when building RAG applications over websites,
# documentation, blogs, or knowledge bases.
#
# After loading, the documents can be chunked, embedded, and stored
# in a vector database.
# =============================================================================
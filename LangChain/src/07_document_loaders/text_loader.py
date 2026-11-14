from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import TextLoader

from utils.helpers import print_separator, print_title


def main() -> None:
    print_title("Text Loader")

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    # TextLoader(): 
        # is a LangChain document loader.
        # It takes the file path as input.
        # It creates a loader object configured to read that file.
    # load():
        # Actually reads the file and returns its content as a list of Document objects (1 file = 1 document).
    loader = TextLoader(file_path)
    documents = loader.load()

    # The entire text file is loaded as ONE Document object.
    # documents → List containing one Document.
    # documents[0] → The entire text file.
    # documents[0].page_content → All the text inside the file.

    print(f"Total Documents Loaded : {len(documents)}")

    print_separator()

    document = documents[0]

    print("Document Metadata:\n")
    print(document.metadata)

    print_separator()

    print("Document Content:\n")
    print(document.page_content)


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# TextLoader reads plain text files and converts them into LangChain
# Document objects.
#
# Every loaded document contains:
#
# 1. page_content → Actual document text
# 2. metadata     → Additional information such as file path
#
# This is usually the first step in a RAG pipeline.
# =============================================================================
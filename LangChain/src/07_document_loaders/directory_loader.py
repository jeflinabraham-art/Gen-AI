
from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

from utils.helpers import print_separator, print_title


def main() -> None:

    print_title("Directory Loader")

    directory = PROJECT_ROOT / "data" / "input"

    # Instead of loading one specific file, it loads multiple files from a directory (folder).
    loader = DirectoryLoader(

        # Specifies which directory to search for files.
        path=directory,

        # Specifies which files to select. 
        # *.txt means all .txt files in the current directory
        glob="*.txt",

        # This tells DirectoryLoader which loader to use for each matching file.
        # Here, you're saying: "For every .txt file you find, use TextLoader to read it."
        loader_cls=TextLoader,
    )

    # 1. Searches the specified directory.
    # 2. Finds files matching *.txt.
    # 3. Passes each file to TextLoader.
    # 4. Loads their contents.
    # 5. Combines the resulting Document objects into one list.
    documents = loader.load()

    print(f"Total Documents Loaded : {len(documents)}")

    print_separator()

    for index, document in enumerate(documents, start=1):

        print(f"Document {index}")

        print(f"Source : {document.metadata['source']}")

        print()

        print(document.page_content[:200])

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# DirectoryLoader automatically loads multiple files from a folder.
#
# Instead of loading one document at a time, it scans the directory,
# finds matching files, and converts each into a LangChain Document.
#
# This is commonly used when building RAG systems over hundreds or
# thousands of documents.
# ===========================================================================
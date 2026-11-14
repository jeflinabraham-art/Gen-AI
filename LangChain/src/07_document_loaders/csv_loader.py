from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import CSVLoader

from utils.helpers import print_separator, print_title


def main() -> None:
    print_title("CSV Loader")

    file_path = PROJECT_ROOT / "data" / "input" / "employees.csv"


    # CSVLoader(file_path)
    #     - CSVLoader is a LangChain document loader.
    #     - It takes the CSV file path as input.
    #     - It creates a loader object configured to read the CSV file.
    loader = CSVLoader(file_path)

    # loader.load()
    #     - Reads the CSV file.
    #     - Converts its rows into LangChain Document objects (1 row = 1 document).
    #     - Returns a list of Document objects.
    documents = loader.load()

    print(f"Total Rows Loaded : {len(documents)}")

    print_separator()

    first_row = documents[0]

    print("Row Metadata:\n")
    print(first_row.metadata)

    print_separator()

    print("Row Content:\n")
    print(first_row.page_content)


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# CSVLoader reads CSV files and converts every row into a LangChain
# Document object.
#
# Each row becomes an independent document containing:
#
# 1. page_content → Row values
# 2. metadata     → Source file and row number
#
# This is useful when building RAG systems over structured tabular data.
# =============================================================================
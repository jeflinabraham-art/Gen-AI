from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_text_splitters import MarkdownHeaderTextSplitter

from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates MarkdownHeaderTextSplitter."""

    print_title("Markdown Header Text Splitter")

    file_path = PROJECT_ROOT / "data" / "input" / "langchain_notes.md"


    # Why are we using open() instead of a LangChain loader?
    # Because MarkdownHeaderTextSplitter accepts plain text as input, rather than a list of Document objects.
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    # This is a LangChain text splitter designed specifically for Markdown files. It splits the text according to Markdown headings.
    splitter = MarkdownHeaderTextSplitter(

        # This argument specifies which Markdown heading levels should be used for splitting.
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
    )

    documents = splitter.split_text(markdown_text)

    print(f"Chunks Created : {len(documents)}")

    print_separator()

    for index, document in enumerate(documents, start=1):

        print(f"Chunk {index}")

        print("\nMetadata:")
        print(document.metadata)

        print("\nContent:")
        print(document.page_content)

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# MarkdownHeaderTextSplitter creates chunks based on Markdown headings.
#
# Instead of splitting text purely by size, it preserves the document
# hierarchy such as sections and sub-sections.
#
# This is especially useful when working with technical documentation,
# README files, knowledge bases, and project documentation.
# ============================================================================
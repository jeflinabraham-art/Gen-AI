from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates RecursiveCharacterTextSplitter."""

    print_title("Recursive Character Text Splitter")

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    loader = TextLoader(file_path)
    documents = loader.load()

    print(f"Original Documents : {len(documents)}")

    print_separator()

    # RecursiveCharacterTextSplitter:
        # This is a LangChain text splitter.
        # Its responsibility is to divide large documents into smaller chunks.
        # It uses a hierarchical approach, trying different separators to find suitable splitting points.
        # By default, it tries separators in this order: ["\n\n", "\n", " ", ""]
            # Meaning:
                # 1. First, try splitting at paragraph boundaries.
                # 2. If chunks are still too large, try line boundaries.
                # 3. If necessary, try spaces between words.
                # 4. Finally, split at individual characters if needed.
        # It tries to preserve meaningful text boundaries instead of blindly cutting text.
    splitter = RecursiveCharacterTextSplitter(

        # Specifies the maximum target size of each chunk.
        chunk_size=200,

        # It specifies how much text should overlap between consecutive chunks. This helps preserve context when information is split across chunk boundaries.
        chunk_overlap=50,
    )

    # Takes the list of Document objects returned by your document loader.
    # Extracts their text content.
    # Splits the text into smaller chunks.
    # returns a list of smaller Document objects.
    chunks = splitter.split_documents(documents)

    print(f"Chunks Created : {len(chunks)}")

    print_separator()

    for index, chunk in enumerate(chunks, start=1):

        print(f"Chunk {index}")
        print(f"Characters : {len(chunk.page_content)}")
        print()
        print(chunk.page_content)

        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RecursiveCharacterTextSplitter is the most commonly used text splitter
# in LangChain because it tries to preserve the meaning of the text.
#
# Instead of splitting strictly by characters, it first tries to split
# using paragraphs, then lines, then spaces, and finally individual
# characters if necessary.
#
# It is the default choice for most RAG applications.
# ===========================================================================
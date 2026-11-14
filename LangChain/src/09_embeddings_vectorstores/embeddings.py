from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from utils.helpers import print_separator, print_title

load_dotenv()


def main() -> None:
    print_title("Text Embeddings")

    text = "I am unable to access my account after entering the wrong password several times."

    # Initialize the embedding model. Its job is to convert text into numerical vectors.
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    # embed_query() converts a text into a numerical vector.
    # The returned vector represents the semantic meaning of the input text.
    # Similar meanings generally produce vectors that are close together.
    # These vectors are used for similarity search in vector databases.
    vector = embeddings.embed_query(text)

    print("Input Text:\n")
    print(text)

    print_separator()

    print(f"Embedding Dimension : {len(vector)}")

    print_separator()

    print("First 10 Vector Values:\n")
    print(vector[:10])


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# Embeddings convert text into numerical vectors.
#
# Texts with similar meanings produce vectors that are close together
# in the embedding space.
#
# These vectors are later stored inside vector databases and used for
# semantic search in RAG applications.
# =============================================================================
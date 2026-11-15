import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    api_key = os.getenv("GEMINI_API_KEY").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    selected_model = os.getenv(
        "EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL
    )

    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=selected_model,
            api_key=api_key,
        )
    except Exception as exc:
        raise RuntimeError(
            "Failed to create the google embedding client. Check GEMINI_API_KEY and EMBEDDING_MODEL in your .env file."
        ) from exc

    return embeddings


def get_embedding_model_name() -> str:
    return os.getenv("EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def create_llm():
    # Load environment variables from the .env file.
    load_dotenv()

    # Read the API key from the environment.
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing from the .env file.")

    # Read the model name; use gpt-4o-mini if not configured.
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Create and return the configured LLM.
    return ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=api_key
    )
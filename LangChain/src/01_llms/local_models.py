"""
File: local_models.py

Description
-----------
Demonstrates how to work with locally hosted LLMs (such as Ollama)
using LangChain instead of cloud-based APIs.

Before running this script:

1. Install Ollama
2. Pull a model (example: llama3.2)
       ollama pull llama3.2
3. Start the Ollama server
       ollama serve

This example intentionally creates the model locally instead of using
the shared llm_client.py because local models typically don't require
API keys or cloud provider configuration.
"""

from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]

# Add the root directory to Python's search path
sys.path.insert(0, str(project_root))

from llm_client import get_llm
from utils.helpers import print_title, get_response_content
from langchain_ollama import ChatOllama

def main() -> None:
    llm = ChatOllama(
        model="mistral",
        temperature=0.7,
    )

    prompt = "Explain LangChain in exactly three concise bullet points."

    response = llm.invoke(prompt)

    print_title("Local Model Response")

    get_response_content(response)

if __name__ == "__main__":
    main()

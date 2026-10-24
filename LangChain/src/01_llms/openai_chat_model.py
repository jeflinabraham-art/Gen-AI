"""
File: gemini_chat_model.py

Description
-----------
Demonstrates how to interact with Open AI chat models using LangChain.

In this project, the model is NOT created directly inside this file. Instead, we reuse the centralized LLM client defined in `llm_client.py`.

To run this example:

1. Open config.json
2. Change the provider to "openai"
3. Ensure your OpenAi API key is configured in the .env file
4. Run this script

Notice that the application code remains unchanged. Only the configured provider changes, which highlights one of LangChain's biggest strengths: 
a unified interface across multiple LLM providers.
"""

from pathlib import Path
import sys

project_root = Path(__file__).resolve().parents[2]

# Add the root directory to Python's search path
sys.path.insert(0, str(project_root))

from llm_client import get_llm
from utils.helpers import print_title, get_response_content


def main() -> None:
    llm = get_llm()

    prompt = "Explain LangChain in exactly three concise bullet points."

    response = llm.invoke(prompt)

    print_title("OpenAi Response")

    get_response_content(response)

if __name__ == "__main__":
    main()
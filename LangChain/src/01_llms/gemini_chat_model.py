"""
Description
-----------
Demonstrates how to interact with Google's Gemini chat models using LangChain.

In this project, the model is NOT created directly inside this file.
Instead, we reuse the centralized LLM client defined in `llm_client.py`.

To run this example:

1. Open config.json
2. Change the provider to "gemini"
3. Ensure your Gemini API key is configured in the .env file
4. Run this script

Notice that the application code remains unchanged. Only the configured
provider changes, which highlights one of LangChain's biggest strengths:
a unified interface across multiple LLM providers.
"""

from pathlib import Path
import sys

# Python searches the script's directory for imports, not automatically the project root. So we need to Locate the project root.

# __file__: The path of the Python file currently being executed.
# .resolve(): Converts the path into an absolute path. (eg: C:\Users\ASUS\UpSkill\GEN AI\LangChain\src\01_llms\openai_chat_model.py)
# Think of .parents as walking up your directory tree.
project_root = Path(__file__).resolve().parents[2]

# Add the root directory to Python's search path
sys.path.insert(0, str(project_root))

from llm_client import get_llm

from utils.helpers import print_title, get_response_content


def main() -> None:
    llm = get_llm()

    prompt = "Explain LangChain in exactly three concise bullet points."

    response = llm.invoke(prompt)

    print_title("Gemini Response")

    get_response_content(response)


# if __name__ == "__main__": ensures main() runs only when the Python file is executed directly, not when it is imported into another file.
if __name__ == "__main__":
    main()
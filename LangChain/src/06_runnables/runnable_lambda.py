"""
Description
-----------
Demonstrates RunnableLambda.

RunnableLambda allows us to convert an ordinary Python function into a LangChain Runnable.

Why is this useful? Because we can use our own Python logic inside LangChain workflows and combine it with prompts, LLMs, output parsers, and other Runnables.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add project root
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.runnables import RunnableLambda

from utils.helpers import print_separator, print_title

# This is just a normal Python function. LangChain doesn't treat it as a Runnable yet.
def to_uppercase(text: str) -> str:
    return text.upper()


def count_words(text: str) -> str:
    return f"Total Words: {len(text.split())}"


def main() -> None:

    print_title("Runnable Lambda")

    # Now LangChain can execute this function using .invoke():
    uppercase = RunnableLambda(to_uppercase)
    word_counter = RunnableLambda(count_words)

    text = "LangChain makes it easy to build LLM applications."

    print("Original Text:\n")
    print(text)

    print_separator()

    print("Uppercase:\n")
    print(uppercase.invoke(text))

    print_separator()

    print("Word Count:\n")
    print(word_counter.invoke(text))


if __name__ == "__main__":
    main()

"""
File: partial_prompt.py

Description
-----------
Demonstrates Partial Prompt Templates.

A Partial PromptTemplate allows us to pre-fill one or more variables while
keeping the remaining variables dynamic. This is useful when certain parts
of a prompt remain constant across multiple LLM calls.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate

from llm_client import get_llm
from utils.helpers import print_separator, print_title, get_response_content


def main() -> None:
    """Demonstrates Partial PromptTemplate."""

    print_title("Partial PromptTemplate")

    llm = get_llm()

    tutor_template = PromptTemplate(
        template="""
            You are an expert {domain} trainer.

            Explain the concept of {topic}.

            Keep the explanation under {word_limit} words.
            """,
        input_variables=["domain", "topic", "word_limit"],
    )

    # Pre-fill the domain once.
    tutor_partial_prompt = tutor_template.partial(domain="Generative AI", word_limit = 100)

    # Only the remaining variables are required. 
    # student1
    prompt1 = tutor_partial_prompt.invoke(
        {
            "topic": "Vector Embeddings",
        }
    )
    # student2
    prompt2 = tutor_partial_prompt.invoke(
        {
            "topic": "RAG",
        }
    )
    # student3
    prompt3 = tutor_partial_prompt.invoke(
        {
            "topic": "LLMs",
        }
    )

    print("Formatted Prompt:\n")
    print(prompt1.text)

    print_separator()

    response = llm.invoke(prompt1)

    print("LLM Response:\n")
    get_response_content(response)


if __name__ == "__main__":
    main()
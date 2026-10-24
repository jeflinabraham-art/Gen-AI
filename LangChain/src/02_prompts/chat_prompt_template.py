"""
File: chat_prompt_template.py

Description
-----------
Demonstrates how to use ChatPromptTemplate for chat-based language models.

Unlike PromptTemplate, ChatPromptTemplate allows us to structure prompts
using different message roles such as System, Human, and AI.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import ChatPromptTemplate

from llm_client import get_llm
from utils.helpers import print_separator, print_title, get_response_content


def main() -> None:
    """Demonstrates ChatPromptTemplate."""

    print_title("ChatPromptTemplate")

    llm = get_llm()

    chat_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an experienced {profession}. "
            "Explain technical concepts simply, using examples/ analogy."
        ),
        (
            "human",
            "What is an API?"
        ),
        (
            "ai",
            "An API is like a waiter in a restaurant. "
            "It carries requests between you and the kitchen."
        ),
        (
            "human",
            "Now explain {topic} in less than {word_limit} words."
        ),
    ])

    messages = chat_prompt.invoke({
        "profession": "AI Engineer",
        "topic": "Vector Databases",
        "word_limit": 100,
    })

    print("\nFormatted Messages:\n")
    for message in messages.messages:
        print(f"{message.type.upper()}: {message.content}\n")

    print_separator()

    response = llm.invoke(messages)

    print("LLM Response:\n")
    get_response_content(response)


if __name__ == "__main__":
    main()
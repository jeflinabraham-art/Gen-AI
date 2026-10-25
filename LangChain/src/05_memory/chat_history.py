"""
Description
-----------
Demonstrates how chat messages are stored using ChatMessageHistory.

ChatMessageHistory is the foundation for conversational AI applications.
It stores all messages exchanged between the user and the AI.
"""

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if(str(PROJECT_ROOT) not in sys.path):
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.helpers import print_title, print_separator

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

def main() -> None:
    print_title("Chat Message History")

    # InMemoryChatMessageHistory is a LangChain class that manages a sequence of chat messages.
    # InMemory means the history is held in your program's memory (RAM).
    chat_history = InMemoryChatMessageHistory()

    # Simulate a conversation
    chat_history.add_message(
        HumanMessage(content="What is LangChain?")
    )

    chat_history.add_message(
        AIMessage(
            content="LangChain is a framework for building LLM-powered applications."
        )
    )

    chat_history.add_message(
        HumanMessage(content="What are Prompt Templates?")
    )

    chat_history.add_message(
        AIMessage(
            content="Prompt Templates help create reusable prompts with dynamic variables."
        )
    )

    print("Conversation History:\n")

    for index, message in enumerate(chat_history.messages, start=1):
        print(f"Message {index}")
        print(f"Type    : {message.type}")
        print(f"Content : {message.content}")
        print_separator()

if __name__ == "__main__":
    main()
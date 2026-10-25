"""
Description
-----------
Demonstrates ConversationBufferMemory.

ConversationBufferMemory stores the complete conversation history.
Every user message and AI response is retained and provided as context
for future interactions.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_classic.memory import ConversationBufferMemory

from utils.helpers import print_separator, print_title

def main() -> None:

    print_title("Conversation Buffer Memory")

    # ConversationBufferMemory: a legacy LangChain class for storing the conversation history.
    # return_messages=True: tells the memory to return history as LangChain message objects, such as HumanMessage and AIMessage.
    memory = ConversationBufferMemory(
        return_messages=True
    )

    # Simulate a conversation

    # The save_context() method add the corresponding human and AI messages to the history.
    memory.save_context(
        {"input": "Hey! I'm a software engineer and I want to learn GenAI."},
        {"output": "That's awesome! Since you're a software engineer, you already have a great foundation. Have you explored LLMs yet?"}
    )

    memory.save_context(
        {"input": "Yes, I've learned the basics of LLMs and prompt engineering."},
        {"output": "Great start! Your next steps could be RAG, LangChain, and AI agents. These will help you build practical GenAI applications."}
    )

    memory.save_context(
        {"input": "I want to build a chatbot that can answer questions from my PDF notes."},
        {"output": "That's a perfect project for RAG! You can extract text from your PDFs, split it into chunks, create embeddings, retrieve relevant chunks, and pass them to an LLM to generate answers."}
    )

    memory.save_context(
        {"input": "Sounds good! Should I learn LangChain before starting the project?"},
        {"output": "Yes, learning the basics of LangChain first will help. Focus on prompt templates, models, output parsers, chains, and memory. Then you can bring these components together in your RAG chatbot."}
    )

    memory.save_context(
        {"input": "Thanks! Can you remind me what project I wanted to build?"},
        {"output": "Of course! You wanted to build a RAG chatbot that answers questions based on your PDF notes. It's a great way to put your GenAI knowledge into practice."}
    )

    print("Complete Conversation History:\n")

    # load_memory_variables() retrieves the information stored in memory and returns it in a dictionary.
    history = memory.load_memory_variables({})
    # print(history)

    for index, message in enumerate(history["history"], start=1):
        print(f"Message {index}")
        print(f"Type    : {message.type}")
        print(f"Content : {message.content}")
        print_separator()


if __name__ == "__main__":
    main()


# =============================================================================
# ChatMessageHistory vs ConversationBufferMemory
#
# ChatMessageHistory:
# -------------------
# - Simply stores conversation messages (Human, AI, System, etc.).
# - Think of it as a list or notebook of chat messages.
# - You manually add, retrieve, and manage the messages.
#
# ConversationBufferMemory:
# -------------------------
# - A memory implementation built on top of ChatMessageHistory.
# - Automatically stores user inputs and AI responses.
# - Provides the complete conversation history whenever the LLM needs context.
# - Commonly used in conversational AI applications and chatbots.
#
# In short:
# ChatMessageHistory = Message Storage
# ConversationBufferMemory = Memory Manager
# ============================================================================= 
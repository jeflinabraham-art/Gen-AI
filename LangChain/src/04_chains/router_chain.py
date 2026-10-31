
"""
File: router_chain.py

Description
-----------
Demonstrates a Router Chain using LCEL.

Routes a user's technical question to the
appropriate specialized chain.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main():
    llm = get_llm()

    # --------------------------------------------------
    # Step 1: Create specialized chains
    # --------------------------------------------------

    java_chain = (
        PromptTemplate.from_template(
            """
            You are a Java and Spring Boot expert.

            Explain the following question in a beginner-friendly
            way.

            Question: {query}
            """
        )
        | llm
        | StrOutputParser()
    )

    python_chain = (
        PromptTemplate.from_template(
            """
            You are a Python programming expert.

            Explain the following question in a beginner-friendly
            way.

            Question: {query}
            """
        )
        | llm
        | StrOutputParser()
    )

    genai_chain = (
        PromptTemplate.from_template(
            """
            You are a Generative AI and LangChain expert.

            Explain the following question in a beginner-friendly
            way.

            Question: {query}
            """
        )
        | llm
        | StrOutputParser()
    )

    general_chain = (
        PromptTemplate.from_template(
            """
            You are a helpful general-purpose assistant.

            Answer the following question clearly and simply.

            Question: {query}
            """
        )
        | llm
        | StrOutputParser()
    )

    # --------------------------------------------------
    # Step 2: Define routing logic
    # --------------------------------------------------

    def route(info: dict):

        query = info["query"].lower()

        # Java / Spring Boot routing
        keywords = ["java", "spring", "spring boot", "jpa", "hibernate"]
        for word in keywords:
            if word in query:
                print("Routing to: Java/Spring Boot Chain\n")
                return java_chain

        # Python routing
        keywords = ["python", "decorator", "list comprehension", "pandas"]
        for word in keywords:
            if word in query:
                print("Routing to: Python Chain\n")
                return python_chain

        # GenAI routing
        keywords = ["llm", "rag", "langchain", "embedding", "vector database", "generative ai"]
        for word in keywords:
            if word in query:
                print("Routing to: GenAI Chain\n")
                return genai_chain

        # Default routing
        print("Routing to: General Chain\n")
        return general_chain

    query = input("You: ")
    print_separator()

    selected_chain = route({"query": query})

    response = selected_chain.invoke({"query": query})

    print("AI Response:\n")
    print(response)

    

    print_separator()


if __name__ == "__main__":
    main()

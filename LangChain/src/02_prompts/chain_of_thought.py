"""
File: chain_of_thought.py

Description
-----------
Demonstrates Chain-of-Thought Prompting.

Chain-of-Thought (CoT) prompting encourages the model to reason through
a problem step by step before arriving at the final answer.

Note:
Some modern reasoning models may internally reason even without explicit
Chain-of-Thought prompting. This example is for educational purposes to
illustrate the prompting technique.
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
    print_title("Chain-of-Thought Prompting")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a careful math tutor.

                Solve problems systematically.
                Break the solution into clear calculation steps.
                Check the calculations before giving the final answer.

                Present a concise explanation of the method,
                followed by the final answer.
                """,
            ),
            (
                "human",
                """
                Solve this problem:

                A company has 120 employees.

                - 40% of employees work in the engineering department.
                - Of the engineering employees, 25% are working remotely.
                - The company gives each remote engineering employee
                  a $150 equipment allowance.

                Calculate the total equipment allowance paid
                to remote engineering employees.

                Show the calculation steps and the final answer.
                """,
            ),
        ]
    )

    messages = prompt.invoke({})

    print("Formatted Prompt:\n")

    for message in messages.messages:
        print(f"{message.type.upper()}:")
        print(message.content)
        print()

    print_separator()

    response = llm.invoke(messages)

    print("LLM Response:\n")
    get_response_content(response)


if __name__ == "__main__":
    main()
"""
Description
-----------
Demonstrates a Parallel Chain using LCEL.

Unlike a Sequential Chain, multiple independent tasks execute
simultaneously on the same input, making workflows faster and more
efficient.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0,str(PROJECT_ROOT))

from llm_client import get_llm

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

from utils.helpers import print_title, print_separator

def main() -> None:
    print_title("Parallel Chain")

    llm = get_llm()

    summary_prompt = PromptTemplate.from_template(
        "Write a short summary about {topic}."
    )

    advantages_prompt = PromptTemplate.from_template(
        "List three advantages of {topic}."
    )

    applications_prompt = PromptTemplate.from_template(
        "List three real-world applications of {topic}."
    )

    parallel_chain = RunnableParallel(
        summary=summary_prompt | llm | StrOutputParser(),
        advantages=advantages_prompt | llm | StrOutputParser(),
        applications=applications_prompt | llm | StrOutputParser(),
    )

    topic = "Retrieval-Augmented Generation (RAG)"

    print(f"Topic:\n{topic}")

    print_separator()

    # result is a Python dictionary. You can access each value using its key. The keys are the names you assigned inside RunnableParallel.
    result = parallel_chain.invoke({"topic": topic})

    print("Summary:\n")
    print(result["summary"])

    print_separator()

    print("Advantages:\n")
    print(result["advantages"])

    print_separator()

    print("Applications:\n")
    print(result["applications"])

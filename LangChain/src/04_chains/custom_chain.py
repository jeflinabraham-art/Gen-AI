from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main():

    print_title("Interview Preparation Workflow")

    llm = get_llm()

    # Step 1: Generate an interview question
    question_chain = (
        PromptTemplate.from_template(
            """
            Generate one important technical interview question
            for a {role}.

            Focus on a commonly asked interview topic.
            Return only the question.
            """
        )
        | llm
        | StrOutputParser()
    )

    # Step 2: Explain the concepts needed to answer
    explanation_chain = (
        PromptTemplate.from_template(
            """
            Explain the concepts required to answer this interview question.

            Question:
            {question}

            explain in very simple terms and keep 1 or 2 sentences.
            """
        )
        | llm
        | StrOutputParser()
    )

    # Step 3: Generate a sample interview answer
    answer_chain = (
        PromptTemplate.from_template(
            """
            Write a good technical interview answer for this question.

            Question:
            {question}

            Use the following explanation as reference:
            {explanation}

            Keep the answer clear and suitable for an interview.
            """
        )
        | llm
        | StrOutputParser()
    )

    # Step 4: Generate short revision notes
    revision_chain = (
        PromptTemplate.from_template(
            """
            Create five short revision points based on this interview question
            and its answer.

            Question:
            {question}

            Answer:
            {answer}
            """
        )
        | llm
        | StrOutputParser()
    )

    # Custom workflow
    def interview_workflow(info: dict) -> dict:

        role = info["role"]

        # Generate question
        question = question_chain.invoke({
            "role": role
        })

        # Explain concepts
        explanation = explanation_chain.invoke({
            "question": question
        })

        # Generate sample answer
        answer = answer_chain.invoke({
            "question": question,
            "explanation": explanation
        })

        # Generate revision notes
        revision = revision_chain.invoke({
            "question": question,
            "answer": answer
        })

        return {
            "question": question,
            "explanation": explanation,
            "answer": answer,
            "revision": revision
        }

    # Convert Python function into a LangChain Runnable
    custom_chain = RunnableLambda(interview_workflow)

    # Input
    role = "Java Spring Boot Developer"

    result = custom_chain.invoke({
        "role": role
    })

    print("Interview Question:\n")
    print(result["question"])

    print_separator()

    print("Concept Explanation:\n")
    print(result["explanation"])

    print_separator()

    print("Sample Interview Answer:\n")
    print(result["answer"])

    print_separator()

    print("Revision Notes:\n")
    print(result["revision"])


if __name__ == "__main__":
    main()

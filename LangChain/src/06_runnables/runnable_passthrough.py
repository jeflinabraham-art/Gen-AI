
"""
Description
-----------
Demonstrates RunnablePassthrough.

Use case:
AI Interview Preparation Assistant.

The candidate provides their role and experience.
The workflow preserves the original candidate details
and generates an interview question.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main() -> None:

    print_title("Runnable Passthrough - Interview Preparation")

    llm = get_llm()

    # --------------------------------------------------------------
    # Step 1: Create an interview question generation chain
    # --------------------------------------------------------------

    question_chain = (
        PromptTemplate.from_template(
            """
            Generate one technical interview question for a candidate.

            Job Role: {role}
            Experience: {experience}

            Generate a question suitable for this candidate's experience level.
            Return only the question.
"""
        )
        | llm
        | StrOutputParser()
    )

    # --------------------------------------------------------------
    # Step 2: Prepare candidate details
    # --------------------------------------------------------------

    candidate = {
        "name": "Jeflin",
        "role": "Java Spring Boot Developer",
        "experience": "1 year"
    }

    print("Candidate Details:\n")
    print(candidate)

    print_separator()

    # --------------------------------------------------------------
    # Step 3: Preserve original input and generate a question
    # --------------------------------------------------------------

    pipeline = RunnableParallel(
        candidate_details=RunnablePassthrough(),
        interview_question=question_chain
    )

    '''
    {
        "candidate_details": {
            "name": "Jeflin",
            "role": "Java Spring Boot Developer",
            "experience": "1 year"
        },
        "interview_question": "..."
    }
    '''
    result = pipeline.invoke(candidate)

    # --------------------------------------------------------------
    # Step 4: Display results
    # --------------------------------------------------------------

    print("Original Candidate Details:\n")
    print(result["candidate_details"])

    print_separator()

    print("Generated Interview Question:\n")
    print(result["interview_question"])

    print_separator()

    # --------------------------------------------------------------
    # Step 5: Add generated output to original input
    # Using RunnablePassthrough.assign()
    # --------------------------------------------------------------

    '''
    approach 2:

    the original fields are preserved at the top level, and the generated question is added to the same dictionary.

    {
        "name": "Jeflin",
        "role": "Java Spring Boot Developer",
        "experience": "1 year",
        "interview_question": "..."
    }
    '''
    enhanced_pipeline = RunnablePassthrough.assign(
        interview_question=question_chain
    )

    enhanced_result = enhanced_pipeline.invoke(candidate)

    print("Enhanced Candidate Details:\n")
    print(enhanced_result)


if __name__ == "__main__":
    main()


# =============================================================================
# CONCEPT SUMMARY
#
# RunnablePassthrough()
#     Passes the original input without modifying it.
#
# RunnableParallel()
#     Sends the same input to multiple branches and combines their outputs.
#
# RunnablePassthrough.assign()
#     Preserves the original dictionary and adds new output fields.
#
# Example:
#
# Original Input:
# {
#     "name": "Jeflin",
#     "role": "Java Spring Boot Developer",
#     "experience": "1 year"
# }
#
# Enhanced Output:
# {
#     "name": "Jeflin",
#     "role": "Java Spring Boot Developer",
#     "experience": "1 year",
#     "interview_question": "Explain dependency injection..."
# }
#
# =============================================================================

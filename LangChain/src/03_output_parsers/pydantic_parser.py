"""
Description
-----------
Demonstrates how to use PydanticOutputParser to parse and validate
LLM responses against a predefined schema.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from llm_client import get_llm
from utils.helpers import print_separator, print_title, get_response_content


# You're creating a class named Employee that inherits from Pydantic's BaseModel.
class Employee(BaseModel):
    """Schema representing employee information."""

    name: str = Field(description="Employee's full name")
    department: str = Field(description="Department name")
    experience: int = Field(description="Years of experience")
    skills: list[str] = Field(description="List of technical skills")


def main() -> None:

    print_title("Pydantic Output Parser")

    llm = get_llm()

    # This creates a parser that uses your Employee class.
    # Think of it as: When I give you an LLM response to parse, expect employee data with the fields defined in Employee.
    parser = PydanticOutputParser(pydantic_object=Employee)

    prompt = PromptTemplate(
        template="""
            Extract the employee information.

            {format_instructions}

            Text:
            {employee_details}
            """,
        input_variables=["employee_details"],
        partial_variables={
            # parser.get_format_instructions(): It generates instructions describing the output format expected by the parser.
            "format_instructions": parser.get_format_instructions()
        },
    )

    prompt_value = prompt.invoke(
        {
            "employee_details": (
                "Rahul Sharma works as a Data Scientist in the AI team. He has 5 years of experience and is skilled in Python, Machine Learning, SQL and LangChain."
            )
        }
    )

    print("Formatted Prompt:\n")
    print(prompt_value.text)

    print_separator()

    response = llm.invoke(prompt_value)

    print("Raw LLM Response:\n")
    get_response_content(response)

    print_separator()

    # The parser receives the LLM response and attempts to:
    #     1. Extract the generated text from the response.
    #     2. Parse the JSON.
    #     3. Validate the data against the Employee model.
    #     4. Create an Employee object if parsing and validation succeed.
    parsed_response = parser.invoke(response)

    print("Parsed Pydantic Object:\n")
    print(parsed_response)

    print_separator()

    print("Accessing Individual Fields:\n")

    print(f"Name       : {parsed_response.name}")
    print(f"Department : {parsed_response.department}")
    print(f"Experience : {parsed_response.experience}")
    print(f"Skills     : {parsed_response.skills}")


if __name__ == "__main__":
    main()
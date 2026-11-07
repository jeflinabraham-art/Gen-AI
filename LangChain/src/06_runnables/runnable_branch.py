
"""
Description
-----------
Demonstrates RunnableBranch.

RunnableBranch selects and executes a particular chain based
on conditions evaluated against the input.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add project root
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main() -> None:

    print_title("Customer Support - Runnable Branch")

    llm = get_llm()

    # Step 1: Create individual chains
    order_chain = (
        PromptTemplate.from_template(
            """
            You are an e-commerce order support assistant.

            Help the customer with their order-related issue.

            Customer query:
            {query}

            Provide a clear and helpful response.
            """
        )
        | llm
        | StrOutputParser()
    )

    payment_chain = (
        PromptTemplate.from_template(
            """
            You are an e-commerce payment support assistant.

            Help the customer with their payment-related issue.

            Customer query:
            {query}

            Provide a clear and helpful response.
            """
        )
        | llm
        | StrOutputParser()
    )

    general_chain = (
        PromptTemplate.from_template(
            """
            You are a friendly e-commerce customer support assistant.

            Answer the customer's general query.

            Customer query:
            {query}

            Provide a clear and helpful response.
            """
        )
        | llm
        | StrOutputParser()
    )

    # ---------------------------------------------------------------
    # Step 2: Define conditions
    # ---------------------------------------------------------------

    def is_order_query(info: dict):
        query = info["query"].lower()

        keywords = ["order", "delivery", "tracking", "shipment", "delayed"]
        for word in keywords:
            if word in query:
                return True
        return False

    def is_payment_query(info):
        query = info["query"].lower()

        keywords = ["payment", "refund", "transaction", "deducted", "charged"]
        for word in keywords:
            if word in query:
                return True
        return False

    # ---------------------------------------------------------------
    # Step 3: Create RunnableBranch
    # ---------------------------------------------------------------

    # RunnableBranch executes only the first matching chain. With RunnableBranch, you don't need to manually return a chain and then invoke it separately. The selected chain is executed automatically.
    branch = RunnableBranch(
        (is_order_query, order_chain),
        (is_payment_query, payment_chain),
        general_chain
    )

    # ---------------------------------------------------------------
    # Step 4: Execute
    # ---------------------------------------------------------------

    query = "My payment was deducted but my order wasn't placed."

    print("Customer Query:\n")
    print(query)

    print_separator()

    response = branch.invoke({
        "query": query
    })

    print("Support Response:\n")
    print(response)


if __name__ == "__main__":
    main()


# =============================================================================
# CONCEPT SUMMARY
#
# RunnableBranch evaluates conditions in the order they are provided.
#
# If the first condition is True:
#     Execute the first chain.
#
# Else if the second condition is True:
#     Execute the second chain.
#
# If none of the conditions are True:
#     Execute the default chain.
#
# =============================================================================

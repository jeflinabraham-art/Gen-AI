# StrOutputParser extracts the text content from an LLM response.
from langchain_core.output_parsers import StrOutputParser

# ChatPromptTemplate allows you to create a reusable prompt with placeholders.
from langchain_core.prompts import ChatPromptTemplate

# RunnableBranch Routes input to different chains based on specified conditions.
from langchain_core.runnables import RunnableBranch

# Pydantic models you defined in schema. Each model defines the expected structure of an LLM response.
from src.schemas import (
    AccountAnalysis,
    BillingAnalysis,
    CancellationRefundAnalysis,
    GeneralAnalysis,
    OrderDeliveryAnalysis,
    ResolutionDecision,
    TechnicalAnalysis,
    TicketTriage,
)


# Defines which fields the LLM should focus on when analyzing each ticket category.
ANALYSIS_FOCUS = {
    # "billing": "- issue\n- amount\n- transaction_count\n- refund_required",
    "billing": (
        "- issue\n"
        "- amount\n"
        "- transaction_count\n"
        "- refund_required"
    ),
    # Both versions produce exactly the same string. So why use parentheses? Python allows you to split a long string across multiple lines using parentheses. Parentheses are being used only for better readability.


    "technical": (
        "- issue\n"
        "- affected_feature\n"
        "- error_message\n"
        "- troubleshooting_required"
    ),
    "account": (
        "- issue\n"
        "- access_problem\n"
        "- verification_required\n"
        "- account_status"
    ),
    "cancellation_refund": (
        "- request_type\n"
        "- reason\n"
        "- refund_required\n"
        "- retention_opportunity"
    ),
    "order_delivery": (
        "- issue\n"
        "- order_status\n"
        "- delivery_problem\n"
        "- customer_request"
    ),
    "general": (
        "- issue\n"
        "- customer_request\n"
        "- additional_context"
    ),
}


def load_prompt(file_name: str):
    try:
        # open(): Python's built-in function for opening files.

        # A computer stores files as bytes (binary data). When Python reads a text file, it needs to convert those bytes into readable characters. Encoding tells Python how to convert the file's stored bytes into readable text.

        # Why use UTF-8?
        # Because it is widely supported and provides consistent text handling across different operating systems.
        with open(f"src/prompts/{file_name}", "r", encoding="utf-8") as file:
            # file.read() reads the entire content of the file and returns the content as a Python string.
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {file_name}")


def create_triage_chain(llm):
    # Load the prompt from the prompts folder.
    prompt_text = load_prompt("classification_prompt.txt")

    # You take the raw string obtained from your text file and convert it into a LangChain prompt template.
    # why did we convert ?: Python Strings doesn't understand that {customer_name} and {ticket} are dynamic variables that should be replaced later whereas Langchain prompt template can identify the placeholders. 

    prompt = ChatPromptTemplate.from_template(prompt_text)
 
    # This configures the model to return a response matching your schema.
    structured_llm = llm.with_structured_output(TicketTriage)

    # Take the output of the prompt and pass it into the structured LLM.
    # The prompt gets its values for placeholders when the chain is invoked.
    # prompt | structured_llm does not execute immediately, it creates a chain.
    return prompt | structured_llm


def _create_analysis_chain(llm, category, schema):
    prompt_text = load_prompt("case_analysis_prompt.txt")
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # partial() allows you to pre-fill some of the variables in a prompt template. You don't have to provide every variable when invoking the chain.
    prompt = prompt.partial(
        category=category,
        analysis_focus=ANALYSIS_FOCUS[category],
    )

    structured_llm = llm.with_structured_output(schema)
    return prompt | structured_llm


def create_billing_chain(llm):
    return _create_analysis_chain(llm, "billing", BillingAnalysis)


def create_technical_chain(llm):
    return _create_analysis_chain(llm, "technical", TechnicalAnalysis)


def create_account_chain(llm):
    return _create_analysis_chain(llm, "account", AccountAnalysis)


def create_cancellation_refund_chain(llm):
    return _create_analysis_chain(
        llm, "cancellation_refund", CancellationRefundAnalysis
    )


def create_order_delivery_chain(llm):
    return _create_analysis_chain(llm, "order_delivery", OrderDeliveryAnalysis)


def create_general_chain(llm):
    return _create_analysis_chain(llm, "general", GeneralAnalysis)


# This function creates a router that decides which category-specific analysis chain should execute.
def create_router(llm):
    billing_chain = create_billing_chain(llm)
    technical_chain = create_technical_chain(llm)
    account_chain = create_account_chain(llm)
    cancellation_refund_chain = create_cancellation_refund_chain(llm)
    order_delivery_chain = create_order_delivery_chain(llm)
    general_chain = create_general_chain(llm)

    # The first condition that returns True determines which runnable receives the input and executes. If no condition matches, the default runnable executes.
    return RunnableBranch(
        (lambda x: x["category"] == "billing", billing_chain),
        (lambda x: x["category"] == "technical", technical_chain),
        (lambda x: x["category"] == "account", account_chain),
        (lambda x: x["category"] == "cancellation_refund", cancellation_refund_chain),
        (lambda x: x["category"] == "order_delivery", order_delivery_chain),
        general_chain,
    )


def create_resolution_chain(llm):
    prompt_text = load_prompt("resolution_prompt.txt")
    prompt = ChatPromptTemplate.from_template(prompt_text)
    structured_llm = llm.with_structured_output(ResolutionDecision)
    return prompt | structured_llm


def create_response_chain(llm):
    """
    Build the customer response chain.

    This chain only writes the reply. It should follow the resolution
    decision that was already made. 
    
    The response-generating LLM shouldn't independently decide whether to refund, escalate or reject a request. It should follow the decision already produced by the resolution chain.
    """
    prompt_text = load_prompt("response_prompt.txt")
    prompt = ChatPromptTemplate.from_template(prompt_text)

    # Plain text output is enough for the customer-facing reply.
    return prompt | llm | StrOutputParser()
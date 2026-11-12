"""
End-to-end support ticket workflow.

Think of it like a customer support department:
- One employee classifies the complaint.
- Another employee sends it to the correct department.
- A specialist investigates the issue.
- A decision-maker decides what to do.
- A communication employee writes back to the customer.
Your Python function process_ticket() is the manager coordinating all these people.
"""

from src.chains import (
    create_resolution_chain,
    create_response_chain,
    create_router,
    create_triage_chain,
)
from src.schemas import TicketResult


# Friendly labels used only for displaying the selected chain in the terminal.
CHAIN_LABELS = {
    "billing": "Billing Chain",
    "technical": "Technical Chain",
    "account": "Account Chain",
    "cancellation_refund": "Cancellation/Refund Chain",
    "order_delivery": "Order/Delivery Chain",
    "general": "General Chain",
}

# Creates all reusable chains required for processing customer support tickets.
# This function only CREATES the chains. It does not process any customer tickets.
# Actual execution happens inside process_ticket() when each chain is called using .invoke().
def build_workflow(llm):
    return {
        "triage_chain": create_triage_chain(llm),
        "router": create_router(llm),
        "resolution_chain": create_resolution_chain(llm),
        "response_chain": create_response_chain(llm),
    }


def process_ticket(ticket, workflow):
    """
    Run the full automation workflow for a single support ticket.

    Steps:
        1. Triage the ticket (category, priority, language)
        2. Route to a specialized analysis chain
        3. Decide the resolution
        4. Generate the customer response
        5. Return a final TicketResult

    Args:
        ticket (dict): One ticket with ticket_id, customer_name, and ticket.
        workflow (dict): Chains created by build_workflow().

    Returns:
        TicketResult: Final structured result for this ticket.
    """
    customer_name = ticket["customer_name"]
    ticket_text = ticket["ticket"]

    # ---- Stage 1: Ticket Triage ----
    triage = workflow["triage_chain"].invoke(
        {
            "customer_name": customer_name,
            "ticket": ticket_text,
        }
    )

    print(f"Category: {triage.category}")
    print(f"Priority: {triage.priority}")

    # dictionary.get(key, default_value)
    # default_value: The value returned if the key doesn't exist.
    print(f"Routing to: {CHAIN_LABELS.get(triage.category, 'General Chain')}")

    # ---- Stage 2 + 3: Routing and Case Analysis ----
    # The router looks at "category" and calls the matching analysis chain.
    # This entire dictionary becomes the input to RunnableBranch. It then executes the selected chain with the same original dictionary.
    case_analysis = workflow["router"].invoke(
        {
            "category": triage.category,
            "customer_name": customer_name,
            "ticket": ticket_text,
        }
    )

    # The router can return different Pydantic objects depending on the selected category ( BillingAnalysis, TechnicalAnalysis, AccountAnalysis, etc.).
    # model_dump_json() converts whichever Pydantic object was returned into a JSON string.
    case_analysis_text = case_analysis.model_dump_json(indent=2)

    # ---- Stage 4: Resolution Decision ----
    resolution = workflow["resolution_chain"].invoke(
        {
            "customer_name": customer_name,
            "ticket": ticket_text,
            "category": triage.category,
            "priority": triage.priority,
            "language": triage.language,
            "case_analysis": case_analysis_text,
        }
    )

    print(f"Resolution: {resolution.resolution_type}")
    print(f"Human Required: {'Yes' if resolution.requires_human else 'No'}")

    # ---- Stage 5: Response Generation ----
    # This step generate a customer-friendly response based on the resolution decision made in the previous stage.
    # The response chain does NOT make a new resolution decision. It only communicates the decision already made.
    response_text = workflow["response_chain"].invoke(
        {
            "customer_name": customer_name,
            "ticket": ticket_text,
            "category": triage.category,
            "priority": triage.priority,
            "language": triage.language,
            "case_analysis": case_analysis_text,
            "resolution_type": resolution.resolution_type,
            "recommended_action": resolution.recommended_action,
            "requires_human": resolution.requires_human,
            "resolution_reason": resolution.reason,
        }
    )

    # ---- Stage 6: Final Structured Output ----
    return TicketResult(
        ticket_id=ticket["ticket_id"],
        customer_name=customer_name,
        category=triage.category,
        priority=triage.priority,
        language=triage.language,
        case_summary=case_analysis_text,
        resolution_type=resolution.resolution_type,
        recommended_action=resolution.recommended_action,
        requires_human=resolution.requires_human,
        resolution_reason=resolution.reason,
        response=response_text.strip(),
    )
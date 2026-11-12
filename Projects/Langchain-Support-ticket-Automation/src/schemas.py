
"""
Pydantic schemas for the support ticket automation workflow.

Each model defines the expected structure of an LLM response.
"""

# In Python, Literal is used to restrict a variable to a specific set of allowed values.
from typing import Literal

from pydantic import BaseModel, Field


Category = Literal[
    "billing",
    "technical",
    "account",
    "cancellation_refund",
    "order_delivery",
    "general",
]

Priority = Literal["low", "medium", "high", "critical"]

ResolutionType = Literal[
    "self_service",        # Customer can solve it independently using the provided instructions.
    "resolve",             # Support system directly fixes the customer's issue.
    "escalate",            # Requires higher-level support.
    "request_information", # Additional details are needed.
]


class TicketTriage(BaseModel):
    category: Category = Field(description="Category of the customer issue")
    priority: Priority = Field(description="Urgency of the ticket")
    language: str = Field(description="Customer's preferred language")


class BillingAnalysis(BaseModel):
    issue: str = Field(description="Summary of the billing issue")
    amount: str = Field(description="Transaction amount or unknown")
    transaction_count: int = Field(description="Number of transactions involved")
    refund_required: bool = Field(description="Whether a refund is needed")


class TechnicalAnalysis(BaseModel):
    issue: str = Field(description="Summary of the technical issue")
    affected_feature: str = Field(description="Affected application feature")
    error_message: str = Field(description="Reported error message, or 'none'")
    troubleshooting_required: bool = Field(description="Whether further troubleshooting is needed")


class AccountAnalysis(BaseModel):
    issue: str = Field(description="Summary of the account issue")
    access_blocked: bool = Field(description="Whether account access is blocked")
    verification_required: bool = Field(description="Whether identity verification is needed")
    account_status: str = Field(description="Current account status, or 'unknown'")


class CancellationRefundAnalysis(BaseModel):
    request_type: str = Field(description="Cancellation, refund, or both")
    reason: str = Field(description="Reason for the cancellation or refund request")
    refund_required: bool = Field(description="Whether a refund is requested")
    retention_opportunity: bool = Field(description="Whether customer retention is possible")


class OrderDeliveryAnalysis(BaseModel):
    issue: str = Field(description="Summary of the order or delivery issue")
    order_status: str = Field(description="Current order status, or 'unknown'")
    delivery_problem: bool = Field(description="Whether delivery is the main issue")
    customer_request: str = Field(description="Action requested by the customer")


class GeneralAnalysis(BaseModel):
    issue: str = Field(description="Summary of the customer issue")
    customer_request: str = Field(description="What the customer is asking for")
    additional_context: str = Field(description="Additional relevant ticket details")


class ResolutionDecision(BaseModel):
    # stage 4

    resolution_type: ResolutionType = Field(description="Selected resolution approach")
    recommended_action: str = Field(description="Recommended next action")
    requires_human: bool = Field(description="Whether human intervention is needed")
    reason: str = Field(description="Reason for the resolution decision")


class TicketResult(BaseModel):
    # stage 5
    # Final structured output for one processed support ticket.

    ticket_id: str = Field(description="Unique ticket identifier")
    customer_name: str = Field(description="Name of the customer")
    category: str = Field(description="Ticket category")
    priority: str = Field(description="Ticket priority")
    language: str = Field(description="Customer's language")
    case_summary: str = Field(description="Summary of the customer case")
    resolution_type: str = Field(description="Selected resolution approach")
    recommended_action: str = Field(description="Recommended action to take")
    requires_human: bool = Field(description="Whether human intervention is needed")
    resolution_reason: str = Field(description="Reason for the resolution approach")
    response: str = Field(description="Final response to the customer")
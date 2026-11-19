import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

class CheckoutInitiateRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", clean):
            raise ValueError("Format d'adresse e-mail invalide")
        return clean

class CheckoutInitiateResponse(BaseModel):
    order_id: str
    checkout_id: str
    checkout_url: str
    product_code: str
    amount_minor: int
    currency: str
    status: str

class OrderStatusResponse(BaseModel):
    order_id: str
    status: str
    amount_minor: int
    currency: str
    is_paid: bool
    portal_access_token: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None

class ProgressStepItem(BaseModel):
    step_number: int
    step_title: str
    is_completed: bool
    completed_at: Optional[datetime] = None

class ValidateStepRequest(BaseModel):
    step_number: int

class SupportAskRequest(BaseModel):
    question: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class SupportAskResponse(BaseModel):
    answer: str
    citations: List[str]
    suggest_ticket: bool

class CreateTicketRequest(BaseModel):
    subject: str
    conversation: List[Dict[str, str]]
    technical_context: Optional[Dict[str, Any]] = None

class CreateTicketResponse(BaseModel):
    ticket_id: str
    status: str
    message: str

class AdminStatsResponse(BaseModel):
    total_orders: int
    paid_orders: int
    total_revenue_xof: int
    conversion_rate: float
    total_downloads: int
    active_tickets: int

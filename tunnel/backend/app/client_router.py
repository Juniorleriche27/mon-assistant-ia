import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Customer, CustomerProgress, Order, SupportTicket
from app.schemas import (
    CreateTicketRequest,
    CreateTicketResponse,
    ProgressStepItem,
    SupportAskRequest,
    SupportAskResponse,
    ValidateStepRequest,
)
from app.support_ai import ask_cohere_support

router = APIRouter(prefix="/api/v1/client", tags=["Espace Client"])

@router.get("/dashboard")
def get_client_dashboard(
    email: str = Query(...),
    order_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retourne les données du cockpit client et les 6 étapes d'onboarding.
    """
    clean_email = email.strip().lower()
    customer = db.query(Customer).filter(Customer.email == clean_email).first()
    if not customer:
        raise HTTPException(status_code=403, detail="Compte introuvable")

    query = db.query(Order).filter(
        Order.customer_id == customer.id,
        Order.status == "succeeded"
    )
    if order_id:
        query = query.filter(Order.id == order_id)

    order = query.order_by(Order.created_at.desc()).first()

    if not order:
        raise HTTPException(status_code=403, detail="Accès non autorisé : aucun paiement confirmé")

    steps = (
        db.query(CustomerProgress)
        .filter(CustomerProgress.customer_id == customer.id)
        .order_by(CustomerProgress.step_number.asc())
        .all()
    )

    steps_data = [
        ProgressStepItem(
            step_number=s.step_number,
            step_title=s.step_title,
            is_completed=s.is_completed,
            completed_at=s.completed_at
        )
        for s in steps
    ]

    return {
        "customer": {
            "id": customer.id,
            "email": customer.email,
            "full_name": customer.full_name,
        },
        "order": {
            "id": order.id,
            "status": order.status,
            "product_code": order.product_code,
            "paid_at": order.paid_at,
        },
        "steps": steps_data,
        "download_links": {
            "livre_pdf": f"/api/v1/downloads/pack/livre?email={customer.email}&order_id={order.id}",
            "projet_zip": f"/api/v1/downloads/pack/projet?email={customer.email}&order_id={order.id}",
        }
    }

@router.post("/progress/validate")
def validate_progress_step(
    payload: ValidateStepRequest,
    email: str = Query(...),
    order_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Valide une étape d'installation réelle dans le parcours guidé de l'apprenant.
    """
    clean_email = email.strip().lower()
    customer = db.query(Customer).filter(Customer.email == clean_email).first()
    if not customer:
        raise HTTPException(status_code=403, detail="Compte introuvable")

    # Vérification d'accès
    query = db.query(Order).filter(
        Order.customer_id == customer.id,
        Order.status == "succeeded"
    )
    if order_id:
        query = query.filter(Order.id == order_id)
    order = query.first()

    if not order:
        raise HTTPException(status_code=403, detail="Accès réservé aux acheteurs confirmés")

    step = db.query(CustomerProgress).filter(
        CustomerProgress.customer_id == customer.id,
        CustomerProgress.step_number == payload.step_number
    ).first()

    if not step:
        raise HTTPException(status_code=404, detail="Étape d'apprentissage introuvable")

    step.is_completed = True
    step.completed_at = datetime.utcnow()
    db.commit()

    return {
        "success": True,
        "step_number": step.step_number,
        "is_completed": step.is_completed,
        "completed_at": step.completed_at
    }

@router.post("/support/ask", response_model=SupportAskResponse)
async def ask_support_assistant(payload: SupportAskRequest):
    """
    Interrogation de l'assistant IA Cohere fondé sur le manuscrit du livre.
    """
    res = await ask_cohere_support(payload.question, payload.conversation_history)
    return SupportAskResponse(
        answer=res["answer"],
        citations=res["citations"],
        suggest_ticket=res["suggest_ticket"]
    )

@router.post("/tickets/create", response_model=CreateTicketResponse)
def create_support_ticket(
    payload: CreateTicketRequest,
    email: str = Query(...),
    order_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Ouverture d'un ticket formateur en cas de blocage non résolu par l'IA.
    """
    clean_email = email.strip().lower()
    customer = db.query(Customer).filter(Customer.email == clean_email).first()
    if not customer:
        raise HTTPException(status_code=403, detail="Compte introuvable")

    ticket_data = {
        "conversation": payload.conversation,
        "technical_context": payload.technical_context or {}
    }

    ticket = SupportTicket(
        customer_id=customer.id,
        subject=payload.subject[:255],
        conversation_json=json.dumps(ticket_data, ensure_ascii=False),
        status="open",
    )
    db.add(ticket)
    db.commit()

    return CreateTicketResponse(
        ticket_id=ticket.id,
        status=ticket.status,
        message="Votre ticket a été transmis à l'équipe KORYXA. Nous l'examinerons dans les meilleurs délais."
    )

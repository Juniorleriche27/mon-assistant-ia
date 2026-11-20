from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Customer, DownloadLog, Order, PaymentRecord, SupportTicket
from app.schemas import AdminStatsResponse

router = APIRouter(prefix="/api/v1/admin", tags=["Administration"])

def verify_admin_token(x_admin_token: str = Header(default="")):
    if not settings.ADMIN_SECRET_TOKEN or x_admin_token != settings.ADMIN_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Accès administration refusé : token invalide"
        )

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_token)
):
    """
    Télémétrie éthique : volumes de vente, chiffre d'affaires XOF, téléchargements et tickets.
    """
    total_orders = db.query(Order).count()
    paid_orders = db.query(Order).filter(Order.status == "succeeded").count()
    total_revenue_xof = paid_orders * settings.PRODUCT_AMOUNT_XOF
    conversion_rate = round((paid_orders / total_orders * 100), 2) if total_orders > 0 else 0.0
    total_downloads = db.query(DownloadLog).count()
    active_tickets = db.query(SupportTicket).filter(SupportTicket.status == "open").count()

    return AdminStatsResponse(
        total_orders=total_orders,
        paid_orders=paid_orders,
        total_revenue_xof=total_revenue_xof,
        conversion_rate=conversion_rate,
        total_downloads=total_downloads,
        active_tickets=active_tickets
    )

@router.get("/orders")
def get_all_orders(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_token)
):
    """
    Liste des commandes et paiements associés.
    """
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(100).all()
    results = []
    for ord in orders:
        cust = db.query(Customer).filter(Customer.id == ord.customer_id).first()
        results.append({
            "order_id": ord.id,
            "customer_email": cust.email if cust else "inconnu",
            "customer_name": cust.full_name if cust else "",
            "amount_minor": ord.amount_minor,
            "currency": ord.currency,
            "status": ord.status,
            "created_at": ord.created_at,
            "paid_at": ord.paid_at,
        })
    return results

@router.post("/orders/{order_id}/simulate-payment")
def simulate_order_payment(
    order_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_token)
):
    """
    Simulation administrative d'un paiement réussi pour valider le parcours client
    de bout en bout (téléchargements, onboarding, dashboard) sans frais bancaires réels.
    """
    from datetime import datetime
    from app.models import CustomerProgress
    from app.webhook import INITIAL_ONBOARDING_STEPS

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    order.status = "succeeded"
    order.paid_at = datetime.utcnow()

    # Initialisation des 6 étapes d'onboarding
    for step_num, title in INITIAL_ONBOARDING_STEPS:
        existing = db.query(CustomerProgress).filter(
            CustomerProgress.customer_id == order.customer_id,
            CustomerProgress.step_number == step_num
        ).first()
        if not existing:
            db.add(CustomerProgress(
                customer_id=order.customer_id,
                step_number=step_num,
                step_title=title,
                is_completed=False
            ))
    db.commit()
    return {
        "success": True,
        "order_id": order.id,
        "status": order.status,
        "message": "Paiement validé avec succès en mode test administratif (0 F CFA dépensé)"
    }

@router.get("/tickets")
def get_all_tickets(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_token)
):
    """
    Liste des tickets de support ouverts par les clients.
    """
    tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).all()
    results = []
    for t in tickets:
        cust = db.query(Customer).filter(Customer.id == t.customer_id).first()
        results.append({
            "ticket_id": t.id,
            "customer_email": cust.email if cust else "inconnu",
            "subject": t.subject,
            "status": t.status,
            "created_at": t.created_at,
            "conversation_history": t.conversation_json,
        })
    return results

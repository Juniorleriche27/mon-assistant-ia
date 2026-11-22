from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.models import Customer, CustomerProgress, DownloadLog, Order, PaymentRecord, SupportTicket
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

@router.get("/bi/overview")
def get_bi_overview(
    db: Session = Depends(get_db),
    _: None = Depends(verify_admin_token)
):
    """
    Cockpit Business Intelligence & Performance Scaling KORYXA Admin.
    Retourne l'ensemble des métriques de vente, d'entonnoir, de déperdition,
    de téléchargements, d'onboarding et de comparaison vs WhatsApp manuel.
    """
    total_orders = db.query(Order).count()
    paid_orders = db.query(Order).filter(Order.status == "succeeded").count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    failed_orders = db.query(Order).filter(Order.status.in_(["failed", "cancelled"])).count()
    total_revenue_xof = paid_orders * settings.PRODUCT_AMOUNT_XOF
    conversion_rate = round((paid_orders / total_orders * 100), 2) if total_orders > 0 else 0.0

    total_downloads = db.query(DownloadLog).count()
    dl_livre = db.query(DownloadLog).filter(
        DownloadLog.asset_name.ilike("%livre%") | DownloadLog.asset_name.ilike("%pdf%")
    ).count()
    dl_code = db.query(DownloadLog).filter(
        DownloadLog.asset_name.ilike("%code%") | DownloadLog.asset_name.ilike("%projet%")
    ).count()
    dl_kit = db.query(DownloadLog).filter(
        DownloadLog.asset_name.ilike("%kit%")
    ).count()

    active_tickets = db.query(SupportTicket).filter(SupportTicket.status == "open").count()
    resolved_tickets = db.query(SupportTicket).filter(SupportTicket.status == "resolved").count()
    total_customers = db.query(Customer).count()

    # Étapes d'onboarding 1 à 6
    step_titles = [
        (1, "Lecture du guide & cadrage"),
        (2, "Environnement & clés Cohere"),
        (3, "Ingestion & chunking du corpus"),
        (4, "Backend RAG FastAPI & tests"),
        (5, "Frontend & citations sources"),
        (6, "Déploiement en production"),
    ]
    step_stats = []
    for step_num, default_title in step_titles:
        completed_count = db.query(CustomerProgress).filter(
            CustomerProgress.step_number == step_num,
            CustomerProgress.is_completed == True
        ).count()
        step_stats.append({
            "step_number": step_num,
            "title": default_title,
            "completed_count": completed_count
        })

    # Commandes récentes
    recent_orders = []
    orders = db.query(Order).order_by(Order.created_at.desc()).limit(50).all()
    for ord in orders:
        cust = db.query(Customer).filter(Customer.id == ord.customer_id).first()
        recent_orders.append({
            "order_id": ord.id,
            "customer_email": cust.email if cust else "inconnu",
            "customer_name": cust.full_name if cust else "",
            "customer_phone": cust.phone if cust else "",
            "amount_minor": ord.amount_minor,
            "currency": ord.currency,
            "status": ord.status,
            "created_at": ord.created_at.isoformat() if ord.created_at else None,
            "paid_at": ord.paid_at.isoformat() if ord.paid_at else None,
        })

    # Tickets récents
    recent_tickets = []
    tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).limit(20).all()
    for t in tickets:
        cust = db.query(Customer).filter(Customer.id == t.customer_id).first()
        recent_tickets.append({
            "ticket_id": t.id,
            "customer_email": cust.email if cust else "inconnu",
            "subject": t.subject,
            "status": t.status,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        })

    # Calcul des heures humaines économisées vs vente manuelle sur WhatsApp
    # ~25 minutes économisées par vente / checkout + 10 min par délivrance de fichier
    hours_saved = round((total_orders * 25 + total_downloads * 10) / 60.0, 1)

    return {
        "status": "success",
        "generated_at": datetime.utcnow().isoformat(),
        "kpis": {
            "total_orders": total_orders,
            "paid_orders": paid_orders,
            "pending_orders": pending_orders,
            "failed_orders": failed_orders,
            "total_revenue_xof": total_revenue_xof,
            "conversion_rate": conversion_rate,
            "total_downloads": total_downloads,
            "active_tickets": active_tickets,
            "resolved_tickets": resolved_tickets,
            "total_customers": total_customers,
            "hours_saved_vs_whatsapp": hours_saved,
            "autonomous_resolution_rate": 100.0 if (active_tickets + resolved_tickets == 0) else round((1 - (active_tickets / (total_orders + 1))) * 100, 1)
        },
        "funnel": {
            "checkout_started": total_orders,
            "payments_confirmed": paid_orders,
            "downloads_completed": total_downloads,
            "onboarding_active": step_stats[0]["completed_count"] if step_stats else 0,
            "onboarding_completed": step_stats[-1]["completed_count"] if step_stats else 0,
            "checkout_abandonment_rate": round(((total_orders - paid_orders) / total_orders * 100), 1) if total_orders > 0 else 0.0,
            "human_escalation_count": active_tickets + resolved_tickets
        },
        "downloads_breakdown": {
            "livre_pdf": dl_livre,
            "code_zip": dl_code,
            "kit_zip": dl_kit,
            "total": total_downloads
        },
        "onboarding_steps": step_stats,
        "recent_orders": recent_orders,
        "recent_tickets": recent_tickets
    }

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

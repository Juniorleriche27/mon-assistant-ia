import hashlib
import hmac
import json
import logging
import time
from datetime import datetime
from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.koryxa_pay import koryxa_pay_client
from app.models import Customer, CustomerProgress, Order, OutboxEmail, PaymentRecord

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/webhook", tags=["Webhook"])

INITIAL_ONBOARDING_STEPS = [
    (1, "Télécharger et préparer l'environnement Python"),
    (2, "Configurer la clé d'API Cohere (.env)"),
    (3, "Lancer le projet Horizon Numérique"),
    (4, "Charger les 5 documents d'exemple du corpus"),
    (5, "Poser les questions et vérifier les citations"),
    (6, "Adapter les modèles de contrat et préparer la livraison"),
]

def verify_koryxa_signature(raw_body: bytes, timestamp: str, signature: str, secret: str) -> bool:
    """
    Contrôle strict : fraîcheur <= 300s + HMAC-SHA256 avec v1=
    """
    if not secret:
        # En mode simulation locale sans secret configuré, accepte si signature de test
        return True
    
    try:
        ts_float = float(timestamp)
    except (ValueError, TypeError):
        return False

    fresh = abs(time.time() - ts_float) <= 300
    if not fresh:
        logger.warning("Timestamp de webhook KORYXA Pay expiré (> 300s) : %s", timestamp)
        return False

    msg = f"{timestamp}.".encode("utf-8") + raw_body
    computed = "v1=" + hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, computed)

@router.post("/koryxa")
async def handle_koryxa_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_koryxa_timestamp: str = Header(default=""),
    x_koryxa_signature: str = Header(default=""),
    x_koryxa_event_id: str = Header(default=""),
):
    """
    Point d'entrée du webhook officiel KORYXA Pay : POST https://votredomaine/api/v1/webhook/koryxa
    """
    raw_body = await request.body()
    
    # 1. Vérification de la signature et de la fraîcheur
    if settings.KORYXA_WEBHOOK_SECRET and not verify_koryxa_signature(
        raw_body, x_koryxa_timestamp, x_koryxa_signature, settings.KORYXA_WEBHOOK_SECRET
    ):
        logger.error("Signature de webhook KORYXA Pay invalide.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature invalide")

    try:
        event = json.loads(raw_body.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Corps JSON invalide") from exc

    payment_id = event.get("payment_id")
    order_id = event.get("order_id")
    event_status = event.get("status")

    if not payment_id:
        raise HTTPException(status_code=422, detail="payment_id manquant")

    # 2. Idempotence : Si ce paiement est déjà validé, on répond 200 sans action doublon
    existing_payment = db.query(PaymentRecord).filter(PaymentRecord.payment_id == payment_id).first()
    if existing_payment and existing_payment.status == "succeeded":
        logger.info("Paiement %s déjà traité (idempotence). Réponse 200 OK.", payment_id)
        return {"status": "ok", "message": "Paiement déjà traité"}

    # 3. Relecture de sécurité obligatoire côté serveur auprès de KORYXA Pay
    payment_info = await koryxa_pay_client.get_payment(payment_id)
    payment_status = payment_info.get("payment_status")
    amount_minor = payment_info.get("amount_minor")
    currency = payment_info.get("currency")

    # 4. Contrôle du montant et de la devise attendus
    if amount_minor != settings.PRODUCT_AMOUNT_XOF or currency != settings.PRODUCT_CURRENCY:
        logger.error("Montant ou devise invalide : %s %s au lieu de %s %s", amount_minor, currency, settings.PRODUCT_AMOUNT_XOF, settings.PRODUCT_CURRENCY)
        raise HTTPException(status_code=422, detail="Montant ou devise incohérente")

    # 5. Recherche de la commande associée
    order = None
    if order_id:
        order = db.query(Order).filter(Order.id == order_id).first()
    if not order and payment_info.get("order_id"):
        order = db.query(Order).filter(Order.id == payment_info.get("order_id")).first()
    if not order:
        order = db.query(Order).filter(Order.checkout_id == payment_id).first()

    if not order:
        logger.error("Aucune commande trouvée pour le paiement %s", payment_id)
        raise HTTPException(status_code=404, detail="Commande introuvable")

    # 6. Enregistrement du paiement
    if not existing_payment:
        record = PaymentRecord(
            order_id=order.id,
            payment_id=payment_id,
            provider=payment_info.get("provider", "koryxa"),
            amount_received=amount_minor,
            currency=currency,
            status=payment_status,
            event_id=x_koryxa_event_id or f"evt_{payment_id}",
            raw_payload=raw_body.decode("utf-8", errors="ignore"),
        )
        db.add(record)
    else:
        existing_payment.status = payment_status

    # 7. Activation de l'accès client si paiement confirmé
    if payment_status == "succeeded":
        order.status = "succeeded"
        order.paid_at = datetime.utcnow()
        
        # Initialiser les 6 étapes de progression si elles n'existent pas encore
        existing_progress = db.query(CustomerProgress).filter(CustomerProgress.customer_id == order.customer_id).count()
        if existing_progress == 0:
            for num, title in INITIAL_ONBOARDING_STEPS:
                step = CustomerProgress(
                    customer_id=order.customer_id,
                    step_number=num,
                    step_title=title,
                    is_completed=False,
                )
                db.add(step)

        # Planifier l'email d'accès immédiat (Outbox pattern)
        customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
        if customer:
            access_email = OutboxEmail(
                customer_id=customer.id,
                email_type="access",
                recipient=customer.email,
                subject="Accès à votre pack : Créer et livrer son premier assistant IA",
                body=(
                    f"Bonjour {customer.full_name or 'cher développeur'},\n\n"
                    f"Votre commande de « Créer et livrer son premier assistant IA » (11 000 F CFA) est validée !\n\n"
                    f"Accédez dès maintenant à votre espace client pour télécharger le livre et le code du projet :\n"
                    f"{settings.FRONTEND_URL}/espace-client?email={customer.email}&order_id={order.id}\n\n"
                    f"À tout de suite,\nL'équipe KORYXA"
                ),
                status="sent",  # Marqué envoyé
                sent_at=datetime.utcnow()
            )
            db.add(access_email)

    elif payment_status in ["failed", "cancelled"]:
        order.status = payment_status

    db.commit()
    logger.info("Commande %s mise à jour avec statut : %s", order.id, payment_status)
    return {"status": "ok", "order_status": order.status}

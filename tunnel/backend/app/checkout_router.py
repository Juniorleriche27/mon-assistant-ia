import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db
from app.koryxa_pay import koryxa_pay_client
from app.models import Customer, Order
from app.schemas import CheckoutInitiateRequest, CheckoutInitiateResponse, OrderStatusResponse

router = APIRouter(prefix="/api/v1/checkout", tags=["Checkout"])

@router.post("/initiate", response_model=CheckoutInitiateResponse)
async def initiate_checkout(payload: CheckoutInitiateRequest, db: Session = Depends(get_db)):
    """
    Initialisation de commande et appel à KORYXA Pay (HTTP 201).
    Le montant de 11 000 F CFA est fixé strictement côté serveur.
    """
    clean_email = payload.email.strip().lower()
    
    # 1. Récupération ou création du client
    customer = db.query(Customer).filter(Customer.email == clean_email).first()
    if not customer:
        customer = Customer(
            email=clean_email,
            full_name=payload.full_name.strip(),
            phone=payload.phone.strip() if payload.phone else None
        )
        db.add(customer)
        db.flush()

    # 2. Clé d'idempotence unique par commande
    idempotency_key = f"cmd_{customer.id[:8]}_{int(time.time())}"

    # 3. Création de la commande en base locale (statut pending)
    order = Order(
        customer_id=customer.id,
        product_code=settings.PRODUCT_CODE,
        amount_minor=settings.PRODUCT_AMOUNT_XOF,
        currency=settings.PRODUCT_CURRENCY,
        status="pending",
        idempotency_key=idempotency_key,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # 4. Appel à l'API KORYXA Pay (https://api-pay.koryxa.fr/v1/client/checkouts)
    try:
        checkout_res = await koryxa_pay_client.create_checkout(
            product_code=settings.PRODUCT_CODE,
            description=settings.PRODUCT_NAME,
            customer_id=customer.email,
            amount_minor=settings.PRODUCT_AMOUNT_XOF,
            currency=settings.PRODUCT_CURRENCY,
            idempotency_key=idempotency_key,
            success_url=f"{settings.FRONTEND_URL}/commande/statut?order_id={order.id}&success=1",
            failure_url=f"{settings.FRONTEND_URL}/commande/statut?order_id={order.id}&failed=1",
            metadata={
                "order_id": order.id,
                "customer_email": customer.email,
                "customer_name": customer.full_name
            }
        )
    except Exception as exc:
        order.status = "failed"
        db.commit()
        raise exc

    # 5. Enregistrement des références KORYXA Pay
    order.checkout_id = checkout_res.get("payment_id")
    order.checkout_url = checkout_res.get("checkout_url")
    db.commit()

    return CheckoutInitiateResponse(
        order_id=order.id,
        checkout_id=checkout_res.get("payment_id", ""),
        checkout_url=checkout_res.get("checkout_url", ""),
        product_code=order.product_code,
        amount_minor=order.amount_minor,
        currency=order.currency,
        status=order.status,
    )

@router.get("/status/{order_id}", response_model=OrderStatusResponse)
def get_order_status(order_id: str, db: Session = Depends(get_db)):
    """
    Consultation de l'état d'une commande par le frontend.
    Ne valide jamais un paiement : seule la notification serveur / relecture le fait.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")

    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    portal_access = None
    if order.status == "succeeded" and customer:
        portal_access = f"{settings.FRONTEND_URL}/espace-client?email={customer.email}&order_id={order.id}"

    return OrderStatusResponse(
        order_id=order.id,
        status=order.status,
        amount_minor=order.amount_minor,
        currency=order.currency,
        is_paid=(order.status == "succeeded"),
        portal_access_token=portal_access,
        created_at=order.created_at,
        paid_at=order.paid_at,
    )

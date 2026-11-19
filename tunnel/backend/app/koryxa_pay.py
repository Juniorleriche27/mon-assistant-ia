import json
import logging
from typing import Any, Dict, Optional
import httpx
from fastapi import HTTPException, status
from app.config import settings

logger = logging.getLogger(__name__)

class KoryxaPayClient:
    def __init__(self):
        self.base_url = settings.KORYXA_PAY_BASE_URL
        self.project_code = settings.KORYXA_PAY_PROJECT_CODE
        self.project_key = settings.KORYXA_PAY_PROJECT_KEY

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Project-Code": self.project_code,
            "X-Project-Key": self.project_key,
        }

    async def create_checkout(
        self,
        product_code: str,
        description: str,
        customer_id: str,
        amount_minor: int,
        currency: str,
        idempotency_key: str,
        success_url: Optional[str] = None,
        failure_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Crée une session de paiement côté serveur sur KORYXA Payment (HTTP 201).
        Point d'entrée : POST https://api-pay.koryxa.fr/v1/client/checkouts
        """
        # Mode simulation local si la clé n'est pas encore configurée en production
        if not self.project_key or self.project_key.startswith("sim_"):
            logger.info("Mode simulation KORYXA Pay actif (pas de clé de production configurée).")
            sim_payment_id = f"pay_sim_{idempotency_key[:16]}"
            return {
                "order_id": idempotency_key,
                "payment_id": sim_payment_id,
                "payment_status": "pending",
                "provider": "leekpay_simulation",
                "provider_payment_id": f"ref_{sim_payment_id}",
                "checkout_url": f"{settings.FRONTEND_URL}/commande/statut?payment_id={sim_payment_id}&order_id={idempotency_key}&simulated=1",
                "return_url": f"/payment/{sim_payment_id}",
                "product_code": product_code,
                "description": description,
                "customer_id": customer_id,
                "amount_minor": amount_minor,
                "currency": currency,
                "metadata": metadata or {},
            }

        url = f"{self.base_url}/v1/client/checkouts"
        payload = {
            "product_code": product_code,
            "description": description[:255],
            "customer_id": customer_id,
            "amount_minor": amount_minor,
            "currency": currency,
            "idempotency_key": idempotency_key,
            "metadata": metadata or {},
        }
        if success_url:
            payload["success_url"] = success_url
        if failure_url:
            payload["failure_url"] = failure_url

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(url, json=payload, headers=self._get_headers())
            except Exception as exc:
                logger.error("Erreur de connexion à KORYXA Pay : %s", exc)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Passerelle KORYXA Pay temporairement inaccessible."
                ) from exc

        if response.status_code == 201:
            return response.json()
        
        # Gestion des codes d'erreur selon la documentation KORYXA Pay
        err_data = response.json() if "application/json" in response.headers.get("content-type", "") else {"detail": response.text}
        logger.error("KORYXA Pay HTTP %s : %s", response.status_code, err_data)

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Clé ou code projet KORYXA Pay invalide.")
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="Projet suspendu ou accès KORYXA Pay refusé.")
        if response.status_code == 409:
            raise HTTPException(status_code=409, detail="Conflit d'état ou d'idempotency sur le paiement.")
        if response.status_code == 422:
            raise HTTPException(status_code=422, detail=f"Données de paiement invalides : {err_data}")
        
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erreur passerelle KORYXA Pay ({response.status_code})"
        )

    async def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Relecture sécurisée du statut du paiement côté serveur.
        Point d'entrée : GET https://api-pay.koryxa.fr/v1/client/payments/{payment_id}
        """
        if not self.project_key or self.project_key.startswith("sim_"):
            # En mode simulation
            return {
                "payment_id": payment_id,
                "order_id": payment_id.replace("pay_sim_", ""),
                "payment_status": "succeeded",
                "amount_minor": settings.PRODUCT_AMOUNT_XOF,
                "currency": settings.PRODUCT_CURRENCY,
                "provider": "leekpay_simulation"
            }

        url = f"{self.base_url}/v1/client/payments/{payment_id}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.get(url, headers=self._get_headers())
            except Exception as exc:
                logger.error("Impossible de joindre KORYXA Pay pour relecture : %s", exc)
                raise HTTPException(status_code=503, detail="Vérification serveur KORYXA Pay indisponible.") from exc

        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Paiement KORYXA introuvable.")
        
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erreur de vérification KORYXA Pay ({response.status_code})"
        )

koryxa_pay_client = KoryxaPayClient()

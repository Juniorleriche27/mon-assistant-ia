import hashlib
import hmac
import json
import os
import time
import unittest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Setup test environment
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["KORYXA_PAY_PROJECT_KEY"] = "sim_test_key"
os.environ["KORYXA_WEBHOOK_SECRET"] = "whsec_test_secret_for_koryxa_pay"
os.environ["COHERE_API_KEY"] = "sim_cohere_key"

from app.config import settings
from app.db import Base, get_db
from app.main import app
from app.models import Customer, CustomerProgress, Order, OutboxEmail, PaymentRecord
from app.automation import evaluate_and_queue_drips

# In-memory test DB with StaticPool to share state across requests
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class TestKoryxaTunnel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=test_engine)
        cls.client = TestClient(app)

    def setUp(self):
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_01_checkout_initiate(self):
        """Initialise une commande de 11 000 FCFA avec KORYXA Pay."""
        payload = {
            "email": "dev.test@example.com",
            "full_name": "Koffi Développeur",
            "phone": "+22890000000"
        }
        res = self.client.post("/api/v1/checkout/initiate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["amount_minor"], 11000)
        self.assertEqual(data["currency"], "XOF")
        self.assertEqual(data["status"], "pending")
        self.assertTrue(data["checkout_url"].startswith("http"))
        self.assertTrue(len(data["order_id"]) > 0)

        # Vérification en base
        order = self.db.query(Order).filter(Order.id == data["order_id"]).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, "pending")

    def test_02_webhook_signature_security(self):
        """Teste le contrôle strict de signature HMAC-SHA256 et de fraîcheur timestamp."""
        now_ts = str(int(time.time()))
        body_dict = {
            "event": "payment.status.changed",
            "payment_id": "pay_test_security",
            "order_id": "ord_fake",
            "status": "succeeded"
        }
        raw_body = json.dumps(body_dict).encode("utf-8")
        secret = settings.KORYXA_WEBHOOK_SECRET

        # Signature correcte
        msg = f"{now_ts}.".encode("utf-8") + raw_body
        valid_sig = "v1=" + hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

        # Fausse signature -> 401
        res_bad_sig = self.client.post(
            "/api/v1/webhook/koryxa",
            content=raw_body,
            headers={"x-koryxa-timestamp": now_ts, "x-koryxa-signature": "v1=bad_signature"}
        )
        self.assertEqual(res_bad_sig.status_code, 401)

        # Timestamp expiré (> 300s) -> 401
        old_ts = str(int(time.time()) - 350)
        old_msg = f"{old_ts}.".encode("utf-8") + raw_body
        old_sig = "v1=" + hmac.new(secret.encode("utf-8"), old_msg, hashlib.sha256).hexdigest()
        res_expired = self.client.post(
            "/api/v1/webhook/koryxa",
            content=raw_body,
            headers={"x-koryxa-timestamp": old_ts, "x-koryxa-signature": old_sig}
        )
        self.assertEqual(res_expired.status_code, 401)

    def test_03_payment_confirmation_and_idempotence(self):
        """Vérifie l'activation après webhook valide et l'idempotence stricte (aucun doublon)."""
        # 1. Créer une commande
        init_res = self.client.post("/api/v1/checkout/initiate", json={
            "email": "yayra.buyer@example.com",
            "full_name": "Yayra L.",
        })
        order_id = init_res.json()["order_id"]

        # 2. Envoyer le webhook de confirmation
        now_ts = str(int(time.time()))
        payment_id = f"pay_sim_{order_id[:16]}"
        body = json.dumps({
            "event": "payment.status.changed",
            "payment_id": payment_id,
            "order_id": order_id,
            "status": "succeeded"
        }).encode("utf-8")

        secret = settings.KORYXA_WEBHOOK_SECRET
        sig = "v1=" + hmac.new(secret.encode("utf-8"), f"{now_ts}.".encode("utf-8") + body, hashlib.sha256).hexdigest()

        res_webhook = self.client.post(
            "/api/v1/webhook/koryxa",
            content=body,
            headers={
                "x-koryxa-timestamp": now_ts,
                "x-koryxa-signature": sig,
                "x-koryxa-event-id": f"evt_{payment_id}"
            }
        )
        self.assertEqual(res_webhook.status_code, 200)

        # 3. Vérifier que la commande est SUCCEEDED et que les 6 étapes sont créées
        order = self.db.query(Order).filter(Order.id == order_id).first()
        self.assertEqual(order.status, "succeeded")
        self.assertIsNotNone(order.paid_at)

        steps = self.db.query(CustomerProgress).filter(CustomerProgress.customer_id == order.customer_id).all()
        self.assertEqual(len(steps), 6)

        # 4. Idempotence : Répéter le même webhook
        res_rejeu = self.client.post(
            "/api/v1/webhook/koryxa",
            content=body,
            headers={
                "x-koryxa-timestamp": now_ts,
                "x-koryxa-signature": sig,
                "x-koryxa-event-id": f"evt_{payment_id}"
            }
        )
        self.assertEqual(res_rejeu.status_code, 200)
        self.assertIn("déjà traité", res_rejeu.json()["message"])

        # Vérifier que les étapes n'ont pas été dupliquées (toujours 6)
        steps_after = self.db.query(CustomerProgress).filter(CustomerProgress.customer_id == order.customer_id).all()
        self.assertEqual(len(steps_after), 6)

    def test_04_downloads_access_control(self):
        """Vérifie le téléchargement public de l'extrait et l'accès protégé aux livrables payants."""
        # Extrait gratuit : accessible publiquement sans authentification
        res_sample = self.client.get("/api/v1/downloads/extrait-gratuit")
        self.assertIn(res_sample.status_code, [200, 404])  # 200 si fichier présent

        # Tentative d'accès au pack sans paiement -> 403 Forbidden
        res_unauth = self.client.get(
            "/api/v1/downloads/pack/livre",
            params={"email": "hacker@example.com", "order_id": "fake_order_id"}
        )
        self.assertEqual(res_unauth.status_code, 403)

        # Accès avec client payé
        order = self.db.query(Order).filter(Order.status == "succeeded").first()
        self.assertIsNotNone(order)
        cust = self.db.query(Customer).filter(Customer.id == order.customer_id).first()

        res_paid = self.client.get(
            "/api/v1/downloads/pack/livre",
            params={"email": cust.email, "order_id": order.id}
        )
        # S'il trouve le fichier sur le disque local de test, retourne 200
        self.assertEqual(res_paid.status_code, 200)

    def test_05_client_dashboard_and_progress_validation(self):
        """Vérifie le chargement du dashboard client et la validation d'une étape d'onboarding."""
        order = self.db.query(Order).filter(Order.status == "succeeded").first()
        cust = self.db.query(Customer).filter(Customer.id == order.customer_id).first()

        res_dash = self.client.get(
            "/api/v1/client/dashboard",
            params={"email": cust.email, "order_id": order.id}
        )
        self.assertEqual(res_dash.status_code, 200)
        dash_data = res_dash.json()
        self.assertEqual(len(dash_data["steps"]), 6)
        self.assertFalse(dash_data["steps"][0]["is_completed"])

        # Valider l'étape 1
        res_val = self.client.post(
            "/api/v1/client/progress/validate",
            params={"email": cust.email, "order_id": order.id},
            json={"step_number": 1}
        )
        self.assertEqual(res_val.status_code, 200)
        self.assertTrue(res_val.json()["is_completed"])

        # Re-vérifier dashboard
        res_dash2 = self.client.get(
            "/api/v1/client/dashboard",
            params={"email": cust.email, "order_id": order.id}
        )
        self.assertTrue(res_dash2.json()["steps"][0]["is_completed"])

    def test_06_support_ai_citations(self):
        """Vérifie que l'assistant support répond et cite les chapitres du livre."""
        res_ask = self.client.post(
            "/api/v1/client/support/ask",
            json={"question": "Comment configurer Cohere et préparer le RAG ?"}
        )
        self.assertEqual(res_ask.status_code, 200)
        data = res_ask.json()
        self.assertTrue(len(data["citations"]) > 0)
        self.assertIn("Chapitre", data["citations"][0])
        self.assertTrue(len(data["answer"]) > 50)

    def test_07_automation_drip_suppression(self):
        """Vérifie que la relance J+2 est annulée pour un client ayant déjà validé l'étape 1."""
        order = self.db.query(Order).filter(Order.status == "succeeded").first()
        # Simuler un achat datant de 3 jours
        order.paid_at = datetime.utcnow() - timedelta(days=3)
        self.db.commit()

        # Évaluer les drips
        res_drips = evaluate_and_queue_drips(self.db)
        # Comme l'étape 1 a été validée dans le test 5, la relance J+2 doit être sautée (skipped_completed >= 1)
        self.assertGreaterEqual(res_drips["skipped_completed"], 1)

if __name__ == "__main__":
    unittest.main()

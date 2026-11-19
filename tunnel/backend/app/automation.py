import logging
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models import Customer, CustomerProgress, Order, OutboxEmail

logger = logging.getLogger(__name__)

DRIP_RULES = [
    {
        "type": "drip_j2",
        "days": 2,
        "prereq_step": 1,
        "subject": "Besoin d'un coup de main pour installer votre environnement Python ?",
        "body_template": (
            "Bonjour {name},\n\n"
            "Deux jours se sont écoulés depuis votre acquisition du pack « Créer et livrer son premier assistant IA ».\n"
            "Avez-vous réussi à préparer votre environnement virtuel Python et installer les dépendances ?\n\n"
            "Si vous rencontrez le moindre blocage, posez directement votre question à l'assistant IA intégré dans votre espace client.\n\n"
            "Bien à vous,\nL'équipe KORYXA"
        )
    },
    {
        "type": "drip_j5",
        "days": 5,
        "prereq_step": 4,
        "subject": "Conseil KORYXA : L'importance du corpus de test avec Cohere",
        "body_template": (
            "Bonjour {name},\n\n"
            "À l'étape 4 du parcours, vous indexez les 5 documents d'exemple d'Horizon Numérique.\n"
            "Prenez le temps d'observer comment les citations de sources sont conservées. "
            "C'est ce qui fait la différence entre une IA qui invente et un assistant d'entreprise fiable.\n\n"
            "Bonne continuation dans votre pratique !\nL'équipe KORYXA"
        )
    },
    {
        "type": "drip_j10",
        "days": 10,
        "prereq_step": 6,
        "subject": "Prêt pour votre premier client ? Utilisez les modèles de livraison fournis",
        "body_template": (
            "Bonjour {name},\n\n"
            "Votre pack contient 4 modèles indispensables pour cadrer, chiffrer et réceptionner un assistant IA auprès d'un client réel :\n"
            "- 01_cahier_des_charges_modele.md\n"
            "- 02_modele_devis_et_maintenance.md\n"
            "- 03_fiche_de_reception_client.md\n"
            "- 04_grille_evaluation_et_couts.md\n\n"
            "N'hésitez pas à les adapter pour vos propres propositions commerciales.\n\n"
            "Excellente réussite,\nL'équipe KORYXA"
        )
    }
]

def evaluate_and_queue_drips(db: Session) -> Dict[str, int]:
    """
    Évalue les relances pédagogiques en fonction de la progression réelle de l'acheteur.
    Un client ayant validé l'étape correspondante ne reçoit JAMAIS de relance inutile.
    """
    now = datetime.utcnow()
    queued = 0
    skipped_completed = 0
    
    # Récupérer les commandes réussies
    paid_orders = db.query(Order).filter(Order.status == "succeeded").all()

    for order in paid_orders:
        if not order.paid_at:
            continue
            
        customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
        if not customer:
            continue

        days_since_paid = (now - order.paid_at).total_seconds() / 86400.0

        for rule in DRIP_RULES:
            if days_since_paid >= rule["days"]:
                # Vérifier si cet email a déjà été programmé ou envoyé
                already_exists = db.query(OutboxEmail).filter(
                    OutboxEmail.customer_id == customer.id,
                    OutboxEmail.email_type == rule["type"]
                ).first()

                if already_exists:
                    continue

                # Vérifier la progression de l'étape requise
                step_progress = db.query(CustomerProgress).filter(
                    CustomerProgress.customer_id == customer.id,
                    CustomerProgress.step_number == rule["prereq_step"]
                ).first()

                # Si l'étape est DÉJÀ complétée, on n'envoie pas de relance (suppression intelligente)
                if step_progress and step_progress.is_completed:
                    skipped_completed += 1
                    # Enregistrer comme annulé pour traçabilité
                    db.add(OutboxEmail(
                        customer_id=customer.id,
                        email_type=rule["type"],
                        recipient=customer.email,
                        subject=rule["subject"],
                        body="Annulé : étape déjà validée par l'apprenant.",
                        status="cancelled",
                        sent_at=now
                    ))
                    continue

                # Sinon, programmer l'email
                email_entry = OutboxEmail(
                    customer_id=customer.id,
                    email_type=rule["type"],
                    recipient=customer.email,
                    subject=rule["subject"],
                    body=rule["body_template"].format(name=customer.full_name or "développeur"),
                    status="sent",  # Marqué envoyé
                    sent_at=now
                )
                db.add(email_entry)
                queued += 1

    db.commit()
    logger.info("Évaluation des relances : %d programmées, %d ignorées (étapes déjà complétées).", queued, skipped_completed)
    return {"queued": queued, "skipped_completed": skipped_completed}

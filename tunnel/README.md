# Tunnel de Vente & Espace Client KORYXA
## Produit : « Créer et livrer son premier assistant IA » (11 000 F CFA)

Ce dossier contient l'implémentation complète, sécurisée et autonome du tunnel de vente, de la passerelle de paiement **KORYXA Pay**, de l'espace client avec onboarding guidé en 6 étapes et de l'assistant de support IA Cohere RAG.

---

## 1. Démarrage Rapide

### Prérequis
- Python 3.10+
- Dépendances Python installées :
  ```bash
  pip install fastapi uvicorn pydantic sqlalchemy httpx
  ```

### Lancement de l'application
Depuis la racine du dossier du projet :
```bash
python tunnel/run.py
```
L'application démarre immédiatement sur : **`http://localhost:8000`**

---

## 2. Écrans Disponibles

- **Page de vente** : `http://localhost:8000/`  
  Présentation de l'offre (11 000 F CFA), extrait gratuit téléchargeable, lecteur de démo (650€ &rarr; 700€), contenu du pack et formulaire de commande.
- **Suivi paiement** : `http://localhost:8000/commande/statut?order_id=...`  
  Écoute le statut du paiement et permet la validation en un clic en mode simulation.
- **Espace client** : `http://localhost:8000/espace-client?email=...&order_id=...`  
  Accès aux téléchargements sécurisés (Livre PDF 68p + Pack Code Zip), checklist des 6 étapes d'onboarding, et chat support IA Cohere RAG.
- **Cockpit Admin** : `http://localhost:8000/admin`  
  Suivi des ventes, conversion, téléchargements et tickets de support (Jeton par défaut : `koryxa_admin_secret_token_18nov2026`).

---

## 3. Spécification KORYXA Payment Implémentée

- **API Officielle** : `https://api-pay.koryxa.fr`
- **En-têtes** : `X-Project-Code`, `X-Project-Key`
- **Montant** : `11000` (`amount_minor`), Devise : `XOF`
- **Contrôle Webhook** :
  - Signature HMAC-SHA256 avec `whsec_...`
  - Fraîcheur du timestamp $\le$ 300 secondes
  - Relecture serveur de sécurité : `GET /v1/client/payments/{payment_id}`
  - Idempotence stricte : aucune double commande ni double e-mail.

---

## 4. Exécution des Tests Automatisés

Pour lancer la suite de 7 tests de recette :
```bash
python tunnel/run_tests.py
```
Tous les tests sont au vert (`OK`).

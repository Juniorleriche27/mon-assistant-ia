# Guide de Déploiement : Vercel (Frontend) & Netcup (Backend)
## Domaine retenu : `mon-assistant.koryxa.fr`

---

## 1. Déploiement du Frontend sur Vercel (`mon-assistant.koryxa.fr`)

Le dossier `tunnel/frontend` est prêt pour le déploiement sur Vercel avec le fichier [vercel.json](file:///C:/KORYXA%20%E2%80%94%20Mon%20premier%20assistant%20IA/tunnel/frontend/vercel.json).

### Étapes :
1. Déployer le dossier `tunnel/frontend` :
   ```bash
   cd "C:\KORYXA — Mon premier assistant IA\tunnel\frontend"
   npx vercel --prod
   # Ou lier le dépôt Git à Vercel en définissant le root directory sur "tunnel/frontend"
   ```
2. Dans le tableau de bord Vercel (Settings &rarr; Domains) :
   - Ajoutez le domaine : **`mon-assistant.koryxa.fr`**
   - Ajoutez l'enregistrement CNAME indiqué par Vercel chez votre registrar DNS (ex: `cname.vercel-dns.com`).

---

## 2. Déploiement du Backend sur votre serveur Netcup (`api-mon-assistant.koryxa.fr`)

Le backend FastAPI tourne avec Docker Compose et Caddy pour la gestion automatique du certificat HTTPS Let's Encrypt.

### Étapes sur le serveur Netcup :
1. **Enregistrement DNS (Type A)** chez votre registrar :
   - Hôte : **`api-mon-assistant.koryxa.fr`**
   - Valeur : `IP_DE_VOTRE_SERVEUR_NETCUP`

2. **Transférer le dossier `tunnel/` sur Netcup** (via SCP ou Git) :
   ```bash
   scp -r tunnel/ root@IP_NETCUP:/opt/koryxa-mon-assistant
   ```

3. **Créer le fichier `.env` sur le serveur Netcup** :
   ```bash
   cd /opt/koryxa-mon-assistant
   cp .env.example .env
   nano .env
   ```
   Remplir avec vos identifiants réels :
   ```dotenv
   KORYXA_PAY_BASE_URL=https://api-pay.koryxa.fr
   KORYXA_PAY_PROJECT_CODE=votre_code_projet_ici
   KORYXA_PAY_PROJECT_KEY=kpx_votre_cle_koryxa_pay_ici
   KORYXA_WEBHOOK_SECRET=whsec_votre_secret_webhook_ici
   COHERE_API_KEY=votre_cle_cohere_ici
   ADMIN_SECRET_TOKEN=un_token_secret_admin_robuste
   FRONTEND_URL=https://mon-assistant.koryxa.fr
   ```

4. **Lancer les conteneurs Docker** :
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
   Caddy va automatiquement générer et renouveler le certificat SSL pour `https://api-mon-assistant.koryxa.fr`.

---

## 3. Configuration sur l'Espace Marchand KORYXA Payment (`pay.koryxa.fr`)

Dans votre projet KORYXA Pay (onglet Développeurs / Projets) :
1. **URL de Webhook** :
   ```text
   https://api-mon-assistant.koryxa.fr/api/v1/webhook/koryxa
   ```
2. **Origines autorisées** :
   ```text
   https://mon-assistant.koryxa.fr
   ```
3. **URL de retour client** :
   ```text
   https://mon-assistant.koryxa.fr/commande/statut
   ```

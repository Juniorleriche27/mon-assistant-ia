#!/usr/bin/env bash
set -e

echo "=== 1. Fix Permissions ==="
chmod -R 755 /opt/apps/mon-assistant-ia

echo "=== 2. Create compose.yml ==="
cat << 'EOF' > /opt/apps/mon-assistant-ia/compose.yml
name: mon-assistant-ia
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    image: mon-assistant-api:local
    container_name: prod_mon_assistant_api
    restart: unless-stopped
    init: true
    env_file:
      - /opt/env/mon-assistant-ia.env
    volumes:
      - mon_assistant_data:/app/data
      - ./storage:/app/storage:ro
      - ./Manuscrit_Complet_Assistant_IA_RAG.md:/app/Manuscrit_Complet_Assistant_IA_RAG.md:ro
      - ./KORYXA_Assistant_IA_Extrait.pdf:/app/KORYXA_Assistant_IA_Extrait.pdf:ro
    networks:
      - public
    ports:
      - "127.0.0.1:18140:8000"
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request,sys; resp=urllib.request.urlopen('http://127.0.0.1:8000/health',timeout=3); sys.exit(0 if resp.status==200 and b'healthy' in resp.read() else 1)"]
      interval: 20s
      timeout: 5s
      retries: 5
      start_period: 20s
    security_opt:
      - no-new-privileges:true
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  mon_assistant_data:
    name: mon_assistant_backend_data

networks:
  public:
    external: true
    name: prod_public
EOF

echo "=== 3. Prepare /opt/env/mon-assistant-ia.env ==="
COHERE_VAL=$(grep "^COHERE_API_KEY=" /opt/env/knowlia.env 2>/dev/null | cut -d"=" -f2- | tr -d "\"'")
cat << EOF > /opt/env/mon-assistant-ia.env
# Configuration KORYXA Tunnel - Mon Premier Assistant IA
KORYXA_PAY_BASE_URL=https://api-pay.koryxa.fr
KORYXA_PAY_PROJECT_CODE=koryxa-formation
KORYXA_PAY_PROJECT_KEY=
KORYXA_WEBHOOK_SECRET=
COHERE_API_KEY=${COHERE_VAL}
COHERE_MODEL=command-r-08-2024
DATABASE_URL=sqlite:////app/data/koryxa_tunnel.db
ADMIN_SECRET_TOKEN=koryxa_admin_secret_token_18nov2026
FRONTEND_URL=https://mon-assistant.koryxa.fr
STORAGE_DIR=/app/storage
EOF

chmod 600 /opt/env/mon-assistant-ia.env
chown deploy:deploy /opt/env/mon-assistant-ia.env /opt/apps/mon-assistant-ia/compose.yml

echo "SETUP_DONE"

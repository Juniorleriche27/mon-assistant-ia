#!/usr/bin/env bash
set -e

CADDYFILE="/opt/proxy/caddy/Caddyfile"
BACKUP="/opt/proxy/caddy/Caddyfile.bak-$(date +%Y%m%d%H%M%S)"

# Vérifier si déjà configuré
if grep -q "api-mon-assistant.koryxa.fr" "$CADDYFILE"; then
    echo "api-mon-assistant.koryxa.fr déjà présent dans Caddyfile."
    exit 0
fi

# Backup
cp "$CADDYFILE" "$BACKUP"
echo "Backup créé : $BACKUP"

# Ajout du bloc de configuration
cat << 'EOF' >> "$CADDYFILE"

api-mon-assistant.koryxa.fr {
    encode gzip

    reverse_proxy prod_mon_assistant_api:8000

    header {
        -Server
        X-Content-Type-Options nosniff
        X-Frame-Options DENY
        Referrer-Policy no-referrer
    }
}
EOF

# Validation Caddy
docker exec prod_caddy caddy validate --config /etc/caddy/Caddyfile
echo "Configuration validée."

# Rechargement à chaud
docker exec prod_caddy caddy reload --config /etc/caddy/Caddyfile
echo "Caddy rechargé avec succès."

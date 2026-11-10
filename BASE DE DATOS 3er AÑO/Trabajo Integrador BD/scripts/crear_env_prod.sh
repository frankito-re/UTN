#!/usr/bin/env bash
# Genera .env.prod con claves aleatorias fuertes (no sobrescribe uno existente).
#   DOMINIO=app.midominio.com ACME_EMAIL=yo@correo.com scripts/crear_env_prod.sh
set -euo pipefail
cd "$(dirname "$0")/.."
[ -e .env.prod ] && { echo ".env.prod ya existe: no se sobrescribe."; exit 0; }
umask 077
gen() { openssl rand -base64 33 | tr -d '/+=' | cut -c1-32; }
cat > .env.prod <<ENV
POSTGRES_DB=bodegas_atuel
POSTGRES_USER=bodegas_owner
POSTGRES_PASSWORD=$(gen)
API_DB_PASSWORD=$(gen)
RO_DB_PASSWORD=$(gen)
DOMINIO=${DOMINIO:-localhost}
ACME_EMAIL=${ACME_EMAIL:-admin@example.com}
HTTP_PORT=${HTTP_PORT:-80}
HTTPS_PORT=${HTTPS_PORT:-443}
ENV
echo ".env.prod creado (permisos 600). Guardalo en un gestor de secretos: NO se versiona."

#!/usr/bin/env bash
# Backup de una base REMOTA (Supabase u otra) por su cadena de conexion, sin instalar Postgres en tu maquina:
# usa el cliente pg_dump de la imagen postgres:17 (un cliente nuevo puede volcar servidores mas viejos).
#   scripts/backup_remoto.sh [directorio_destino]
# La URL sale de $BACKUP_URL o de SUPABASE_DB_URL en .env.supabase (nunca se pasa por la linea de comandos).
# Formato: SQL plano comprimido del esquema public (+ SHA-256; AES-256 si se define BACKUP_CLAVE). El SQL plano
# se restaura en cualquier version de Postgres (pg_restore exige la misma version o mayor que el servidor de origen).
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -z "${BACKUP_URL:-}" ]; then
  [ -f "$RAIZ/.env.supabase" ] || { echo "Defina BACKUP_URL o cree .env.supabase" >&2; exit 1; }
  BACKUP_URL="$(grep -E '^SUPABASE_DB_URL=' "$RAIZ/.env.supabase" | head -1 | cut -d= -f2-)"
fi
export BACKUP_URL
DESTINO="${1:-$RAIZ/backups}"; mkdir -p "$DESTINO"; chmod 700 "$DESTINO"; umask 077
ARCHIVO="$DESTINO/remoto_$(date +%Y%m%d_%H%M%S).sql.gz"
echo "Backup remoto -> $ARCHIVO"
docker run --rm -e BACKUP_URL postgres:17-alpine sh -c 'pg_dump "$BACKUP_URL" -n public --no-owner --no-comments -Fp' | gzip -6 > "$ARCHIVO"
[ -s "$ARCHIVO" ] && gzip -t "$ARCHIVO" || { echo "El backup salio vacio o corrupto" >&2; rm -f "$ARCHIVO"; exit 1; }
if [ -n "${BACKUP_CLAVE:-}" ]; then
  openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -pass env:BACKUP_CLAVE -in "$ARCHIVO" -out "$ARCHIVO.enc"; rm -f "$ARCHIVO"; ARCHIVO="$ARCHIVO.enc"
  echo "Cifrado con AES-256."
fi
if command -v sha256sum >/dev/null; then H=$(sha256sum "$ARCHIVO" | cut -d' ' -f1); else H=$(shasum -a 256 "$ARCHIVO" | cut -d' ' -f1); fi
echo "$H  $(basename "$ARCHIVO")" > "$ARCHIVO.sha256"
echo "Listo: $(basename "$ARCHIVO") · $(du -h "$ARCHIVO" | cut -f1)"
echo "$ARCHIVO" > "$DESTINO/ultimo_backup.txt"

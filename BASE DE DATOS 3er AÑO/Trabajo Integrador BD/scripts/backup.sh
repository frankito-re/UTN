#!/usr/bin/env bash
# Backup logico de la base: pg_dump formato custom (comprimido) + SHA-256 + rotacion.
#   ENTORNO=prod scripts/backup.sh [directorio_destino]
# Cifrado opcional (AES-256): exportar BACKUP_CLAVE=...  -> genera .dump.enc y borra el .dump en claro.
# Retencion: BACKUP_RETENCION_DIAS (por defecto 14).
# Programarlo: ver docs/despliegue_nube.md (cron diario + copia FUERA del servidor).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib_entorno.sh"
DESTINO="${1:-$RAIZ/backups}"
RETENCION="${BACKUP_RETENCION_DIAS:-14}"
mkdir -p "$DESTINO"; chmod 700 "$DESTINO"
umask 077
SELLO="$(date +%Y%m%d_%H%M%S)"
ARCHIVO="$DESTINO/${PGBASE}_${SELLO}.dump"

echo "Backup de '$PGBASE' ($ENTORNO) -> $ARCHIVO"
docker exec "$CONTENEDOR_DB" pg_dump -U "$PGUSUARIO" -d "$PGBASE" -Fc -Z 6 > "$ARCHIVO"
[ -s "$ARCHIVO" ] || { echo "El backup salio vacio" >&2; rm -f "$ARCHIVO"; exit 1; }

if [ -n "${BACKUP_CLAVE:-}" ]; then
  openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -pass env:BACKUP_CLAVE -in "$ARCHIVO" -out "$ARCHIVO.enc"
  rm -f "$ARCHIVO"; ARCHIVO="$ARCHIVO.enc"
  echo "Cifrado con AES-256 (la clave NO se guarda junto al archivo)."
fi
echo "$(sha "$ARCHIVO")  $(basename "$ARCHIVO")" > "$ARCHIVO.sha256"
echo "Listo: $(basename "$ARCHIVO") · $(du -h "$ARCHIVO" | cut -f1) · sha256 $(cut -c1-16 "$ARCHIVO.sha256")…"

# Rotacion: borra backups (y sus sumas) mas viejos que la retencion
find "$DESTINO" -maxdepth 1 -type f \( -name "${PGBASE}_*.dump" -o -name "${PGBASE}_*.dump.enc" -o -name "${PGBASE}_*.sha256" \) \
  -mtime "+$RETENCION" -print -delete | sed 's/^/Rotado: /' || true
echo "$ARCHIVO" > "$DESTINO/ultimo_backup.txt"

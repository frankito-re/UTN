#!/usr/bin/env bash
# Restaura un backup en una base NUEVA (nunca pisa la de produccion sin --forzar).
#   ENTORNO=prod scripts/restore.sh backups/bodegas_atuel_YYYYmmdd_HHMMSS.dump[.enc] [base_destino] [--forzar]
# - Verifica la suma SHA-256 y descifra si hace falta (BACKUP_CLAVE).
# - Crea los roles si no existen (servidor nuevo) y les pone clave desde el .env (API_DB_PASSWORD / RO_DB_PASSWORD).
# - Reaplica lo que pg_dump NO guarda: privilegio CONNECT y random_page_cost de la base.
# Recuperacion ante desastre (reemplazar produccion): detener la API, `restore.sh archivo bodegas_atuel --forzar`,
# levantar la API.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib_entorno.sh"
ARCHIVO="${1:?uso: restore.sh archivo [base_destino] [--forzar]}"; shift
DESTINO_BD=""; FORZAR=0
for a in "$@"; do [ "$a" = "--forzar" ] && FORZAR=1 || DESTINO_BD="$a"; done
DESTINO_BD="${DESTINO_BD:-${PGBASE}_restauracion}"
[ -f "$ARCHIVO" ] || { echo "No existe $ARCHIVO" >&2; exit 1; }

if [ -f "$ARCHIVO.sha256" ]; then
  esperado="$(cut -d' ' -f1 "$ARCHIVO.sha256")"
  [ "$(sha "$ARCHIVO")" = "$esperado" ] && echo "SHA-256 correcto." || { echo "SHA-256 NO coincide: el archivo esta alterado o corrupto." >&2; exit 1; }
else
  echo "AVISO: no hay archivo .sha256; no se pudo verificar la integridad." >&2
fi
FUENTE="$ARCHIVO"; TEMPORAL=""
if [[ "$ARCHIVO" == *.enc ]]; then
  : "${BACKUP_CLAVE:?este backup esta cifrado: exportar BACKUP_CLAVE}"
  TEMPORAL="$(mktemp)"; trap 'rm -f "$TEMPORAL"' EXIT
  openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -pass env:BACKUP_CLAVE -in "$ARCHIVO" -out "$TEMPORAL"
  FUENTE="$TEMPORAL"
fi

# Roles (en un servidor nuevo no existen; pg_dump no los incluye)
psql_db -d postgres <<SQL
DO \$\$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='bodegas_api') THEN
    CREATE ROLE bodegas_api LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION CONNECTION LIMIT 20; END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='bodegas_ro') THEN
    CREATE ROLE bodegas_ro LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION CONNECTION LIMIT 10; END IF;
END \$\$;
SQL
for par in "bodegas_api:API_DB_PASSWORD" "bodegas_ro:RO_DB_PASSWORD"; do
  rol="${par%%:*}"; var="${par##*:}"; clave="$(leer_env "$var")"
  [ -n "$clave" ] && psql_db -d postgres -v pw="$clave" <<< "ALTER ROLE $rol PASSWORD :'pw';"
done

if [ "$FORZAR" = 1 ]; then
  echo "--forzar: se elimina la base '$DESTINO_BD' si existe."
  psql_db -d postgres -c "DROP DATABASE IF EXISTS \"$DESTINO_BD\" WITH (FORCE)"
fi
psql_db -d postgres -c "CREATE DATABASE \"$DESTINO_BD\" OWNER \"$PGUSUARIO\"" \
  || { echo "La base '$DESTINO_BD' ya existe: use otro nombre o --forzar." >&2; exit 1; }

echo "Restaurando en '$DESTINO_BD'..."
docker exec -i "$CONTENEDOR_DB" pg_restore -U "$PGUSUARIO" -d "$DESTINO_BD" --no-owner --exit-on-error < "$FUENTE"

psql_db -d postgres <<SQL
REVOKE ALL ON DATABASE "$DESTINO_BD" FROM PUBLIC;
GRANT CONNECT ON DATABASE "$DESTINO_BD" TO bodegas_api, bodegas_ro;
ALTER DATABASE "$DESTINO_BD" SET random_page_cost = 1.1;
SQL
echo "Restauracion completa en '$DESTINO_BD'."

#!/bin/bash
# =============================================================================
# 090_roles_passwords.sh · Asigna las claves de bodegas_api y bodegas_ro.
# Las claves vienen de variables de entorno (archivo .env, fuera de git); asi no
# hay ninguna clave escrita en el repositorio. Corre despues de 007_roles.sql,
# solo la primera vez que se crea el volumen (igual que los .sql).
# Si una variable esta vacia, el rol queda SIN clave y no puede iniciar sesion
# por red hasta que se la asignes con ALTER ROLE.
# =============================================================================
set -e

asignar() {   # $1 = rol, $2 = clave
  if [ -z "$2" ]; then
    echo "AVISO: sin clave para el rol $1 (definila en .env y recrea el volumen, o usa ALTER ROLE)" >&2
    return 0
  fi
  # La clave viaja como variable de psql (:'pw'), nunca concatenada en el SQL.
  psql -v ON_ERROR_STOP=1 -v pw="$2" --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<SQL
ALTER ROLE $1 PASSWORD :'pw';
SQL
}

asignar bodegas_api "${API_DB_PASSWORD:-}"
asignar bodegas_ro  "${RO_DB_PASSWORD:-}"

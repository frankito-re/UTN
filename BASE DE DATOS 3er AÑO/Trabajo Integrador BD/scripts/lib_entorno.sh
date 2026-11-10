# Funciones comunes de los scripts de backup/restauracion. Se incluye con `source`.
#   ENTORNO=dev  (por defecto)  -> contenedor del docker-compose.yml, variables de .env
#   ENTORNO=prod                -> docker-compose.prod.yml, variables de .env.prod
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENTORNO="${ENTORNO:-dev}"
if [ "$ENTORNO" = prod ]; then
  ARCHIVO_ENV="$RAIZ/.env.prod"
  COMPOSE=(docker compose --env-file "$ARCHIVO_ENV" -f "$RAIZ/docker-compose.prod.yml")
  CONTENEDOR_DB="$("${COMPOSE[@]}" ps -q db)"
else
  ARCHIVO_ENV="$RAIZ/.env"
  CONTENEDOR_DB="${CONTENEDOR_DB:-bodegas_atuel_postgres}"
fi
[ -f "$ARCHIVO_ENV" ] || { echo "No existe $ARCHIVO_ENV" >&2; exit 1; }
[ -n "$CONTENEDOR_DB" ] || { echo "No se encontro el contenedor de la base (¿esta levantado?)" >&2; exit 1; }
leer_env() { grep -E "^$1=" "$ARCHIVO_ENV" | head -1 | cut -d= -f2-; }
PGUSUARIO="$(leer_env POSTGRES_USER)"; PGBASE="$(leer_env POSTGRES_DB)"
# psql/pg_dump dentro del contenedor por el socket local (el propietario no entra por red).
psql_db()   { docker exec -i "$CONTENEDOR_DB" psql -U "$PGUSUARIO" -v ON_ERROR_STOP=1 -X -q "$@"; }
sha() { if command -v sha256sum >/dev/null; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }

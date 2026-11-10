#!/usr/bin/env bash
# Verifica la seguridad del despliegue de PRODUCCION en marcha (docker-compose.prod.yml).
#   scripts/verificar_despliegue.sh [url_https]        (por defecto https://localhost:${HTTPS_PORT})
# Cada control imprime ok/FALLO; termina con codigo != 0 si algo falla.
set -uo pipefail
export ENTORNO=prod
source "$(dirname "${BASH_SOURCE[0]}")/lib_entorno.sh"
HTTPS_PORT="$(leer_env HTTPS_PORT)"; HTTP_PORT="$(leer_env HTTP_PORT)"
URL="${1:-https://localhost:${HTTPS_PORT:-443}}"
CLAVE_API="$(leer_env API_DB_PASSWORD)"; CLAVE_OWNER="$(leer_env POSTGRES_PASSWORD)"
FALLOS=0
ok()  { echo "  ok    $1"; }
mal() { echo "  FALLO $1"; FALLOS=$((FALLOS+1)); }
cond() { if eval "$2"; then ok "$1"; else mal "$1"; fi; }
sql_tcp() {  # $1 usuario, $2 clave, $3 sslmode, resto: consulta
  local u="$1" c="$2" m="$3"; shift 3
  docker exec -e PGPASSWORD="$c" -e PGCONNECT_TIMEOUT=5 "$CONTENEDOR_DB" psql "host=127.0.0.1 user=$u dbname=$PGBASE sslmode=$m" -At -c "$*" 2>&1
}
srv() { "${COMPOSE[@]}" ps -q "$1"; }

echo "== Exposicion de red"
for s in db api front; do
  cond "$s no publica ningun puerto en el host" '[ -z "$(docker port "$(srv '"$s"')" 2>/dev/null)" ]'
done
cond "el proxy publica solo 80 y 443 (internos)" '[ "$(docker port "$(srv proxy)" | cut -d/ -f1 | sort -u | tr "\n" " ")" = "443 80 " ]'
cond "nada escucha en el puerto 5432 del host (la base de produccion no se expone)" '! (exec 3<>/dev/tcp/127.0.0.1/5432) 2>/dev/null'
cond "la API no es alcanzable directamente (8000)" '! curl -s --max-time 2 http://localhost:8000/health >/dev/null 2>&1 || ! docker port "$(srv api)" | grep -q 8000'
cond "las redes internas no tienen salida a internet (la API no llega a example.com)" \
  '! docker exec "$(srv api)" python -c "import urllib.request; urllib.request.urlopen(\"https://example.com\", timeout=4)" >/dev/null 2>&1'

echo "== HTTPS"
cond "HTTPS responde y la API contesta por /api/health" 'curl -sk --max-time 5 "$URL/api/health" | grep -q "\"estado\":\"ok\""'
cond "HTTP redirige a HTTPS (308)" '[ "$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "http://localhost:${HTTP_PORT:-80}/")" = 308 ]'
cond "HSTS activo" 'curl -skI --max-time 5 "$URL/" | grep -qi "^strict-transport-security: max-age=31536000"'
cond "CSP estricta, nosniff y X-Frame-Options llegan al navegador" \
  'H="$(curl -skI --max-time 5 "$URL/")"; grep -qi "^content-security-policy: default-src .self." <<<"$H" && grep -qi "^x-content-type-options: nosniff" <<<"$H" && grep -qi "^x-frame-options: DENY" <<<"$H"'
cond "no se anuncia la version del servidor (sin cabecera Server)" '! curl -skI --max-time 5 "$URL/" | grep -qi "^server:"'
cond "TLS 1.0/1.1 rechazados (el proxy exige TLS >= 1.2)" '! curl -sk --max-time 5 --tls-max 1.1 "$URL/" >/dev/null 2>&1'
cond "la CSP no permite scripts de terceros (no hay 'unsafe-inline' ni 'unsafe-eval')" '! curl -skI "$URL/" | grep -i "^content-security-policy" | grep -qE "unsafe-(inline|eval)"'

echo "== Base de datos"
r=$(sql_tcp bodegas_api "$CLAVE_API" disable "SELECT 1"); cond "conexion SIN TLS rechazada" '[[ "$r" == *"no pg_hba.conf entry"* || "$r" == *"rejected"* || "$r" == *"FATAL"* ]]'
r=$(sql_tcp bodegas_api "$CLAVE_API" require "SELECT current_user"); cond "conexion con TLS y clave correcta aceptada (bodegas_api)" '[ "$r" = bodegas_api ]'
r=$(sql_tcp bodegas_api "clave-incorrecta" require "SELECT 1"); cond "clave incorrecta rechazada" '[[ "$r" == *"password authentication failed"* ]]'
r=$(sql_tcp bodegas_owner "$CLAVE_OWNER" require "SELECT 1"); cond "el propietario NO puede entrar por red aunque tenga la clave" '[[ "$r" == *"no pg_hba.conf entry"* || "$r" == *"FATAL"* ]]'
r=$(sql_tcp bodegas_api "$CLAVE_API" require "SELECT rolsuper OR rolcreaterole OR rolcreatedb FROM pg_roles WHERE rolname=current_user"); cond "bodegas_api no es superusuario ni crea roles/bases" '[ "$r" = f ]'
r=$(docker exec "$CONTENEDOR_DB" psql -U "$PGUSUARIO" -d "$PGBASE" -At -c "SELECT count(*) FILTER (WHERE s.ssl), count(*) FROM pg_stat_activity a JOIN pg_stat_ssl s USING (pid) WHERE a.application_name = 'bodegas-api'")
cond "todas las conexiones de la API a la base van cifradas ($r = cifradas|total)" '[ "${r%%|*}" = "${r##*|}" ] && [ "${r##*|}" -ge 1 ]'
r=$(docker exec "$CONTENEDOR_DB" psql -U "$PGUSUARIO" -d "$PGBASE" -At -c "SELECT string_agg(DISTINCT s.version, ',') FROM pg_stat_ssl s JOIN pg_stat_activity a USING (pid) WHERE a.application_name = 'bodegas-api'")
cond "version de TLS de la API a la base: $r (>= 1.2)" '[[ "$r" == *TLSv1.3* || "$r" == *TLSv1.2* ]]'
r=$(docker exec "$CONTENEDOR_DB" psql -U "$PGUSUARIO" -d "$PGBASE" -At -c "SHOW password_encryption")
cond "las claves se guardan con SCRAM-SHA-256 ($r)" '[ "$r" = scram-sha-256 ]'

echo "== Contenedores y secretos"
cond "la API corre sin root" '[ "$(docker exec "$(srv api)" id -u)" != 0 ]'
cond "la API tiene el sistema de archivos de solo lectura" '[ "$(docker inspect -f "{{.HostConfig.ReadonlyRootfs}}" "$(srv api)")" = true ]'
cond "la API no tiene capacidades de Linux (cap_drop ALL)" 'docker inspect -f "{{.HostConfig.CapDrop}}" "$(srv api)" | grep -qi all'
cond "la API no puede escalar privilegios (no-new-privileges)" 'docker inspect -f "{{.HostConfig.SecurityOpt}}" "$(srv api)" | grep -q no-new-privileges'
cond "ningun secreto de .env/.env.prod esta en archivos versionados" '
  ok_=1; for v in POSTGRES_PASSWORD API_DB_PASSWORD RO_DB_PASSWORD; do
    for f in "$RAIZ/.env" "$RAIZ/.env.prod"; do val="$(grep -E "^$v=" "$f" 2>/dev/null | cut -d= -f2-)"; [ -n "$val" ] && git -C "$RAIZ" grep -qF -- "$val" && ok_=0; done; done; [ $ok_ = 1 ]'
cond ".env, .env.prod, certs/ y backups/ estan ignorados por git" 'for f in .env .env.prod certs/ca/ca.key certs/db/server.key backups/x.dump; do git -C "$RAIZ" check-ignore -q "$f" || exit 1; done'
cond "la clave privada de la CA no esta montada en ningun contenedor" '! docker inspect "$(srv db)" "$(srv api)" "$(srv proxy)" | grep -q "ca.key"'

echo
[ "$FALLOS" = 0 ] && echo "DESPLIEGUE VERIFICADO: todos los controles pasan" || { echo "$FALLOS CONTROL(ES) FALLARON"; exit 1; }

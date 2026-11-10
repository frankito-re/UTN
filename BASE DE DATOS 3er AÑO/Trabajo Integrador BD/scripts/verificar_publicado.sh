#!/usr/bin/env bash
# Controles de SOLO LECTURA sobre el sistema publicado (no modifica datos):
#   scripts/verificar_publicado.sh https://bodegas-del-atuel.onrender.com
set -uo pipefail
URL="${1:?uso: verificar_publicado.sh https://url-publica}"; URL="${URL%/}"
FALLOS=0
ok()   { echo "  ok    $1"; }
mal()  { echo "  FALLO $1"; FALLOS=$((FALLOS+1)); }
cond() { if eval "$2"; then ok "$1"; else mal "$1"; fi; }
H="$(curl -sSI --max-time 60 "$URL/")" || { echo "No responde $URL (si es un plan gratuito puede estar despertando: reintentar en 1 minuto)"; exit 1; }
echo "== HTTPS y cabeceras"
cond "responde por HTTPS con certificado valido" 'curl -sS --max-time 30 -o /dev/null "$URL/"'
[[ "$URL" == https://* ]] && cond "HTTP redirige a HTTPS" '[[ "$(curl -s -o /dev/null -w "%{http_code} %{redirect_url}" --max-time 30 "http://${URL#https://}/")" == 30[1278]\ https://* ]]'
[[ "$URL" == https://* ]] || echo "  (URL sin https: se omiten los controles de redireccion y de TLS; solo para pruebas locales)"
cond "HSTS" 'grep -qi "^strict-transport-security: max-age=31536000" <<<"$H"'
cond "CSP estricta sin unsafe-inline" 'C="$(grep -i "^content-security-policy" <<<"$H")"; [ -n "$C" ] && ! grep -qE "unsafe-(inline|eval)" <<<"$C"'
cond "nosniff y X-Frame-Options" 'grep -qi "^x-content-type-options: nosniff" <<<"$H" && grep -qi "^x-frame-options: DENY" <<<"$H"'
[[ "$URL" == https://* ]] && cond "TLS 1.0/1.1 rechazados" '! curl -s --max-time 20 --tls-max 1.1 -o /dev/null "$URL/" 2>/dev/null'
echo "== Aplicacion"
cond "el front carga (index.html y modulos JS)" 'curl -sf --max-time 30 "$URL/" | grep -q "Bodegas del Atuel" && curl -sf --max-time 30 "$URL/js/app.js" >/dev/null'
cond "la API responde y llega a la base (/api/health)" 'curl -sf --max-time 30 "$URL/api/health" | grep -q "\"base\":\"ok\""'
cond "el catalogo devuelve datos (/api/vinos)" 'curl -sf --max-time 30 "$URL/api/vinos?page_size=1" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d[\"total\"]>0 else 1)"'
cond "Swagger UI y contrato OpenAPI publicados" 'curl -sf --max-time 30 "$URL/api/docs" >/dev/null && curl -sf --max-time 30 "$URL/api/openapi.json" | grep -q "\"/comprobantes\""'
echo "== Seguridad de la API"
cond "inyeccion SQL en un filtro: texto inerte (200 y 0 resultados)" '[ "$(curl -s --max-time 30 -G "$URL/api/vinos" --data-urlencode "q=x'"'"'; DROP TABLE vino; --" | python3 -c "import sys,json; print(json.load(sys.stdin)[\"total\"])")" = 0 ]'
cond "inyeccion en el ORDER BY rechazada (400)" '[ "$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 -G "$URL/api/vinos" --data-urlencode "orden=precio; DROP TABLE vino")" = 400 ]'
cond "la tabla sigue existiendo despues de los ataques" 'curl -sf --max-time 30 "$URL/api/vinos?page_size=1" >/dev/null'
cond "no se filtran detalles internos en los errores (404 limpio)" '[ "$(curl -s --max-time 30 "$URL/api/vinos/999999999" | python3 -c "import sys,json; e=json.load(sys.stdin)[\"error\"]; print(e[\"estado\"], \"sql\" in str(e).lower())")" = "404 False" ]'
echo; [ "$FALLOS" = 0 ] && echo "PUBLICACION VERIFICADA" || { echo "$FALLOS CONTROL(ES) FALLARON"; exit 1; }

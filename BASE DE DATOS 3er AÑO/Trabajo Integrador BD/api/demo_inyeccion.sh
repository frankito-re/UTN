#!/usr/bin/env bash
# =============================================================================
# Demostracion de inyeccion SQL FALLIDA contra la API en marcha (docker compose up -d).
#   bash api/demo_inyeccion.sh            (API en http://localhost:8000)
# Cada ataque se envia de verdad; despues se cuentan las filas para probar que no
# se borro ni se filtro nada. Por que falla: todo valor del usuario viaja como
# parametro (%s) y el ORDER BY sale de una lista blanca (api/app/routers/vinos.py).
# =============================================================================
API="${API:-http://localhost:8000}"
CONT="${CONTENEDOR:-bodegas_atuel_postgres}"
contar() { docker exec "$CONT" sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SELECT (SELECT count(*) FROM vino)||'"'"' vinos, '"'"'||(SELECT count(*) FROM cliente)||'"'"' clientes, '"'"'||(SELECT count(*) FROM comprobante)||'"'"' comprobantes'"'"'"'; }
ataque() {  # $1 = descripcion, resto = argumentos de curl
  local desc="$1"; shift
  local salida; salida=$(curl -s -w '\n%{http_code}' "$@")
  local codigo="${salida##*$'\n'}" cuerpo="${salida%$'\n'*}"
  printf '\n-- %s\n   HTTP %s  %s\n' "$desc" "$codigo" "$(echo "$cuerpo" | cut -c1-150)"
}

echo "Filas ANTES : $(contar)"

ataque "1. Tautologia en un filtro de texto:  q=' OR '1'='1" -G "$API/vinos" --data-urlencode "q=' OR '1'='1"
ataque "2. Sentencia apilada:  q='; DROP TABLE vino; --" -G "$API/vinos" --data-urlencode "q='; DROP TABLE vino; --"
ataque "3. UNION para leer claves de la base:  q=' UNION SELECT usename, passwd ... FROM pg_shadow --" \
       -G "$API/clientes" --data-urlencode "q=' UNION SELECT usename,passwd,1,1,1,1,1,1,1 FROM pg_shadow --"
ataque "4. Inyeccion en el ORDER BY:  orden=precio; DROP TABLE vino" -G "$API/vinos" --data-urlencode "orden=precio; DROP TABLE vino"
ataque "5. Inyeccion en un parametro numerico de la ruta:  /vinos/1;DROP TABLE vino" "$API/vinos/1;DROP%20TABLE%20vino"
ataque "6. Comodin: q=%  (se busca un % literal, no 'todo')" -G "$API/vinos" --data-urlencode "q=%"
ataque "7. En el cuerpo de un alta (queda guardado como TEXTO, sin ejecutarse)" -X POST "$API/clientes" \
       -H 'content-type: application/json' \
       -d '{"nombre_razon_social":"Robert'"'"'); DROP TABLE cliente;--","tipo_doc":"DNI","nro_doc":"INYECCION-'"$RANDOM"'","direccion":"x","cod_postal":"5600","tipo_cliente":"socio"}'

echo
echo "Filas DESPUES: $(contar)   (la unica diferencia esperada es +1 cliente del ataque 7, guardado como dato)"

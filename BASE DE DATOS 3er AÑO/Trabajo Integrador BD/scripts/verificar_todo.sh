#!/usr/bin/env bash
# Verificacion integral DESDE CERO del proyecto (una sola orden, ideal antes de la defensa):
#   scripts/verificar_todo.sh
# Recrea el stack de desarrollo (ATENCION: borra el volumen de la base de desarrollo; los datos se
# regeneran con la semilla), y corre en orden:
#   1. migraciones 001..008 en una base nueva     4. consultas U/I/D/S contra la base cargada
#   2. pruebas SQL (002,003,005,006,007,008)      5. pruebas de la API (pytest) y del front (node --test)
#   3. carga masiva reproducible + coherencia     6. simulacro de backup/restauracion
# Termina con un resumen y codigo != 0 si algo fallo.
set -uo pipefail
cd "$(dirname "$0")/.."
LOG="$(mktemp -d)"; RESUMEN=(); FALLOS=0
paso() {  # $1 = descripcion, resto = comando
  local desc="$1"; shift
  printf '%-62s' "$desc"
  if "$@" > "$LOG/$(echo "$desc" | tr -c 'A-Za-z0-9' '_').log" 2>&1; then echo "OK"; RESUMEN+=("OK    $desc")
  else echo "FALLO  (ver $LOG)"; RESUMEN+=("FALLO $desc"); FALLOS=$((FALLOS+1)); fi
}
psql_() { docker exec -i bodegas_atuel_postgres sh -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1 -X -q'; }
suite() { psql_ < "db/tests/$1.sql" 2>&1 | tee /dev/stderr | grep -q "OK:"; }

echo "== Entorno"
[ -x .venv/bin/python ] || { python3 -m venv .venv && .venv/bin/pip install -q -r api/requirements-dev.txt -r db/seed/requirements.txt; }
[ -f .env ] || { echo "Falta .env (copiar .env.example y completar claves)"; exit 1; }
paso "Recrear base, API y front desde cero (docker compose)" bash -c 'docker compose down -v && docker compose up -d --build'
paso "Base lista con las migraciones aplicadas" bash -c 'for i in $(seq 1 60); do docker exec bodegas_atuel_postgres sh -c "psql -U \$POSTGRES_USER -d \$POSTGRES_DB -tAc \"select to_regclass('"'"'idx_empleado_sala'"'"')\"" 2>/dev/null | grep -q idx_ && exit 0; sleep 2; done; exit 1'

echo "== Pruebas SQL (base vacia)"
for s in 002_constraints_test 003_funciones_test 005_reglas_test 006_vistas_test 007_roles_test 008_indices_test; do
  paso "SQL: $s" suite "$s"; done

echo "== Carga masiva"
paso "Carga reproducible (500 mil renglones) + 8 verificaciones" .venv/bin/python db/seed/cargar_datos.py --limpiar --fecha-ref hoy --reporte ""

echo "== Consultas, concurrencia y aplicaciones"
paso "Consultas U1-U6, I1-I6, D1-D6, S1-S12" bash db/tests/consultas_test.sh
paso "Demo de concurrencia (RN-09, FOR UPDATE)" bash -c 'bash db/tests/concurrencia_demo.sh | grep -q "stock restante en la sala | 2" || bash db/tests/concurrencia_demo.sh | grep -E "stock restante" | grep -q " 2$"'
for i in $(seq 1 30); do curl -sf localhost:8000/health >/dev/null && break; sleep 2; done
paso "API: 54+ pruebas (pytest, base descartable)" bash -c 'cd api && ../.venv/bin/python -m pytest'
paso "API: inyeccion SQL fallida (demo en vivo)" bash -c 'bash api/demo_inyeccion.sh | grep -q "Filas DESPUES: 600 vinos, 20001 clientes, 160000 comprobantes"'
paso "Front: pruebas (node --test)" node --test "front/test/*.test.mjs"

echo "== Backup"
paso "Simulacro de backup cifrado + restauracion + comparacion" scripts/probar_backup.sh

echo; echo "================ RESUMEN ================"; printf '%s\n' "${RESUMEN[@]}"
[ "$FALLOS" = 0 ] && { echo "TODO VERIFICADO"; exit 0; } || { echo "$FALLOS PASO(S) FALLARON · logs en $LOG"; exit 1; }

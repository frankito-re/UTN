#!/usr/bin/env bash
# SIMULACRO de backup y restauracion: hace un backup cifrado, lo restaura en una base temporal y
# compara contra el original (filas por tabla, huellas de contenido, privilegios, triggers, indices,
# vista materializada, funciones). Borra la base temporal al terminar. Sale con error si algo difiere.
#   ENTORNO=prod scripts/probar_backup.sh
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib_entorno.sh"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
export BACKUP_CLAVE="${BACKUP_CLAVE:-$(openssl rand -hex 16)}"
BD_DRILL="${PGBASE}_simulacro"
FALLOS=0

"$RAIZ/scripts/backup.sh" "$TMP" | sed 's/^/  /'
ARCH="$(cat "$TMP/ultimo_backup.txt")"
echo "-- integridad: un byte alterado debe detectarse"
cp "$ARCH" "$TMP/alterado.enc"; cp "$ARCH.sha256" "$TMP/alterado.enc.sha256"
printf '\x00' | dd of="$TMP/alterado.enc" bs=1 seek=100 conv=notrunc 2>/dev/null
sed -i.bak "s/  .*/  alterado.enc/" "$TMP/alterado.enc.sha256"
if "$RAIZ/scripts/restore.sh" "$TMP/alterado.enc" "${BD_DRILL}_x" >/dev/null 2>&1; then
  echo "  FALLO: se restauro un archivo alterado"; FALLOS=$((FALLOS+1)); psql_db -d postgres -c "DROP DATABASE IF EXISTS \"${BD_DRILL}_x\" WITH (FORCE)"
else echo "  ok: el archivo alterado fue rechazado"; fi

echo "-- restauracion en '$BD_DRILL'"
"$RAIZ/scripts/restore.sh" "$ARCH" "$BD_DRILL" --forzar 2>&1 | sed 's/^/  /'
trap 'rm -rf "$TMP"; psql_db -d postgres -c "DROP DATABASE IF EXISTS \"'"$BD_DRILL"'\" WITH (FORCE)" >/dev/null 2>&1 || true' EXIT

CONTEOS='SELECT format($f$SELECT %L || '"'"'='"'"' || count(*) FROM public.%I$f$, relname, relname) FROM pg_class WHERE relkind = '"'"'r'"'"' AND relnamespace = '"'"'public'"'"'::regnamespace ORDER BY relname \gexec'
HUELLAS="SELECT 'renglon_comprobante='||md5(string_agg(r::text, ',' ORDER BY nro_comprobante, cod_vino)) FROM renglon_comprobante r
UNION ALL SELECT 'cliente='||md5(string_agg(c::text, ',' ORDER BY id_cliente)) FROM cliente c
UNION ALL SELECT 'vino='||md5(string_agg(v::text, ',' ORDER BY cod_vino)) FROM vino v
UNION ALL SELECT 'stock_sala='||md5(string_agg(s::text, ',' ORDER BY id_sala, cod_vino)) FROM stock_sala s"
ESTRUCTURA="SELECT 'indices='||count(*) FROM pg_indexes WHERE schemaname='public'
UNION ALL SELECT 'triggers='||count(*) FROM pg_trigger WHERE NOT tgisinternal
UNION ALL SELECT 'funciones='||count(*) FROM pg_proc WHERE pronamespace='public'::regnamespace
UNION ALL SELECT 'vistas='||count(*) FROM pg_class WHERE relnamespace='public'::regnamespace AND relkind IN ('v','m')
UNION ALL SELECT 'api_inserta_vino='||has_table_privilege('bodegas_api','vino','INSERT')
UNION ALL SELECT 'api_inserta_stock='||has_table_privilege('bodegas_api','stock_sala','INSERT')
UNION ALL SELECT 'ro_inserta_vino='||has_table_privilege('bodegas_ro','vino','INSERT')
UNION ALL SELECT 'ro_lee_vino='||has_table_privilege('bodegas_ro','vino','SELECT')
UNION ALL SELECT 'api_ejecuta_sp='||has_function_privilege('bodegas_api','sp_procesar_ingreso(integer)','EXECUTE')
UNION ALL SELECT 'public_conecta='||has_database_privilege('public', current_database(), 'CONNECT')
UNION ALL SELECT 'total_comprobante_1='||fn_total_comprobante(1)
UNION ALL SELECT 'matview_filas='||count(*) FROM mv_ventas_mensuales_sala"
for consulta in "$CONTEOS" "$HUELLAS" "$ESTRUCTURA"; do
  psql_db -At -d "$PGBASE"     <<< "$consulta" | sort > "$TMP/origen.txt"
  psql_db -At -d "$BD_DRILL"   <<< "$consulta" | sort > "$TMP/copia.txt"
  if diff -q "$TMP/origen.txt" "$TMP/copia.txt" >/dev/null; then echo "  ok: $(wc -l < "$TMP/origen.txt" | tr -d ' ') valores identicos"
  else echo "  FALLO: diferencias entre origen y restauracion:"; diff "$TMP/origen.txt" "$TMP/copia.txt" | sed 's/^/     /'; FALLOS=$((FALLOS+1)); fi
done
echo "-- la base restaurada se puede usar con el rol de la API (clave de .env, por TCP)"
CLAVE_API="$(leer_env API_DB_PASSWORD)"
n=$(docker exec -e PGPASSWORD="$CLAVE_API" -e PGSSLMODE=prefer "$CONTENEDOR_DB" psql -h 127.0.0.1 -U bodegas_api -d "$BD_DRILL" -At -c "SELECT count(*) FROM vino" 2>&1) \
  && echo "  ok: bodegas_api entra a la base restaurada y lee $n vinos" || { echo "  FALLO: bodegas_api no pudo entrar: $n"; FALLOS=$((FALLOS+1)); }
psql_db -At -d "$BD_DRILL" -c "SELECT '  restaurada: '||(SELECT count(*) FROM vino)||' vinos, '||(SELECT count(*) FROM comprobante)||' comprobantes, '||(SELECT count(*) FROM renglon_comprobante)||' renglones'"
[ "$FALLOS" = 0 ] && echo "SIMULACRO OK" || { echo "SIMULACRO CON $FALLOS FALLO(S)"; exit 1; }

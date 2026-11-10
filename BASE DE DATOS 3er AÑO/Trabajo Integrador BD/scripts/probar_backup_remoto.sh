#!/usr/bin/env bash
# SIMULACRO para una base REMOTA (Supabase): backup remoto cifrado -> restauracion en una base LOCAL temporal
# (Docker de desarrollo) -> comparacion con el original (filas por tabla, huellas de contenido, estructura,
# privilegios de los roles de la aplicacion) -> limpieza. Requiere la base local levantada (docker compose up -d db).
#   scripts/probar_backup_remoto.sh          # URL de SUPABASE_DB_URL (.env.supabase) o de $BACKUP_URL
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ENTORNO=dev
source "$RAIZ/scripts/lib_entorno.sh"
if [ -z "${BACKUP_URL:-}" ]; then BACKUP_URL="$(grep -E '^SUPABASE_DB_URL=' "$RAIZ/.env.supabase" | head -1 | cut -d= -f2-)"; fi
export BACKUP_URL
TMP="$(mktemp -d)"; BD="${PGBASE}_remoto_sim"; FALLOS=0
trap 'rm -rf "$TMP"; psql_db -d postgres -c "DROP DATABASE IF EXISTS \"'"$BD"'\" WITH (FORCE)" >/dev/null 2>&1 || true' EXIT
export BACKUP_CLAVE="${BACKUP_CLAVE:-$(openssl rand -hex 16)}"

"$RAIZ/scripts/backup_remoto.sh" "$TMP" | sed 's/^/  /'
ARCH="$(cat "$TMP/ultimo_backup.txt")"
echo "-- restauracion en la base local '$BD'"
"$RAIZ/scripts/restore.sh" "$ARCH" "$BD" --forzar 2>&1 | grep -vE "^NOTICE|does not exist, skipping" | sed 's/^/  /'

remoto() { docker run --rm -i -e BACKUP_URL postgres:17-alpine sh -c 'psql "$BACKUP_URL" -At -X -q'; }
CONTEOS='SELECT format($f$SELECT %L || '"'"'='"'"' || count(*) FROM public.%I$f$, relname, relname) FROM pg_class WHERE relkind = '"'"'r'"'"' AND relnamespace = '"'"'public'"'"'::regnamespace ORDER BY relname \gexec'
HUELLAS="SELECT 'renglon_comprobante='||md5(string_agg(r::text, ',' ORDER BY nro_comprobante, cod_vino)) FROM renglon_comprobante r
UNION ALL SELECT 'cliente='||md5(string_agg(c::text, ',' ORDER BY id_cliente)) FROM cliente c
UNION ALL SELECT 'vino='||md5(string_agg(v::text, ',' ORDER BY cod_vino)) FROM vino v
UNION ALL SELECT 'stock_sala='||md5(string_agg(s::text, ',' ORDER BY id_sala, cod_vino)) FROM stock_sala s"
ESTRUCTURA="SELECT 'indices='||count(*) FROM pg_indexes WHERE schemaname='public'
UNION ALL SELECT 'triggers='||count(*) FROM pg_trigger WHERE NOT tgisinternal
UNION ALL SELECT 'funciones='||count(*) FROM pg_proc WHERE pronamespace='public'::regnamespace
UNION ALL SELECT 'api_inserta_vino='||has_table_privilege('bodegas_api','vino','INSERT')
UNION ALL SELECT 'api_inserta_stock='||has_table_privilege('bodegas_api','stock_sala','INSERT')
UNION ALL SELECT 'ro_inserta_vino='||has_table_privilege('bodegas_ro','vino','INSERT')
UNION ALL SELECT 'total_comprobante_1='||fn_total_comprobante(1)"
for q in "$CONTEOS" "$HUELLAS" "$ESTRUCTURA"; do
  remoto <<< "$q" | sort > "$TMP/o.txt"; psql_db -At -d "$BD" <<< "$q" | sort > "$TMP/c.txt"
  if diff -q "$TMP/o.txt" "$TMP/c.txt" >/dev/null; then echo "  ok: $(wc -l < "$TMP/o.txt" | tr -d ' ') valores identicos entre el remoto y la copia restaurada"
  else echo "  FALLO:"; diff "$TMP/o.txt" "$TMP/c.txt" | sed 's/^/     /'; FALLOS=$((FALLOS+1)); fi
done
[ "$FALLOS" = 0 ] && echo "SIMULACRO REMOTO OK" || { echo "SIMULACRO REMOTO CON $FALLOS FALLO(S)"; exit 1; }

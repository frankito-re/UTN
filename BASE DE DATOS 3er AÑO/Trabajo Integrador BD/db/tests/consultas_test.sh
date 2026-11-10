#!/usr/bin/env bash
# =============================================================================
# Verifica consultas/*.sql (Etapa 5) contra la base CARGADA (cargar_datos.py):
#   * ningun archivo produce errores;
#   * cada UPDATE/DELETE afecta exactamente las filas que cuenta una consulta
#     independiente (sin copiar la sentencia a probar);
#   * los archivos dejan la base intacta (todo termina en ROLLBACK);
#   * S2 (division relacional) coincide con la formulacion alternativa HAVING;
#   * S12a devuelve al cliente armado por la demostracion.
# Uso:  bash db/tests/consultas_test.sh        (contenedor levantado y base cargada)
# =============================================================================
set -u
cd "$(dirname "$0")/../.."
CONT="${CONTENEDOR:-bodegas_atuel_postgres}"
sql()  { docker exec -i "$CONT" sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At -X -q' <<<"$1"; }
run()  { docker exec -i "$CONT" sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -X' < "$1" 2>&1; }
FALLOS=0
ok()   { echo "  ok    $1"; }
mal()  { echo "  FALLO $1"; FALLOS=$((FALLOS + 1)); }
check_tag() {  # $1 = salida, $2 = etiqueta exacta esperada (linea completa), $3 = descripcion
  if grep -qx "$2" <<<"$1"; then ok "$3 ($2)"; else mal "$3: no aparece la linea «$2»"; fi
}
HUELLA="SELECT (SELECT count(*) FROM comprobante)||'/'||(SELECT count(*) FROM renglon_comprobante)||'/'||(SELECT count(*) FROM cliente)||'/'||(SELECT count(*) FROM socio)||'/'||(SELECT count(*) FROM empleado)||'/'||(SELECT count(*) FROM ingreso)||'/'||(SELECT count(*) FROM renglon_ingreso)||'/'||(SELECT count(*) FROM cepa)||'/'||(SELECT count(*) FROM maridaje)||'/'||(SELECT count(*) FROM vino_maridaje)||'/'||(SELECT count(*) FROM bodega)||'/'||(SELECT count(*) FROM sala_venta)||'/'||(SELECT count(*) FROM cobertura_transportista)||'/'||(SELECT count(*) FROM auditoria_precio)||'/'||(SELECT sum(cantidad) FROM stock_sala)||'/'||(SELECT sum(precio) FROM vino)||'/'||(SELECT sum(salario) FROM empleado)||'/'||(SELECT sum(descuento) FROM cliente)||'/'||(SELECT string_agg(dia_cierre, ',' ORDER BY id_sala) FROM sala_venta)"
ANTES=$(sql "$HUELLA")

echo "== update.sql"
OUT=$(run consultas/update.sql)
grep -q "ERROR" <<<"$OUT" && mal "update.sql tiene errores" || ok "sin errores"
check_tag "$OUT" "UPDATE $(sql "SELECT count(*) FROM empleado WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '5 years'")" "U2 filas"
check_tag "$OUT" "UPDATE $(sql "SELECT count(*) FROM vino WHERE cuit_bodega = (SELECT min(cuit) FROM bodega)")" "U3 filas"
check_tag "$OUT" "UPDATE $(sql "SELECT count(*) FROM sala_venta WHERE dia_cierre IN ('lunes','miercoles')")" "U4 filas"
check_tag "$OUT" "UPDATE 10" "U5 filas"
check_tag "$OUT" "UPDATE $(sql "SELECT count(*) FROM (SELECT id_cliente FROM permiso_exportacion GROUP BY 1 HAVING count(*) > 3) x")" "U6 filas"
[ "$(grep -c '^UPDATE 200$' <<<"$OUT")" = 2 ] && ok "U1 desajusta y corrige 200 renglones" || mal "U1: se esperaban dos UPDATE 200"
grep -A2 "renglones_desajustados_despues" <<<"$OUT" | grep -qE '^ +0$' && ok "U1 deja 0 renglones desajustados" || mal "U1 no corrigio todo"
grep -A2 "comprobantes_con_total_incorrecto" <<<"$OUT" | grep -qE '^ +0$' && ok "U1: totales consistentes (RN-08)" || mal "U1: totales inconsistentes"
grep -A2 "filas_de_auditoria_generadas" <<<"$OUT" | grep -qE "^ +$(sql "SELECT count(*) FROM vino WHERE cuit_bodega = (SELECT min(cuit) FROM bodega)")$" && ok "U3 audita cada cambio de precio (RN-13)" || mal "U3 no audito todos los cambios"
grep -qE '^ *lunes +\| *[0-9, ]+$' <<<"$OUT" && ok "U4 muestra el intercambio" || mal "U4 sin salida"

echo "== insert.sql"
OUT=$(run consultas/insert.sql)
grep -q "ERROR" <<<"$OUT" && mal "insert.sql tiene errores" || ok "sin errores"
check_tag "$OUT" "INSERT 0 $(sql "SELECT count(*) FROM vino WHERE tipo='tinto' AND graduacion >= 14")" "I2 asocia todos los tintos >= 14°"
grep -qE 'Cordero al disco.*\| t$' <<<"$OUT" && ok "I2: todos los asociados son tintos" || mal "I2: hay asociados que no son tintos"
[ "$(grep -c '^INSERT 0 3$' <<<"$OUT")" = 1 ] && ok "I3 inserta 3 renglones" || mal "I3: falta INSERT 0 3"
grep -qE '^ +[0-9]+ \| [0-9-]+ \| +[0-9.]+ \| +[0-9.]+ \| +[0-9.]+$' <<<"$OUT" && ok "I3: la base calculo subtotal, descuento y total" || mal "I3: sin importes"
grep -qE 'Bodega Cerros del Atuel' <<<"$OUT" && ok "I4 inserta la bodega" || mal "I4"
grep -qE 'Yrigoyen +\| +1250 +\| +domingo +\| +General Alvear' <<<"$OUT" && ok "I5 inserta la sala" || mal "I5"
grep -qE 'en_confeccion \| +1 \| +120' <<<"$OUT" && ok "I6 ingreso en confeccion de 120" || mal "I6"
grep -A2 "stock_deposito_despues_sin_procesar" <<<"$OUT" | tail -1 | grep -qE "^ +$(sql "SELECT fn_stock_deposito(min(cod_vino)) FROM vino")$" && ok "I6 no toca el stock del deposito" || mal "I6 altero el deposito"
I1_COD=$(sed -n '/=== I1 /,/=== I2 /p' <<<"$OUT" | grep -E '^ +[0-9]+ \| +5620$' | head -1 | awk '{print $1}')
I1_N=$(sql "SELECT count(*) FROM ingreso WHERE cod_transportista = ${I1_COD:-0} AND fecha >= CURRENT_DATE - INTERVAL '3 months'")
I1_MIN=$(sql "SELECT min(n) FROM (SELECT count(i.cod_ingreso) n FROM transportista t LEFT JOIN ingreso i ON i.cod_transportista = t.cod_transportista AND i.fecha >= CURRENT_DATE - INTERVAL '3 months' WHERE NOT EXISTS (SELECT 1 FROM cobertura_transportista c WHERE c.cod_transportista = t.cod_transportista AND c.cod_postal = '5620') GROUP BY t.cod_transportista) x")
[ -n "$I1_COD" ] && [ "$I1_N" = "$I1_MIN" ] && ok "I1 eligio al transportista $I1_COD con $I1_N envios (el minimo entre los que no cubrian General Alvear)" || mal "I1: transportista=$I1_COD envios=$I1_N minimo=$I1_MIN"
[ "$(grep -c '^INSERT 0 1$' <<<"$OUT")" -ge 4 ] && ok "I1/I4/I5 insertan una fila cada una" || mal "faltan INSERT 0 1"

echo "== delete.sql"
OUT=$(run consultas/delete.sql)
grep -q "ERROR" <<<"$OUT" && mal "delete.sql tiene errores" || ok "sin errores"
check_tag "$OUT" "DELETE $(sql "SELECT count(*) FROM comprobante c JOIN cliente cl USING (id_cliente) WHERE cl.tipo_cliente='socio' AND c.fecha < CURRENT_DATE - INTERVAL '5 years'")" "D1 filas"
check_tag "$OUT" "DELETE 1" "D2 borra solo la cepa sin uso"
check_tag "$OUT" "DELETE $(sql "SELECT count(*) FROM empleado WHERE fecha_ingreso > CURRENT_DATE - INTERVAL '2 years' AND id_sala = (SELECT id_sala FROM empleado WHERE fecha_ingreso > CURRENT_DATE - INTERVAL '2 years' GROUP BY id_sala ORDER BY count(*) DESC, id_sala LIMIT 1)")" "D3 filas"
check_tag "$OUT" "DELETE $(sql "SELECT count(*) FROM cliente c WHERE c.tipo_cliente='socio' AND c.fecha_alta < CURRENT_DATE - INTERVAL '5 years' AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente=c.id_cliente)")" "D4 filas"
check_tag "$OUT" "DELETE $(sql "SELECT count(*) FROM ingreso WHERE estado='procesado' AND fecha < CURRENT_DATE - 365")" "D5 filas"
check_tag "$OUT" "DELETE $(sql "SELECT count(*) FROM cliente c WHERE c.tipo_cliente='socio' AND c.cod_postal=(SELECT cod_postal FROM localidad WHERE nombre='San Rafael' AND provincia='Mendoza') AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente=c.id_cliente)")" "D6 filas"
grep -A2 "renglones_huerfanos" <<<"$OUT" | grep -qE '^ +0$' && ok "D1 sin renglones huerfanos" || mal "D1 dejo renglones huerfanos"
grep -A2 "filas_de_socio_huerfanas" <<<"$OUT" | grep -qE '^ +0$' && ok "D4 sin subtipos huerfanos" || mal "D4 dejo subtipos huerfanos"

echo "== select.sql"
OUT=$(run consultas/select.sql)
grep -q "ERROR" <<<"$OUT" && mal "select.sql tiene errores" || ok "sin errores"
for s in S1 S2 S3 S4 S5 S6 S7 S8 S9 S10 S11 S12a S12b; do grep -q "=== $s " <<<"$OUT" && ok "$s ejecutada" || mal "$s no se ejecuto"; done
N_S2=$(sql "SELECT count(*) FROM (SELECT cod_vino FROM comprobante c JOIN renglon_comprobante r USING (nro_comprobante) GROUP BY 1 HAVING count(DISTINCT id_sala) = (SELECT count(*) FROM sala_venta)) x")
ESC_S2=$(sed -n '/=== S2 /,/=== S3 /p' <<<"$OUT" | grep -oE '^\([0-9]+ rows?\)' | head -1)
[ "$ESC_S2" = "($N_S2 rows)" ] && ok "S2 (NOT EXISTS) = formulacion con HAVING: $N_S2 vinos" || mal "S2: $ESC_S2 contra $N_S2 esperados"
sed -n '/resultado_con_los_datos_reales/,/ROLLBACK/p' <<<"$OUT" | grep -q "(0 rows)" && ok "S12a: 0 clientes con los datos reales" || mal "S12a deberia dar 0 con los datos reales"
sed -n '/resultado_de_la_demostracion/,/ROLLBACK/p' <<<"$OUT" | grep -q "(1 row)" && ok "S12a: la demostracion encuentra al cliente armado" || mal "S12a demostracion"
sed -n '/=== S11 /,/=== S12a /p' <<<"$OUT" | grep -qE "\(15 rows\)" && ok "S11 devuelve filas con ranking y acumulado" || mal "S11 sin filas"

DESPUES=$(sql "$HUELLA")
[ "$ANTES" = "$DESPUES" ] && ok "la base quedo intacta (todo termino en ROLLBACK)" || mal "la base cambio:\n  antes   $ANTES\n  despues $DESPUES"
echo
[ "$FALLOS" = 0 ] && echo "TODO OK" || { echo "$FALLOS FALLO(S)"; exit 1; }

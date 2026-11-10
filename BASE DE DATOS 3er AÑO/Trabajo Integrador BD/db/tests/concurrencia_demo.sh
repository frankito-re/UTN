#!/usr/bin/env bash
# =============================================================================
# Demo de concurrencia (RN-09): dos ventas simultaneas del mismo vino.
#
# Hay 10 botellas en la sala. La sesion A vende 8 y tarda 4 s en confirmar; la
# sesion B intenta vender 8 mientras A sigue abierta. El trigger
# trg_validar_stock_venta toma SELECT ... FOR UPDATE sobre la fila de stock:
#   * B queda BLOQUEADA hasta que A confirma (se mide cuanto espera);
#   * al desbloquearse ve el stock real (2) y la venta se rechaza con RN009;
#   * sin el bloqueo, las dos leerian 10 y venderian 16 botellas.
#
# Uso (con el contenedor levantado):  bash db/tests/concurrencia_demo.sh
# Deja la base como estaba: los datos de la demo se borran al final.
# =============================================================================
set -u
CONTENEDOR="${CONTENEDOR:-bodegas_atuel_postgres}"
psql_() { docker exec -i "$CONTENEDOR" sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -q -X "$@"' _ "$@"; }

limpiar() {
  psql_ >/dev/null 2>&1 <<'SQL'
DELETE FROM comprobante WHERE id_cliente IN (SELECT id_cliente FROM cliente WHERE nro_doc = 'DEMO-CONC');
DELETE FROM cliente     WHERE nro_doc = 'DEMO-CONC';
DELETE FROM stock_sala  WHERE id_sala IN (SELECT id_sala FROM sala_venta WHERE calle = 'Sala Demo Concurrencia');
DELETE FROM vino        WHERE nombre = 'Demo Concurrencia';
DELETE FROM cepa        WHERE nombre = 'Cepa Demo Concurrencia';
DELETE FROM sala_venta  WHERE calle = 'Sala Demo Concurrencia';
DELETE FROM bodega      WHERE cuit = '30999999990';
DELETE FROM localidad   WHERE cod_postal = 'DEMO';
SQL
}
trap limpiar EXIT
limpiar

echo "== Preparacion: sala con 10 botellas y dos comprobantes vacios"
psql_ -v ON_ERROR_STOP=1 <<'SQL'
-- Una sola transaccion: el vino y su corte (RN-05) y el cliente y su subtipo deben confirmarse juntos.
BEGIN;
INSERT INTO localidad VALUES ('DEMO', 'Demo', 'Mendoza', 'Encargado Demo');
INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Sala Demo Concurrencia', 1, 'lunes', 'DEMO');
INSERT INTO bodega VALUES ('30999999990', 'Bodega Demo', 'Demo');
INSERT INTO cepa (nombre, tipo) VALUES ('Cepa Demo Concurrencia', 'tinta');
INSERT INTO vino (nombre, tipo, anada, volumen_ml, graduacion, precio, cuit_bodega)
     VALUES ('Demo Concurrencia', 'tinto', 2024, 750, 13, 1000, '30999999990');
INSERT INTO composicion SELECT v.cod_vino, c.id_cepa, 100 FROM vino v, cepa c
 WHERE v.nombre = 'Demo Concurrencia' AND c.nombre = 'Cepa Demo Concurrencia';
INSERT INTO cliente (nombre_razon_social, tipo_doc, nro_doc, direccion, cod_postal, tipo_cliente)
     VALUES ('Cliente Demo', 'DNI', 'DEMO-CONC', 'Demo', 'DEMO', 'socio');
INSERT INTO socio SELECT id_cliente FROM cliente WHERE nro_doc = 'DEMO-CONC';
INSERT INTO stock_sala SELECT s.id_sala, v.cod_vino, 10 FROM sala_venta s, vino v
 WHERE s.calle = 'Sala Demo Concurrencia' AND v.nombre = 'Demo Concurrencia';
INSERT INTO comprobante (id_cliente, id_sala)
     SELECT c.id_cliente, s.id_sala FROM cliente c, sala_venta s
      WHERE c.nro_doc = 'DEMO-CONC' AND s.calle = 'Sala Demo Concurrencia';
INSERT INTO comprobante (id_cliente, id_sala)
     SELECT c.id_cliente, s.id_sala FROM cliente c, sala_venta s
      WHERE c.nro_doc = 'DEMO-CONC' AND s.calle = 'Sala Demo Concurrencia';
COMMIT;
SQL
[ $? -eq 0 ] || { echo "No se pudo preparar la demo (¿esta el contenedor levantado?)"; exit 1; }

COMP_A=$(psql_ -At -c "SELECT min(nro_comprobante) FROM comprobante WHERE id_cliente = (SELECT id_cliente FROM cliente WHERE nro_doc='DEMO-CONC')")
COMP_B=$(psql_ -At -c "SELECT max(nro_comprobante) FROM comprobante WHERE id_cliente = (SELECT id_cliente FROM cliente WHERE nro_doc='DEMO-CONC')")

echo "== Sesion A: vende 8 y confirma a los 4 segundos"
psql_ <<SQL &
BEGIN;
INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad)
     SELECT $COMP_A, cod_vino, 8 FROM vino WHERE nombre = 'Demo Concurrencia';
\echo '   [A] inserto 8 botellas; mantiene el bloqueo y duerme 4 s...'
SELECT pg_sleep(4);
COMMIT;
\echo '   [A] COMMIT'
SQL
PID_A=$!

sleep 1
echo "== Sesion B: intenta vender 8 mientras A esta abierta"
T0=$(date +%s)
psql_ <<SQL
\echo '   [B] intentando insertar 8 botellas (deberia quedar esperando a A)...'
BEGIN;
INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad)
     SELECT $COMP_B, cod_vino, 8 FROM vino WHERE nombre = 'Demo Concurrencia';
SQL
echo "   [B] respondio despues de $(( $(date +%s) - T0 )) s (esperaba el COMMIT de A) y fue rechazada con RN009, como se esperaba"
wait "$PID_A"

echo "== Resultado final"
psql_ <<'SQL'
SELECT 'stock restante en la sala' AS dato, cantidad::text AS valor
  FROM stock_sala WHERE id_sala = (SELECT id_sala FROM sala_venta WHERE calle = 'Sala Demo Concurrencia')
UNION ALL
SELECT 'renglones de venta registrados', count(*)::text FROM renglon_comprobante
 WHERE nro_comprobante IN (SELECT nro_comprobante FROM comprobante
                            WHERE id_cliente = (SELECT id_cliente FROM cliente WHERE nro_doc = 'DEMO-CONC'));
SQL
echo "Esperado: stock restante = 2 y 1 solo renglon (se vendieron 8 de 10; la otra venta fue rechazada)."

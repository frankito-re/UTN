-- =============================================================================
-- consultas/delete.sql · Borrado de datos (D1 a D6) · Bodegas del Atuel
--
-- Ejecutar con psql (usa \echo y \gset):
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB' < consultas/delete.sql
--
-- Cada consulta corre en su propia transacción y termina en ROLLBACK: se puede
-- ejecutar el archivo entero sin alterar los datos. Para aplicar una de verdad,
-- cambiar su ROLLBACK por COMMIT. La sentencia a evaluar es la marcada «-- D<n>».
--
-- Las FK usan ON DELETE RESTRICT (RN-14) salvo en dependientes naturales
-- (renglones, subtipos de cliente), que se borran en cascada. Las sentencias
-- están escritas para no chocar con ningún RESTRICT.
-- =============================================================================
\set ON_ERROR_STOP on
\pset pager off


-- =============================================================================
-- D1 · Borrar los comprobantes de más de 5 años de los socios del club.
-- Los renglones se borran en cascada. El stock NO se devuelve a las salas: es una
-- depuración de historial, no una anulación de ventas. Si se usa la vista
-- materializada, refrescarla después (CALL sp_refrescar_reportes()).
-- =============================================================================
\echo '=== D1 · Comprobantes de socios con más de 5 años'
BEGIN;
SELECT count(*) AS comprobantes_a_borrar
  FROM comprobante c JOIN cliente cl USING (id_cliente)
 WHERE cl.tipo_cliente = 'socio' AND c.fecha < CURRENT_DATE - INTERVAL '5 years' \gset
\echo 'a borrar:' :comprobantes_a_borrar

-- D1
DELETE FROM comprobante c
 USING cliente cl
 WHERE cl.id_cliente = c.id_cliente
   AND cl.tipo_cliente = 'socio'
   AND c.fecha < CURRENT_DATE - INTERVAL '5 years';

SELECT count(*) AS quedan_de_socios_con_mas_de_5_anios
  FROM comprobante c JOIN cliente cl USING (id_cliente)
 WHERE cl.tipo_cliente = 'socio' AND c.fecha < CURRENT_DATE - INTERVAL '5 years';
SELECT count(*) AS renglones_huerfanos
  FROM renglon_comprobante r WHERE NOT EXISTS (SELECT 1 FROM comprobante c WHERE c.nro_comprobante = r.nro_comprobante);
ROLLBACK;


-- =============================================================================
-- D2 · Eliminar las cepas que no se usan en ningún vino ni en ninguna parcela.
-- (Para la demostración se agrega primero una cepa sin uso.)
-- =============================================================================
\echo '=== D2 · Cepas sin uso'
BEGIN;
INSERT INTO cepa (nombre, tipo) VALUES ('Cepa de prueba sin uso', 'tinta');
SELECT count(*) AS cepas_antes FROM cepa;

-- D2
DELETE FROM cepa c
 WHERE NOT EXISTS (SELECT 1 FROM composicion co WHERE co.id_cepa = c.id_cepa)
   AND NOT EXISTS (SELECT 1 FROM parcela p WHERE p.id_cepa = c.id_cepa);

SELECT count(*) AS cepas_despues FROM cepa;
SELECT count(*) AS cepa_de_prueba_sigue_existiendo FROM cepa WHERE nombre = 'Cepa de prueba sin uso';
ROLLBACK;


-- =============================================================================
-- D3 · Eliminar los empleados de una sala dada de baja que tengan menos de
--      2 años de antigüedad. La sala se elige en :sala_baja (aquí, la que más
--      empleados recientes tiene). Los de mayor antigüedad no se tocan: habría que
--      reasignarlos a otra sala antes de poder borrar la sala (RN-03).
-- =============================================================================
\echo '=== D3 · Empleados recientes de una sala dada de baja'
SELECT id_sala AS sala_baja FROM empleado
 WHERE fecha_ingreso > CURRENT_DATE - INTERVAL '2 years'
 GROUP BY id_sala ORDER BY count(*) DESC, id_sala LIMIT 1 \gset
BEGIN;
SELECT count(*) AS empleados_de_la_sala,
       count(*) FILTER (WHERE fecha_ingreso > CURRENT_DATE - INTERVAL '2 years') AS con_menos_de_2_anios
  FROM empleado WHERE id_sala = :sala_baja;

-- D3
DELETE FROM empleado
 WHERE id_sala = :sala_baja
   AND fecha_ingreso > CURRENT_DATE - INTERVAL '2 years';

SELECT count(*) AS empleados_de_la_sala_despues,
       count(*) FILTER (WHERE fecha_ingreso > CURRENT_DATE - INTERVAL '2 years') AS con_menos_de_2_anios
  FROM empleado WHERE id_sala = :sala_baja;
ROLLBACK;


-- =============================================================================
-- D4 · Borrar los socios que nunca compraron y que se dieron de alta hace más
--      de 5 años. El subtipo (tabla socio) se borra en cascada.
-- =============================================================================
\echo '=== D4 · Socios sin compras con alta de más de 5 años'
BEGIN;
SELECT count(*) AS socios_a_borrar FROM cliente c
 WHERE c.tipo_cliente = 'socio' AND c.fecha_alta < CURRENT_DATE - INTERVAL '5 years'
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);

-- D4
DELETE FROM cliente c
 WHERE c.tipo_cliente = 'socio'
   AND c.fecha_alta < CURRENT_DATE - INTERVAL '5 years'
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);

SELECT count(*) AS quedan_socios_sin_compras_de_mas_de_5_anios FROM cliente c
 WHERE c.tipo_cliente = 'socio' AND c.fecha_alta < CURRENT_DATE - INTERVAL '5 years'
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);
SELECT count(*) AS filas_de_socio_huerfanas
  FROM socio s WHERE NOT EXISTS (SELECT 1 FROM cliente c WHERE c.id_cliente = s.id_cliente);
ROLLBACK;


-- =============================================================================
-- D5 · Eliminar los ingresos procesados de hace más de 365 días.
-- Sus renglones se borran en cascada (RN-12 lo permite porque el ingreso ya no
-- existe). El stock del depósito no cambia: ya se sumó al procesarlos.
-- =============================================================================
\echo '=== D5 · Ingresos procesados de más de 365 días'
BEGIN;
SELECT count(*) AS ingresos_a_borrar FROM ingreso
 WHERE estado = 'procesado' AND fecha < CURRENT_DATE - 365;
SELECT sum(cantidad) AS stock_deposito_total_antes FROM stock_deposito;

-- D5
DELETE FROM ingreso
 WHERE estado = 'procesado'
   AND fecha < CURRENT_DATE - 365;

SELECT count(*) AS quedan_procesados_viejos FROM ingreso
 WHERE estado = 'procesado' AND fecha < CURRENT_DATE - 365;
SELECT sum(cantidad) AS stock_deposito_total_despues FROM stock_deposito;
ROLLBACK;


-- =============================================================================
-- D6 · Borrar los socios sin compras de una localidad específica (aquí, San Rafael).
-- =============================================================================
\echo '=== D6 · Socios sin compras de San Rafael'
BEGIN;
SELECT count(*) AS socios_a_borrar FROM cliente c
 WHERE c.tipo_cliente = 'socio'
   AND c.cod_postal = (SELECT cod_postal FROM localidad WHERE nombre = 'San Rafael' AND provincia = 'Mendoza')
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);

-- D6
DELETE FROM cliente c
 WHERE c.tipo_cliente = 'socio'
   AND c.cod_postal = (SELECT cod_postal FROM localidad WHERE nombre = 'San Rafael' AND provincia = 'Mendoza')
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);

SELECT count(*) AS quedan_socios_sin_compras_en_san_rafael FROM cliente c
 WHERE c.tipo_cliente = 'socio'
   AND c.cod_postal = (SELECT cod_postal FROM localidad WHERE nombre = 'San Rafael' AND provincia = 'Mendoza')
   AND NOT EXISTS (SELECT 1 FROM comprobante v WHERE v.id_cliente = c.id_cliente);
ROLLBACK;

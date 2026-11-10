-- =============================================================================
-- consultas/update.sql · Modificación de datos (U1 a U6) · Bodegas del Atuel
--
-- Ejecutar con psql (usa \echo y \gset):
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB' < consultas/update.sql
--
-- Cada consulta corre en su propia transacción y termina en ROLLBACK, así que se
-- puede ejecutar el archivo entero sin alterar los datos. Para aplicar una de
-- verdad, cambiar su ROLLBACK por COMMIT. Los SELECT de «antes/después» son solo
-- para verificar. La sentencia a evaluar es la marcada con «-- U<n>».
--
-- Los triggers de la base participan: recalculan comprobantes (RN-08), auditan
-- cambios de precio (RN-13), etc.
-- =============================================================================
\set ON_ERROR_STOP on
\pset pager off


-- =============================================================================
-- U1 · Recalcular el total de los comprobantes aplicando el descuento que
--      corresponde al tipo de cliente (socio 10 %, distribuidor 20 %, exportador 30 %).
--
-- Se corrige el descuento de cada RENGLÓN; los triggers recalculan el subtotal
-- del renglón y el subtotal, descuento y total del comprobante (RN-08): nada se
-- calcula a mano. Solo se tocan los renglones desajustados.
-- Nota: usa el descuento BASE del tipo. Los exportadores con descuento especial
-- (U6) volverían a 30 %; correr U1 antes de U6 o excluirlos.
-- =============================================================================
\echo '=== U1 · Recalcular totales según tipo de cliente'
BEGIN;

-- (solo para la demostración) desajustar el descuento de los últimos 200 renglones
UPDATE renglon_comprobante r
   SET descuento_pct = 0
  FROM (SELECT nro_comprobante, cod_vino FROM renglon_comprobante
         ORDER BY nro_comprobante DESC, cod_vino LIMIT 200) x
 WHERE r.nro_comprobante = x.nro_comprobante AND r.cod_vino = x.cod_vino;

SELECT count(*) AS renglones_desajustados_antes
  FROM renglon_comprobante r
  JOIN comprobante c  ON c.nro_comprobante = r.nro_comprobante
  JOIN cliente cl     ON cl.id_cliente = c.id_cliente
 WHERE r.descuento_pct <> fn_descuento_tipo_cliente(cl.tipo_cliente);

-- U1
UPDATE renglon_comprobante r
   SET descuento_pct = fn_descuento_tipo_cliente(cl.tipo_cliente)
  FROM comprobante c
  JOIN cliente cl ON cl.id_cliente = c.id_cliente
 WHERE c.nro_comprobante = r.nro_comprobante
   AND r.descuento_pct <> fn_descuento_tipo_cliente(cl.tipo_cliente);

SELECT count(*) AS renglones_desajustados_despues
  FROM renglon_comprobante r
  JOIN comprobante c  ON c.nro_comprobante = r.nro_comprobante
  JOIN cliente cl     ON cl.id_cliente = c.id_cliente
 WHERE r.descuento_pct <> fn_descuento_tipo_cliente(cl.tipo_cliente);

-- Los totales de los últimos comprobantes coinciden con la suma de sus renglones:
SELECT count(*) AS comprobantes_con_total_incorrecto
  FROM (SELECT * FROM comprobante ORDER BY nro_comprobante DESC LIMIT 100) c
  JOIN LATERAL fn_calcular_comprobante(c.nro_comprobante) f ON TRUE
 WHERE (c.subtotal, c.descuento, c.total) IS DISTINCT FROM (f.subtotal_bruto, f.monto_descuento, f.total);
ROLLBACK;


-- =============================================================================
-- U2 · Aumentar un 20 % el salario de los empleados con más de 5 años de antigüedad.
-- =============================================================================
\echo '=== U2 · +20 % de salario a empleados con más de 5 años'
BEGIN;
SELECT count(*) AS empleados_afectados, round(avg(salario), 2) AS salario_promedio_antes
  FROM empleado WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '5 years';

-- U2
UPDATE empleado
   SET salario = ROUND(salario * 1.20, 2)
 WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '5 years';

SELECT count(*) AS empleados_con_mas_de_5_anios, round(avg(salario), 2) AS salario_promedio_despues
  FROM empleado WHERE fecha_ingreso < CURRENT_DATE - INTERVAL '5 years';
ROLLBACK;


-- =============================================================================
-- U3 · Incrementar un 13 % el precio de los vinos de una bodega determinada.
-- La bodega se elige en la variable :cuit_bodega (aquí, la de menor CUIT).
-- El trigger de RN-13 registra cada cambio en auditoria_precio.
-- =============================================================================
\echo '=== U3 · +13 % de precio a los vinos de una bodega'
SELECT cuit AS cuit_bodega FROM bodega ORDER BY cuit LIMIT 1 \gset
BEGIN;
SELECT count(*) AS vinos_de_la_bodega, round(avg(precio), 2) AS precio_promedio_antes
  FROM vino WHERE cuit_bodega = :'cuit_bodega';

-- U3
UPDATE vino
   SET precio = ROUND(precio * 1.13, 2)
 WHERE cuit_bodega = :'cuit_bodega';

SELECT round(avg(precio), 2) AS precio_promedio_despues FROM vino WHERE cuit_bodega = :'cuit_bodega';
SELECT count(*) AS filas_de_auditoria_generadas
  FROM auditoria_precio a JOIN vino v USING (cod_vino)
 WHERE v.cuit_bodega = :'cuit_bodega' AND a.fecha_hora >= now() - INTERVAL '1 minute';
ROLLBACK;


-- =============================================================================
-- U4 · Cambiar el día de cierre de las salas de lunes a miércoles y viceversa,
--      en UNA sola sentencia (un UPDATE secuencial pisaría el primer cambio).
-- =============================================================================
\echo '=== U4 · Intercambiar día de cierre lunes <-> miércoles'
BEGIN;
SELECT dia_cierre, string_agg(id_sala::text, ', ' ORDER BY id_sala) AS salas FROM sala_venta
 WHERE dia_cierre IN ('lunes', 'miercoles') GROUP BY dia_cierre ORDER BY dia_cierre;

-- U4
UPDATE sala_venta
   SET dia_cierre = CASE dia_cierre WHEN 'lunes' THEN 'miercoles' ELSE 'lunes' END
 WHERE dia_cierre IN ('lunes', 'miercoles');

SELECT dia_cierre, string_agg(id_sala::text, ', ' ORDER BY id_sala) AS salas FROM sala_venta
 WHERE dia_cierre IN ('lunes', 'miercoles') GROUP BY dia_cierre ORDER BY dia_cierre;
ROLLBACK;


-- =============================================================================
-- U5 · Aplicar un 15 % de descuento al precio de los 10 vinos menos vendidos
--      (por unidades; los que nunca se vendieron cuentan como 0). Desempata por código.
-- =============================================================================
\echo '=== U5 · -15 % de precio a los 10 vinos menos vendidos'
BEGIN;
-- U5
UPDATE vino
   SET precio = ROUND(precio * 0.85, 2)
 WHERE cod_vino IN (SELECT v.cod_vino
                      FROM vino v
                      LEFT JOIN renglon_comprobante r ON r.cod_vino = v.cod_vino
                     GROUP BY v.cod_vino
                     ORDER BY COALESCE(SUM(r.cantidad), 0), v.cod_vino
                     LIMIT 10);

SELECT a.cod_vino, a.precio_anterior, a.precio_nuevo
  FROM auditoria_precio a
 WHERE a.fecha_hora >= now() - INTERVAL '1 minute'
 ORDER BY a.cod_vino;
ROLLBACK;


-- =============================================================================
-- U6 · Subir al 35 % el descuento de los exportadores con más de 3 permisos
--      de exportación.
-- =============================================================================
\echo '=== U6 · Descuento 35 % a exportadores con más de 3 permisos'
BEGIN;
SELECT count(*) AS exportadores_con_mas_de_3_permisos
  FROM (SELECT id_cliente FROM permiso_exportacion GROUP BY id_cliente HAVING COUNT(*) > 3) x;

-- U6
UPDATE cliente
   SET descuento = 35
 WHERE tipo_cliente = 'exportador'
   AND id_cliente IN (SELECT id_cliente
                        FROM permiso_exportacion
                       GROUP BY id_cliente
                      HAVING COUNT(*) > 3);

SELECT descuento, count(*) AS exportadores FROM cliente
 WHERE tipo_cliente = 'exportador' GROUP BY descuento ORDER BY descuento;
ROLLBACK;

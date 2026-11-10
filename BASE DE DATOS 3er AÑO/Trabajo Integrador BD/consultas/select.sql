-- =============================================================================
-- consultas/select.sql · Consultas (S1 a S12) · Bodegas del Atuel
--
-- Ejecutar con psql (usa \echo y \gset):
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB' < consultas/select.sql
--
-- Todas son de solo lectura (salvo la preparación de S12a, que va en una
-- transacción con ROLLBACK). Las ventanas «última semana / último mes / trimestre»
-- son relativas a CURRENT_DATE: para que devuelvan datos, cargar la base con
-- `cargar_datos.py --fecha-ref hoy`.
-- =============================================================================
\set ON_ERROR_STOP on
\pset pager off

-- Parámetros de las consultas (se calculan a partir de los datos; editar a gusto)
SELECT COALESCE((SELECT id_sala FROM comprobante WHERE fecha >= CURRENT_DATE - 7
                  GROUP BY id_sala ORDER BY count(*) DESC, id_sala LIMIT 1), 1)        AS sala_ref,
       COALESCE((SELECT rt.cod_vino FROM renglon_transferencia rt
                   JOIN transferencia t USING (nro_transferencia)
                  WHERE t.fecha_confeccion >= CURRENT_DATE - 15
                  GROUP BY rt.cod_vino ORDER BY sum(rt.cantidad) DESC, rt.cod_vino LIMIT 1), 1) AS vino_ref,
       2024                                                                            AS campania_ref,
       (SELECT cuit_bodega FROM vino GROUP BY cuit_bodega ORDER BY count(*), cuit_bodega LIMIT 1) AS bodega_ref \gset


-- =============================================================================
-- S1 · Top 10 de vinos más vendidos de la red (por unidades).
-- =============================================================================
\echo '=== S1 · Top 10 vinos más vendidos'
SELECT v.cod_vino, v.nombre, v.anada, v.tipo,
       SUM(r.cantidad)  AS unidades_vendidas,
       SUM(r.subtotal)  AS importe_vendido
  FROM renglon_comprobante r
  JOIN vino v ON v.cod_vino = r.cod_vino
 GROUP BY v.cod_vino, v.nombre, v.anada, v.tipo
 ORDER BY unidades_vendidas DESC, v.cod_vino
 LIMIT 10;


-- =============================================================================
-- S2 · Vinos vendidos en TODAS las salas (división relacional).
-- «No existe una sala en la que no exista una venta del vino». Equivale a
-- GROUP BY cod_vino HAVING COUNT(DISTINCT id_sala) = (SELECT COUNT(*) FROM sala_venta).
-- =============================================================================
\echo '=== S2 · Vinos vendidos en todas las salas'
SELECT v.cod_vino, v.nombre, v.anada
  FROM vino v
 WHERE NOT EXISTS (
         SELECT 1
           FROM sala_venta s
          WHERE NOT EXISTS (
                  SELECT 1
                    FROM comprobante c
                    JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
                   WHERE c.id_sala = s.id_sala
                     AND r.cod_vino = v.cod_vino))
 ORDER BY v.cod_vino;


-- =============================================================================
-- S3 · Cantidad de clientes, por tipo, que compraron en una sala en la última
--      semana (sala: :sala_ref).
-- =============================================================================
\echo '=== S3 · Clientes por tipo que compraron en la sala' :sala_ref '(última semana)'
SELECT cl.tipo_cliente, COUNT(DISTINCT c.id_cliente) AS clientes
  FROM comprobante c
  JOIN cliente cl ON cl.id_cliente = c.id_cliente
 WHERE c.id_sala = :sala_ref
   AND c.fecha >= CURRENT_DATE - 7
 GROUP BY cl.tipo_cliente
 ORDER BY clientes DESC;


-- =============================================================================
-- S4 · Top 5 de salas con mayor solicitud de transferencias de un vino en los
--      últimos 15 días (vino: :vino_ref). Cuenta unidades solicitadas, en
--      cualquier estado.
-- =============================================================================
\echo '=== S4 · Salas que más pidieron el vino' :vino_ref '(últimos 15 días)'
SELECT t.id_sala, COUNT(*) AS transferencias, SUM(rt.cantidad) AS unidades_solicitadas
  FROM transferencia t
  JOIN renglon_transferencia rt ON rt.nro_transferencia = t.nro_transferencia
 WHERE rt.cod_vino = :vino_ref
   AND t.fecha_confeccion >= CURRENT_DATE - 15
 GROUP BY t.id_sala
 ORDER BY unidades_solicitadas DESC, t.id_sala
 LIMIT 5;


-- =============================================================================
-- S5 · Salas con MENOR cantidad de transferencias pendientes (en confección o
--      terminadas). Incluye las que tienen 0 y devuelve todas las empatadas en el mínimo.
-- =============================================================================
\echo '=== S5 · Salas con menos transferencias pendientes'
WITH pendientes AS (
    SELECT s.id_sala,
           COUNT(t.nro_transferencia) FILTER (WHERE t.estado <> 'procesado') AS pendientes
      FROM sala_venta s
      LEFT JOIN transferencia t ON t.id_sala = s.id_sala
     GROUP BY s.id_sala
)
SELECT id_sala, pendientes
  FROM pendientes
 WHERE pendientes = (SELECT MIN(pendientes) FROM pendientes)
 ORDER BY id_sala;


-- =============================================================================
-- S6 · Vinos sin stock en una sala (:sala_ref) pero con stock en el depósito
--      central. «Sin stock» incluye que la sala nunca haya tenido el vino.
-- =============================================================================
\echo '=== S6 · Vinos agotados en la sala' :sala_ref 'con stock en el depósito'
SELECT v.cod_vino, v.nombre, d.cantidad AS stock_deposito, fn_stock_sala(:sala_ref, v.cod_vino) AS stock_sala
  FROM stock_deposito d
  JOIN vino v ON v.cod_vino = d.cod_vino
 WHERE d.cantidad > 0
   AND fn_stock_sala(:sala_ref, v.cod_vino) = 0
 ORDER BY d.cantidad DESC, v.cod_vino
 LIMIT 20;


-- =============================================================================
-- S7 · Transportista con mayor actividad en el último mes (ingresos
--      transportados; desempata por botellas y luego por código).
-- =============================================================================
\echo '=== S7 · Transportista más activo del último mes'
SELECT t.cod_transportista, t.razon_social,
       COUNT(DISTINCT i.cod_ingreso)  AS ingresos,
       COALESCE(SUM(r.cantidad), 0)   AS botellas
  FROM transportista t
  JOIN ingreso i ON i.cod_transportista = t.cod_transportista
                AND i.fecha >= CURRENT_DATE - INTERVAL '1 month'
  LEFT JOIN renglon_ingreso r ON r.cod_ingreso = i.cod_ingreso
 GROUP BY t.cod_transportista, t.razon_social
 ORDER BY ingresos DESC, botellas DESC, t.cod_transportista
 LIMIT 1;


-- =============================================================================
-- S8 · Ventas por sala en el último trimestre, de mayor a menor.
-- =============================================================================
\echo '=== S8 · Ventas por sala del último trimestre'
SELECT s.id_sala, s.calle || ' ' || s.numero AS sala, l.nombre AS localidad,
       COUNT(*)      AS comprobantes,
       SUM(c.total)  AS total_vendido
  FROM comprobante c
  JOIN sala_venta s ON s.id_sala = c.id_sala
  JOIN localidad l  ON l.cod_postal = s.cod_postal
 WHERE c.fecha >= CURRENT_DATE - INTERVAL '3 months'
 GROUP BY s.id_sala, s.calle, s.numero, l.nombre
 ORDER BY total_vendido DESC;


-- =============================================================================
-- S9 · Ficha de un vino (:vino_ref): datos, bodega, cepas con su porcentaje,
--      maridajes con temperatura de servicio y stock (depósito + salas).
-- =============================================================================
\echo '=== S9 · Ficha del vino' :vino_ref
SELECT v.cod_vino, v.nombre, v.tipo, v.anada, v.volumen_ml, v.graduacion, v.precio,
       b.razon_social AS bodega,
       corte.detalle  AS cepas,
       mar.detalle    AS maridajes,
       st.stock_deposito, st.stock_salas, st.stock_total
  FROM vino v
  JOIN bodega b ON b.cuit = v.cuit_bodega
  JOIN v_stock_vino st ON st.cod_vino = v.cod_vino
  LEFT JOIN LATERAL (
        SELECT string_agg(c.nombre || ' ' || trim_scale(co.porcentaje)::TEXT || '%',
                          ', ' ORDER BY co.porcentaje DESC, c.nombre) AS detalle
          FROM composicion co JOIN cepa c ON c.id_cepa = co.id_cepa
         WHERE co.cod_vino = v.cod_vino) corte ON TRUE
  LEFT JOIN LATERAL (
        SELECT string_agg(m.nombre || ' (' || trim_scale(m.temperatura_servicio)::TEXT || ' °C)',
                          ', ' ORDER BY m.nombre) AS detalle
          FROM vino_maridaje vm JOIN maridaje m ON m.id_maridaje = vm.id_maridaje
         WHERE vm.cod_vino = v.cod_vino) mar ON TRUE
 WHERE v.cod_vino = :vino_ref;


-- =============================================================================
-- S10 · Rendimiento (kg/ha) por parcela y campaña (campaña: :campania_ref),
--       comparado con el promedio de su misma cepa en esa campaña.
-- CTE con la cosecha por parcela y SUBCONSULTA CORRELACIONADA para el promedio.
-- =============================================================================
\echo '=== S10 · Rendimiento por parcela, campaña' :campania_ref '(top 15)'
WITH cosecha AS (
    SELECT l.id_finca, l.nro_parcela, l.campania, SUM(l.kg) AS kg
      FROM lote_uva l
     GROUP BY l.id_finca, l.nro_parcela, l.campania
)
SELECT f.nombre AS finca, p.nro_parcela, ce.nombre AS cepa, co.campania,
       ROUND(co.kg / p.superficie_ha)  AS kg_por_ha,
       (SELECT ROUND(AVG(c2.kg / p2.superficie_ha))
          FROM cosecha c2
          JOIN parcela p2 ON p2.id_finca = c2.id_finca AND p2.nro_parcela = c2.nro_parcela
         WHERE c2.campania = co.campania
           AND p2.id_cepa = p.id_cepa)  AS promedio_de_la_cepa
  FROM cosecha co
  JOIN parcela p ON p.id_finca = co.id_finca AND p.nro_parcela = co.nro_parcela
  JOIN finca f   ON f.id_finca = p.id_finca
  JOIN cepa ce   ON ce.id_cepa = p.id_cepa
 WHERE co.campania = :campania_ref
 ORDER BY kg_por_ha DESC, f.nombre, p.nro_parcela
 LIMIT 15;


-- =============================================================================
-- S11 · Ranking de vinos por sala y ventas acumuladas mensuales (funciones de
--       ventana). Últimos 6 meses; muestra el top 3 de cada sala y mes.
--   RANK()  -> puesto del vino dentro de su sala y mes (por unidades);
--   SUM() OVER (... ORDER BY mes) -> unidades acumuladas del vino en esa sala.
-- El acumulado se calcula ANTES de filtrar el top 3, por eso va en subconsulta.
-- =============================================================================
\echo '=== S11 · Ranking mensual de vinos por sala (top 3, 6 meses) · primeras 15 filas'
SELECT *
  FROM (
        SELECT m.id_sala, m.mes, v.nombre AS vino, m.unidades,
               SUM(m.unidades) OVER (PARTITION BY m.id_sala, m.cod_vino ORDER BY m.mes) AS unidades_acumuladas,
               RANK()          OVER (PARTITION BY m.id_sala, m.mes ORDER BY m.unidades DESC, m.cod_vino) AS puesto
          FROM (SELECT c.id_sala, date_trunc('month', c.fecha)::DATE AS mes, r.cod_vino,
                       SUM(r.cantidad) AS unidades
                  FROM comprobante c
                  JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
                 WHERE c.fecha >= date_trunc('month', CURRENT_DATE) - INTERVAL '5 months'
                 GROUP BY c.id_sala, date_trunc('month', c.fecha), r.cod_vino) m
          JOIN vino v ON v.cod_vino = m.cod_vino
       ) ranking
 WHERE puesto <= 3
 ORDER BY id_sala, mes, puesto
 LIMIT 15;


-- =============================================================================
-- S12a · Clientes que compraron TODOS los vinos de una bodega (:bodega_ref, la de
--        menos vinos). División relacional con NOT EXISTS doble.
-- Con los datos generados nadie cumple (la mayor compra cubre 8 de 14 vinos), así
-- que la demostración arma, dentro de una transacción con ROLLBACK, un cliente que
-- sí los compró todos.
-- =============================================================================
\echo '=== S12a · Clientes que compraron todos los vinos de la bodega' :bodega_ref
SELECT cl.id_cliente, cl.nombre_razon_social AS resultado_con_los_datos_reales
  FROM cliente cl
 WHERE NOT EXISTS (
         SELECT 1 FROM vino v
          WHERE v.cuit_bodega = :'bodega_ref'
            AND NOT EXISTS (
                  SELECT 1 FROM comprobante c
                  JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
                   WHERE c.id_cliente = cl.id_cliente AND r.cod_vino = v.cod_vino));

\echo '--- demostración: se crea un cliente que compra los 14 vinos (ROLLBACK al final)'
BEGIN;
INSERT INTO stock_sala (id_sala, cod_vino, cantidad)
SELECT :sala_ref, cod_vino, 100 FROM vino WHERE cuit_bodega = :'bodega_ref'
ON CONFLICT (id_sala, cod_vino) DO UPDATE SET cantidad = 100;
INSERT INTO comprobante (id_cliente, id_sala) VALUES (1, :sala_ref) RETURNING nro_comprobante AS nro_s12 \gset
INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad)
SELECT :nro_s12, cod_vino, 1 FROM vino WHERE cuit_bodega = :'bodega_ref';

SELECT cl.id_cliente, cl.nombre_razon_social AS resultado_de_la_demostracion
  FROM cliente cl
 WHERE NOT EXISTS (
         SELECT 1 FROM vino v
          WHERE v.cuit_bodega = :'bodega_ref'
            AND NOT EXISTS (
                  SELECT 1 FROM comprobante c
                  JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
                   WHERE c.id_cliente = cl.id_cliente AND r.cod_vino = v.cod_vino));
ROLLBACK;


-- =============================================================================
-- S12b · Clientes sin compras de vino tinto (anti-join con NOT EXISTS).
-- Resumen por tipo de cliente y una muestra de 10.
-- =============================================================================
\echo '=== S12b · Clientes que nunca compraron vino tinto'
WITH sin_tinto AS (
    SELECT cl.id_cliente, cl.nombre_razon_social, cl.tipo_cliente
      FROM cliente cl
     WHERE NOT EXISTS (
             SELECT 1
               FROM comprobante c
               JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
               JOIN vino v ON v.cod_vino = r.cod_vino
              WHERE c.id_cliente = cl.id_cliente AND v.tipo = 'tinto')
)
SELECT tipo_cliente, COUNT(*) AS clientes_sin_compras_de_tinto
  FROM sin_tinto GROUP BY tipo_cliente ORDER BY tipo_cliente;

SELECT cl.id_cliente, cl.nombre_razon_social, cl.tipo_cliente
  FROM cliente cl
 WHERE NOT EXISTS (
         SELECT 1
           FROM comprobante c
           JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
           JOIN vino v ON v.cod_vino = r.cod_vino
          WHERE c.id_cliente = cl.id_cliente AND v.tipo = 'tinto')
 ORDER BY cl.id_cliente
 LIMIT 10;

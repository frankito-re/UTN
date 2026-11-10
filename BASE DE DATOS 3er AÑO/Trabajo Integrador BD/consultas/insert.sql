-- =============================================================================
-- consultas/insert.sql · Inserción de datos (I1 a I6) · Bodegas del Atuel
--
-- Ejecutar con psql (usa \echo y \gset):
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB' < consultas/insert.sql
--
-- Cada consulta corre en su propia transacción y termina en ROLLBACK: se puede
-- ejecutar el archivo entero sin alterar los datos. Para aplicar una de verdad,
-- cambiar su ROLLBACK por COMMIT. La sentencia a evaluar es la marcada «-- I<n>».
-- =============================================================================
\set ON_ERROR_STOP on
\pset pager off


-- =============================================================================
-- I1 · Asociar la cobertura de General Alvear al transportista con MENOS envíos
--      en el último trimestre (envío = ingreso transportado).
-- Entre los transportistas que todavía no la cubren, así la inserción siempre es
-- efectiva; los que no tuvieron ningún envío cuentan como 0.
-- =============================================================================
\echo '=== I1 · Cobertura de General Alvear para el transportista menos activo'
BEGIN;
-- I1
INSERT INTO cobertura_transportista (cod_transportista, cod_postal)
SELECT t.cod_transportista, l.cod_postal
  FROM transportista t
  JOIN localidad l ON l.nombre = 'General Alvear' AND l.provincia = 'Mendoza'
  LEFT JOIN ingreso i ON i.cod_transportista = t.cod_transportista
                     AND i.fecha >= CURRENT_DATE - INTERVAL '3 months'
 WHERE NOT EXISTS (SELECT 1 FROM cobertura_transportista c
                    WHERE c.cod_transportista = t.cod_transportista AND c.cod_postal = l.cod_postal)
 GROUP BY t.cod_transportista, l.cod_postal
 ORDER BY COUNT(i.cod_ingreso), t.cod_transportista
 LIMIT 1
RETURNING cod_transportista, cod_postal;

SELECT t.cod_transportista, t.razon_social,
       (SELECT COUNT(*) FROM ingreso i WHERE i.cod_transportista = t.cod_transportista
           AND i.fecha >= CURRENT_DATE - INTERVAL '3 months') AS envios_ultimo_trimestre
  FROM cobertura_transportista c
  JOIN transportista t USING (cod_transportista)
  JOIN localidad l ON l.cod_postal = c.cod_postal
 WHERE l.nombre = 'General Alvear'
 ORDER BY envios_ultimo_trimestre, t.cod_transportista;
ROLLBACK;


-- =============================================================================
-- I2 · Crear el maridaje «Cordero al disco» y asociarlo a todos los vinos tintos
--      con graduación mayor o igual a 14°. Una sola sentencia (CTE con INSERT).
-- =============================================================================
\echo '=== I2 · Maridaje «Cordero al disco» para tintos de 14° o más'
BEGIN;
-- I2
WITH nuevo AS (
    INSERT INTO maridaje (nombre, temperatura_servicio)
    VALUES ('Cordero al disco', 17)
    RETURNING id_maridaje
)
INSERT INTO vino_maridaje (cod_vino, id_maridaje)
SELECT v.cod_vino, n.id_maridaje
  FROM vino v CROSS JOIN nuevo n
 WHERE v.tipo = 'tinto' AND v.graduacion >= 14;

SELECT m.nombre, m.temperatura_servicio, count(*) AS vinos_asociados,
       min(v.graduacion) AS graduacion_minima, bool_and(v.tipo = 'tinto') AS todos_tintos
  FROM maridaje m
  JOIN vino_maridaje vm USING (id_maridaje)
  JOIN vino v USING (cod_vino)
 WHERE m.nombre = 'Cordero al disco'
 GROUP BY m.nombre, m.temperatura_servicio;
ROLLBACK;


-- =============================================================================
-- I3 · Crear un comprobante con 3 renglones dentro de una transacción.
-- Solo se informan cliente, sala, vinos y cantidades: precio, descuento del
-- cliente, subtotales y total los calcula la base (RN-06, RN-08) y el stock de la
-- sala se descuenta (RN-09). Si algún renglón no tuviera stock, falla TODO el
-- comprobante (RN-09) y no queda nada a medias.
-- Parámetros de la demostración: una sala con 3 vinos con stock y un socio.
-- =============================================================================
\echo '=== I3 · Comprobante con 3 renglones'
SELECT id_sala AS sala_i3,
       (array_agg(cod_vino ORDER BY cantidad DESC, cod_vino))[1] AS vino1,
       (array_agg(cod_vino ORDER BY cantidad DESC, cod_vino))[2] AS vino2,
       (array_agg(cod_vino ORDER BY cantidad DESC, cod_vino))[3] AS vino3
  FROM stock_sala WHERE cantidad >= 5
 GROUP BY id_sala HAVING count(*) >= 3
 ORDER BY id_sala LIMIT 1 \gset
SELECT id_cliente AS cliente_i3 FROM cliente WHERE tipo_cliente = 'socio' ORDER BY id_cliente LIMIT 1 \gset

BEGIN;
SELECT cod_vino, cantidad AS stock_antes FROM stock_sala
 WHERE id_sala = :sala_i3 AND cod_vino IN (:vino1, :vino2, :vino3) ORDER BY cod_vino;

-- I3
INSERT INTO comprobante (id_cliente, id_sala)
VALUES (:cliente_i3, :sala_i3)
RETURNING nro_comprobante AS nro_i3 \gset

INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad)
VALUES (:nro_i3, :vino1, 2),
       (:nro_i3, :vino2, 1),
       (:nro_i3, :vino3, 3);

SELECT nro_comprobante, fecha, subtotal, descuento, total FROM comprobante WHERE nro_comprobante = :nro_i3;
SELECT cod_vino, cantidad, precio_unitario, descuento_pct, subtotal FROM renglon_comprobante
 WHERE nro_comprobante = :nro_i3 ORDER BY cod_vino;
SELECT cod_vino, cantidad AS stock_despues FROM stock_sala
 WHERE id_sala = :sala_i3 AND cod_vino IN (:vino1, :vino2, :vino3) ORDER BY cod_vino;
ROLLBACK;


-- =============================================================================
-- I4 · Insertar una nueva bodega.
-- =============================================================================
\echo '=== I4 · Nueva bodega'
BEGIN;
-- I4
INSERT INTO bodega (cuit, razon_social, domicilio)
VALUES ('30712345671', 'Bodega Cerros del Atuel S.A.', 'Ruta Provincial 173 km 12, San Rafael, Mendoza');

SELECT * FROM bodega WHERE cuit = '30712345671';
ROLLBACK;


-- =============================================================================
-- I5 · Insertar una nueva sala de venta (en General Alvear).
-- =============================================================================
\echo '=== I5 · Nueva sala de venta'
BEGIN;
-- I5
INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal)
SELECT 'Avenida Hipólito Yrigoyen', 1250, 'domingo', cod_postal
  FROM localidad WHERE nombre = 'General Alvear' AND provincia = 'Mendoza';

SELECT s.id_sala, s.calle, s.numero, s.dia_cierre, l.nombre AS localidad
  FROM sala_venta s JOIN localidad l USING (cod_postal)
 WHERE s.calle = 'Avenida Hipólito Yrigoyen' AND s.numero = 1250;
ROLLBACK;


-- =============================================================================
-- I6 · Crear un ingreso EN CONFECCIÓN de 120 botellas de un vino.
-- El ingreso nace en_confeccion (RN-10) y todavía no toca el stock: eso ocurre
-- recién con terminado + CALL sp_procesar_ingreso(...). El transportista es el
-- primero del catálogo y la bodega es la del vino.
-- =============================================================================
\echo '=== I6 · Ingreso en confección de 120 botellas'
SELECT cod_vino AS vino_i6 FROM vino ORDER BY cod_vino LIMIT 1 \gset
BEGIN;
SELECT fn_stock_deposito(:vino_i6) AS stock_deposito_antes;

-- I6
INSERT INTO ingreso (cod_transportista, cuit_bodega)
SELECT (SELECT MIN(cod_transportista) FROM transportista), v.cuit_bodega
  FROM vino v WHERE v.cod_vino = :vino_i6
RETURNING cod_ingreso AS ingreso_i6 \gset

INSERT INTO renglon_ingreso (cod_ingreso, cod_vino, cantidad)
VALUES (:ingreso_i6, :vino_i6, 120);

SELECT i.cod_ingreso, i.fecha, i.estado, r.cod_vino, r.cantidad
  FROM ingreso i JOIN renglon_ingreso r USING (cod_ingreso) WHERE i.cod_ingreso = :ingreso_i6;
SELECT fn_stock_deposito(:vino_i6) AS stock_deposito_despues_sin_procesar;
ROLLBACK;

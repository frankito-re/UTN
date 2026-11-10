-- =============================================================================
-- 008_indices.sql  ·  Bodegas del Atuel  ·  Etapa 4 (Índices y rendimiento)
-- Cada índice responde a una consulta concreta medida con
-- EXPLAIN (ANALYZE, BUFFERS) antes y después (ver docs/informe_indices.md).
--
-- PostgreSQL ya indexa las PK y los UNIQUE de 001/002. NO indexa las columnas
-- de las FK: sin índice, cada DELETE sobre la tabla padre recorre entera la
-- tabla hija para verificar RN-14 (ON DELETE RESTRICT).
--
-- Costo: cada índice se mantiene en cada INSERT/UPDATE/DELETE. Por eso no se
-- indexó todo: solo lo que una consulta de las Etapas 5-7 o una FK de RN-14 usa.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Compuestos
-- -----------------------------------------------------------------------------
-- Ficha de cliente / historial: "últimas N compras de un cliente".
-- (id_cliente, fecha DESC) entrega las filas ya ordenadas: LIMIT corta sin ordenar.
-- Además sirve de índice de la FK comprobante.id_cliente.
CREATE INDEX idx_comprobante_cliente_fecha
    ON comprobante (id_cliente, fecha DESC);

-- Consultas por sala y período (S3, tableros). INCLUDE (total) permite resolver
-- sumas de ventas por sala sin leer la tabla (index-only scan). Es también el
-- índice de la FK comprobante.id_sala.
CREATE INDEX idx_comprobante_sala_fecha
    ON comprobante (id_sala, fecha) INCLUDE (total);

-- Pedidos de un vino a lo largo del tiempo (S4) y verificación RN-14: columna
-- líder cod_vino, con el comprobante de transferencia incluido en la clave y la
-- cantidad como columna cubierta.
CREATE INDEX idx_renglon_transferencia_vino
    ON renglon_transferencia (cod_vino, nro_transferencia) INCLUDE (cantidad);

-- -----------------------------------------------------------------------------
-- Covering (INCLUDE) sobre la tabla más grande
-- -----------------------------------------------------------------------------
-- Ventas por vino (S1, ranking, ventas mensuales de un vino) y verificación de
-- FK al borrar un vino. Con INCLUDE (cantidad) los totales por vino se resuelven
-- solo con el índice, sin tocar renglon_comprobante.
CREATE INDEX idx_renglon_comprobante_vino
    ON renglon_comprobante (cod_vino) INCLUDE (cantidad);

-- -----------------------------------------------------------------------------
-- BRIN
-- -----------------------------------------------------------------------------
-- Los comprobantes se insertan en orden cronológico, así que fecha está
-- físicamente ordenada en el disco. BRIN guarda solo el mínimo y máximo de cada
-- rango de páginas: ocupa una fracción de un B-tree y casi no cuesta en escritura.
-- Sirve a "ventas de un período" sobre toda la red (S8, tablero).
CREATE INDEX brin_comprobante_fecha
    ON comprobante USING brin (fecha) WITH (pages_per_range = 16);

-- -----------------------------------------------------------------------------
-- Parcial
-- -----------------------------------------------------------------------------
-- Casi todas las transferencias están procesadas; las pendientes (en_confeccion
-- y terminado) son pocas y son las que se consultan (S5, pantalla de
-- transferencias). El índice solo contiene esas filas.
CREATE INDEX idx_transferencia_pendientes
    ON transferencia (id_sala) WHERE estado <> 'procesado';

-- -----------------------------------------------------------------------------
-- De expresión
-- -----------------------------------------------------------------------------
-- Autocompletado de clientes sin distinguir mayúsculas: WHERE lower(nombre) LIKE 'gonz%'.
-- text_pattern_ops permite usar el índice con LIKE 'prefijo%' sea cual sea la
-- collation de la base.
CREATE INDEX idx_cliente_nombre_lower
    ON cliente (lower(nombre_razon_social) text_pattern_ops);

-- -----------------------------------------------------------------------------
-- Índices de FK que usan RN-14 y las consultas (el resto de las FK no se indexa:
-- tablas chicas o columnas que nunca se borran ni se filtran)
-- -----------------------------------------------------------------------------
CREATE INDEX idx_renglon_ingreso_vino        ON renglon_ingreso (cod_vino);
CREATE INDEX idx_stock_sala_vino             ON stock_sala (cod_vino);          -- PK es (id_sala, cod_vino)
CREATE INDEX idx_auditoria_precio_vino       ON auditoria_precio (cod_vino, fecha_hora DESC);  -- historial de precios
CREATE INDEX idx_ingreso_transportista_fecha ON ingreso (cod_transportista, fecha);          -- S7 y RN-14
CREATE INDEX idx_ingreso_bodega              ON ingreso (cuit_bodega);                         -- RN-14
CREATE INDEX idx_vino_bodega                 ON vino (cuit_bodega);                            -- U3 y RN-14
CREATE INDEX idx_lote_uva_bodega             ON lote_uva (cuit_bodega);                        -- RN-14
CREATE INDEX idx_empleado_sala               ON empleado (id_sala);                            -- D3, baja de sala

-- -----------------------------------------------------------------------------
-- Configuración del planificador
-- -----------------------------------------------------------------------------
-- random_page_cost viene en 4.0 (pensado para discos giratorios). En SSD y con la
-- base en cache el acceso aleatorio cuesta casi lo mismo que el secuencial; con el
-- valor por defecto el planificador desaprovecha los índices recién creados (ej.:
-- prefiere recorrer 160.000 comprobantes antes que hacer 1.600 búsquedas por PK).
-- Se aplica a toda conexión nueva a esta base. Medido en docs/informe_indices.md.
DO $$
BEGIN
    BEGIN
        EXECUTE format('ALTER DATABASE %I SET random_page_cost = 1.1', current_database());
    EXCEPTION WHEN insufficient_privilege THEN
        RAISE NOTICE 'Sin privilegios para ALTER DATABASE (servicio gestionado): el ajuste queda solo a nivel de rol.';
    END;
END;
$$;

-- Tambien por rol: vale aunque no se pueda cambiar la base (y cubre a las conexiones de la API y de reportes).
ALTER ROLE bodegas_api SET random_page_cost = 1.1;
ALTER ROLE bodegas_ro  SET random_page_cost = 1.1;

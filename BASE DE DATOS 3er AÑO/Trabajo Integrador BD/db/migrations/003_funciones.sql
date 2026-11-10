-- =============================================================================
-- 003_funciones.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Lógica en la base)
-- Funciones de cálculo y consulta. Son la única fuente de verdad de los
-- cálculos: los triggers (005), los procedimientos (004) y la API las invocan,
-- nadie recalcula totales, descuentos ni stock por su cuenta.
--
-- Volatilidad: IMMUTABLE si solo depende de los argumentos; STABLE si lee
-- tablas (no modifica datos).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- RN-06 · Descuento según tipo de cliente
-- -----------------------------------------------------------------------------
-- Devuelve el % base de descuento del tipo. NULL si el tipo no existe (el
-- NOT NULL de cliente.descuento lo rechaza).
CREATE OR REPLACE FUNCTION fn_descuento_tipo_cliente(p_tipo VARCHAR)
RETURNS NUMERIC(5,2)
LANGUAGE sql IMMUTABLE AS $$
    SELECT (CASE p_tipo
                WHEN 'socio'        THEN 10
                WHEN 'distribuidor' THEN 20
                WHEN 'exportador'   THEN 30
            END)::NUMERIC(5,2);
$$;

-- % de descuento vigente de un cliente concreto (puede diferir del base, ej. U6).
CREATE OR REPLACE FUNCTION fn_descuento_cliente(p_id_cliente INTEGER)
RETURNS NUMERIC(5,2)
LANGUAGE sql STABLE AS $$
    SELECT c.descuento FROM cliente c WHERE c.id_cliente = p_id_cliente;
$$;

-- -----------------------------------------------------------------------------
-- RN-08 · Cálculo de renglones y comprobantes
-- -----------------------------------------------------------------------------
-- Subtotal de un renglón: cantidad * precio * (1 - descuento/100), a 2 decimales.
CREATE OR REPLACE FUNCTION fn_subtotal_renglon(
    p_cantidad INTEGER, p_precio NUMERIC, p_descuento_pct NUMERIC)
RETURNS NUMERIC(14,2)
LANGUAGE sql IMMUTABLE AS $$
    SELECT ROUND(p_cantidad * p_precio * (1 - p_descuento_pct / 100), 2)::NUMERIC(14,2);
$$;

-- Subtotal bruto, monto de descuento y total de un comprobante, calculados a
-- partir de sus renglones. Siempre cumple total = subtotal_bruto - monto_descuento.
CREATE OR REPLACE FUNCTION fn_calcular_comprobante(p_nro_comprobante INTEGER)
RETURNS TABLE (subtotal_bruto NUMERIC(14,2), monto_descuento NUMERIC(14,2), total NUMERIC(14,2))
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(SUM(r.cantidad * r.precio_unitario), 0)::NUMERIC(14,2),
           (COALESCE(SUM(r.cantidad * r.precio_unitario), 0)
            - COALESCE(SUM(r.subtotal), 0))::NUMERIC(14,2),
           COALESCE(SUM(r.subtotal), 0)::NUMERIC(14,2)
    FROM renglon_comprobante r
    WHERE r.nro_comprobante = p_nro_comprobante;
$$;

CREATE OR REPLACE FUNCTION fn_total_comprobante(p_nro_comprobante INTEGER)
RETURNS NUMERIC(14,2)
LANGUAGE sql STABLE AS $$
    SELECT c.total FROM fn_calcular_comprobante(p_nro_comprobante) c;
$$;

-- -----------------------------------------------------------------------------
-- RN-09 · Stock (0 si no hay fila: "sin registro" equivale a "sin stock")
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_stock_sala(p_id_sala INTEGER, p_cod_vino INTEGER)
RETURNS INTEGER
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(
        (SELECT s.cantidad FROM stock_sala s
          WHERE s.id_sala = p_id_sala AND s.cod_vino = p_cod_vino), 0);
$$;

CREATE OR REPLACE FUNCTION fn_stock_deposito(p_cod_vino INTEGER)
RETURNS INTEGER
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(
        (SELECT d.cantidad FROM stock_deposito d WHERE d.cod_vino = p_cod_vino), 0);
$$;

-- -----------------------------------------------------------------------------
-- RN-05 · Suma de porcentajes del corte de un vino (la usa el constraint trigger)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION fn_suma_composicion(p_cod_vino INTEGER)
RETURNS NUMERIC(6,2)
LANGUAGE sql STABLE AS $$
    SELECT COALESCE(SUM(c.porcentaje), 0)::NUMERIC(6,2)
    FROM composicion c WHERE c.cod_vino = p_cod_vino;
$$;

-- -----------------------------------------------------------------------------
-- RN-10 / RN-11 · Transiciones válidas de estado
-- -----------------------------------------------------------------------------
-- Solo en_confeccion -> terminado -> procesado. Quedarse en el mismo estado NO
-- es una transición: el trigger decide qué hacer en ese caso.
CREATE OR REPLACE FUNCTION fn_transicion_estado_valida(
    p_anterior estado_documento, p_nuevo estado_documento)
RETURNS BOOLEAN
LANGUAGE sql IMMUTABLE AS $$
    SELECT (p_anterior = 'en_confeccion' AND p_nuevo = 'terminado')
        OR (p_anterior = 'terminado'     AND p_nuevo = 'procesado');
$$;

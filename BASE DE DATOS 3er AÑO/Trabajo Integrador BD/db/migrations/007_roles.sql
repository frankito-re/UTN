-- =============================================================================
-- 007_roles.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Seguridad)
-- Tres roles con privilegios mínimos:
--
--   bodegas_owner  PROPIETARIO. Es el usuario POSTGRES_USER del contenedor: crea
--                  el esquema, corre las migraciones y es dueño de todos los
--                  objetos. Nunca lo usa la aplicación.
--   bodegas_api    LECTURA/ESCRITURA para la API REST. Hace CRUD de datos de
--                  negocio y llama funciones y procedimientos. NO escribe stock
--                  ni auditoría directamente (solo los triggers de venta y
--                  sp_procesar_* lo hacen, con SECURITY DEFINER), no hace DDL
--                  ni TRUNCATE.
--   bodegas_ro     SOLO LECTURA para reportes (tablas, vistas y materializada).
--
-- Las CLAVES no están en este archivo (el repositorio es público): las pone
-- 090_roles_passwords.sh a partir de variables de entorno del archivo .env.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Creación de roles (idempotente)
-- -----------------------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bodegas_api') THEN
        CREATE ROLE bodegas_api LOGIN
            NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION CONNECTION LIMIT 20;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bodegas_ro') THEN
        CREATE ROLE bodegas_ro LOGIN
            NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION CONNECTION LIMIT 10;
    END IF;
END;
$$;

-- Topes de seguridad por rol: consultas colgadas no acaparan la base y el rol de
-- reportes no puede escribir ni por error.
ALTER ROLE bodegas_api SET statement_timeout = '30s';
ALTER ROLE bodegas_ro  SET statement_timeout = '30s';
ALTER ROLE bodegas_ro  SET default_transaction_read_only = on;

-- -----------------------------------------------------------------------------
-- Cerrar lo que PUBLIC recibe por defecto y abrir solo lo necesario
-- -----------------------------------------------------------------------------
DO $$
BEGIN
    EXECUTE format('REVOKE ALL ON DATABASE %I FROM PUBLIC', current_database());
    EXECUTE format('GRANT CONNECT ON DATABASE %I TO bodegas_api, bodegas_ro', current_database());
END;
$$;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO bodegas_api, bodegas_ro;

-- Por defecto cualquiera puede ejecutar cualquier funcion: se cierra, tambien
-- para las que se creen mas adelante.
REVOKE ALL ON ALL ROUTINES IN SCHEMA public FROM PUBLIC;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON ROUTINES FROM PUBLIC;

-- -----------------------------------------------------------------------------
-- bodegas_api · lectura y escritura de datos de negocio
-- -----------------------------------------------------------------------------
GRANT SELECT, INSERT, UPDATE, DELETE ON
    localidad, sala_venta, empleado,
    finca, parcela, cepa, lote_uva, analisis_calidad,
    bodega, vino, composicion, maridaje, vino_maridaje,
    cliente, socio, distribuidor, exportador, permiso_exportacion,
    comprobante, renglon_comprobante,
    transportista, cobertura_transportista,
    ingreso, renglon_ingreso, transferencia, renglon_transferencia
TO bodegas_api;

-- Stock y auditoria: solo lectura. Cambian unicamente por los triggers de venta,
-- por los procedimientos sp_procesar_* y por el trigger de precio.
GRANT SELECT ON stock_sala, stock_deposito, auditoria_precio TO bodegas_api;

GRANT SELECT ON v_stock_vino, v_catalogo_vino, v_comprobante_detalle,
                mv_ventas_mensuales_sala TO bodegas_api;

-- Claves generadas (identity) de las tablas en las que inserta.
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO bodegas_api;

-- Funciones de calculo y procedimientos que la API invoca (la API no recalcula).
GRANT EXECUTE ON FUNCTION
    fn_descuento_tipo_cliente(VARCHAR),
    fn_descuento_cliente(INTEGER),
    fn_subtotal_renglon(INTEGER, NUMERIC, NUMERIC),
    fn_calcular_comprobante(INTEGER),
    fn_total_comprobante(INTEGER),
    fn_stock_sala(INTEGER, INTEGER),
    fn_stock_deposito(INTEGER),
    fn_suma_composicion(INTEGER),
    fn_transicion_estado_valida(estado_documento, estado_documento)
TO bodegas_api, bodegas_ro;

GRANT EXECUTE ON PROCEDURE
    sp_procesar_ingreso(INTEGER),
    sp_procesar_transferencia(INTEGER),
    sp_refrescar_reportes()
TO bodegas_api;

-- -----------------------------------------------------------------------------
-- bodegas_ro · solo lectura para reportes
-- -----------------------------------------------------------------------------
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bodegas_ro;   -- incluye vistas y materializada
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO bodegas_ro;

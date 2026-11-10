-- =============================================================================
-- 002_constraints.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Integridad)
-- UNIQUE, CHECK y DEFAULT. Las PK, FK y NOT NULL están en 001_esquema.sql.
-- Cada constraint nombra la regla de negocio (RN-xx) que implementa.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- UNIQUE
-- -----------------------------------------------------------------------------
-- RN-04: máximo una cosecha por parcela y campaña.
ALTER TABLE lote_uva
    ADD CONSTRAINT uq_lote_parcela_campania UNIQUE (id_finca, nro_parcela, campania);

-- Un mismo vino (nombre, añada, presentación) no se registra dos veces.
ALTER TABLE vino
    ADD CONSTRAINT uq_vino_nombre_anada_volumen UNIQUE (nombre, anada, volumen_ml);

ALTER TABLE cliente
    ADD CONSTRAINT uq_cliente_documento UNIQUE (tipo_doc, nro_doc);

ALTER TABLE transportista
    ADD CONSTRAINT uq_transportista_cuit UNIQUE (cuit);

ALTER TABLE distribuidor
    ADD CONSTRAINT uq_distribuidor_habilitacion UNIQUE (nro_habilitacion);

ALTER TABLE cepa
    ADD CONSTRAINT uq_cepa_nombre UNIQUE (nombre);

ALTER TABLE maridaje
    ADD CONSTRAINT uq_maridaje_nombre UNIQUE (nombre);

ALTER TABLE sala_venta
    ADD CONSTRAINT uq_sala_direccion UNIQUE (calle, numero, cod_postal);

ALTER TABLE localidad
    ADD CONSTRAINT uq_localidad_nombre_prov UNIQUE (nombre, provincia);

-- -----------------------------------------------------------------------------
-- CHECK
-- -----------------------------------------------------------------------------
-- Módulo A
ALTER TABLE sala_venta
    ADD CONSTRAINT ck_sala_numero_pos CHECK (numero > 0),                           -- RN-15
    ADD CONSTRAINT ck_sala_dia_cierre CHECK (dia_cierre IN
        ('lunes','martes','miercoles','jueves','viernes','sabado','domingo'));

ALTER TABLE empleado
    ADD CONSTRAINT ck_empleado_salario_pos CHECK (salario > 0);                     -- RN-15

-- Módulo B
ALTER TABLE finca
    ADD CONSTRAINT ck_finca_superficie_pos CHECK (superficie_ha > 0);               -- RN-15

ALTER TABLE cepa
    ADD CONSTRAINT ck_cepa_tipo CHECK (tipo IN ('tinta','blanca'));

ALTER TABLE parcela
    ADD CONSTRAINT ck_parcela_nro_pos         CHECK (nro_parcela > 0),
    ADD CONSTRAINT ck_parcela_superficie_pos  CHECK (superficie_ha > 0),            -- RN-15
    ADD CONSTRAINT ck_parcela_anio_plantacion CHECK (anio_plantacion BETWEEN 1900 AND 2100);

ALTER TABLE lote_uva
    ADD CONSTRAINT ck_lote_kg_pos       CHECK (kg > 0),                             -- RN-15
    ADD CONSTRAINT ck_lote_campania     CHECK (campania BETWEEN 1990 AND 2100);

ALTER TABLE analisis_calidad
    ADD CONSTRAINT ck_analisis_brix     CHECK (brix BETWEEN 0 AND 40),
    ADD CONSTRAINT ck_analisis_ph       CHECK (ph > 0 AND ph < 14),
    ADD CONSTRAINT ck_analisis_acidez   CHECK (acidez_total > 0);

ALTER TABLE vino
    ADD CONSTRAINT ck_vino_tipo         CHECK (tipo IN ('tinto','blanco','rosado','espumante')),
    ADD CONSTRAINT ck_vino_anada        CHECK (anada BETWEEN 1990 AND 2100),
    ADD CONSTRAINT ck_vino_volumen      CHECK (volumen_ml IN (375, 750, 1500)),
    ADD CONSTRAINT ck_vino_graduacion   CHECK (graduacion BETWEEN 5 AND 20),        -- RN-15
    ADD CONSTRAINT ck_vino_precio_pos   CHECK (precio > 0);                         -- RN-01

ALTER TABLE composicion
    ADD CONSTRAINT ck_composicion_pct   CHECK (porcentaje > 0 AND porcentaje <= 100); -- RN-05 (suma: trigger)

ALTER TABLE maridaje
    ADD CONSTRAINT ck_maridaje_temp     CHECK (temperatura_servicio BETWEEN 0 AND 30);

-- Módulo C
ALTER TABLE cliente
    ADD CONSTRAINT ck_cliente_tipo_doc  CHECK (tipo_doc IN ('DNI','CUIT','CUIL','PASAPORTE')),
    ADD CONSTRAINT ck_cliente_tipo      CHECK (tipo_cliente IN ('socio','distribuidor','exportador')),
    ADD CONSTRAINT ck_cliente_descuento CHECK (descuento BETWEEN 0 AND 100);        -- RN-06

-- Cada subtipo solo puede apuntar a clientes de su propio tipo (jerarquía disjunta).
ALTER TABLE socio
    ADD CONSTRAINT ck_socio_tipo        CHECK (tipo_cliente = 'socio');
ALTER TABLE distribuidor
    ADD CONSTRAINT ck_distribuidor_tipo CHECK (tipo_cliente = 'distribuidor');
ALTER TABLE exportador
    ADD CONSTRAINT ck_exportador_tipo   CHECK (tipo_cliente = 'exportador');

ALTER TABLE permiso_exportacion
    ADD CONSTRAINT ck_permiso_fechas    CHECK (fecha_vencimiento > fecha_emision);  -- RN-07

ALTER TABLE comprobante
    ADD CONSTRAINT ck_comprobante_montos CHECK (subtotal >= 0 AND descuento >= 0 AND descuento <= subtotal),
    ADD CONSTRAINT ck_comprobante_total  CHECK (total = subtotal - descuento);      -- RN-08

ALTER TABLE renglon_comprobante
    ADD CONSTRAINT ck_renglon_cantidad_pos CHECK (cantidad > 0),                    -- RN-15
    ADD CONSTRAINT ck_renglon_precio_pos   CHECK (precio_unitario > 0),             -- RN-15
    ADD CONSTRAINT ck_renglon_descuento    CHECK (descuento_pct BETWEEN 0 AND 100), -- RN-06
    ADD CONSTRAINT ck_renglon_subtotal     CHECK (subtotal >= 0);

-- Módulo D
ALTER TABLE transportista
    ADD CONSTRAINT ck_transportista_email  CHECK (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$');

ALTER TABLE renglon_ingreso
    ADD CONSTRAINT ck_renglon_ingreso_cantidad CHECK (cantidad > 0);                -- RN-15
ALTER TABLE renglon_transferencia
    ADD CONSTRAINT ck_renglon_transf_cantidad  CHECK (cantidad > 0);                -- RN-15

ALTER TABLE stock_sala
    ADD CONSTRAINT ck_stock_sala_no_neg     CHECK (cantidad >= 0);                  -- RN-09
ALTER TABLE stock_deposito
    ADD CONSTRAINT ck_stock_deposito_no_neg CHECK (cantidad >= 0);                  -- RN-09

ALTER TABLE auditoria_precio
    ADD CONSTRAINT ck_auditoria_precios CHECK (precio_anterior > 0 AND precio_nuevo > 0
                                               AND precio_anterior <> precio_nuevo);

-- -----------------------------------------------------------------------------
-- DEFAULT
-- -----------------------------------------------------------------------------
ALTER TABLE ingreso
    ALTER COLUMN fecha  SET DEFAULT CURRENT_DATE,
    ALTER COLUMN estado SET DEFAULT 'en_confeccion';                                -- RN-10

ALTER TABLE transferencia
    ALTER COLUMN fecha_confeccion SET DEFAULT CURRENT_DATE,                         -- RN-11
    ALTER COLUMN estado           SET DEFAULT 'en_confeccion';

ALTER TABLE comprobante
    ALTER COLUMN fecha     SET DEFAULT CURRENT_DATE,
    ALTER COLUMN subtotal  SET DEFAULT 0,                                           -- RN-08: los recalcula un trigger
    ALTER COLUMN descuento SET DEFAULT 0,
    ALTER COLUMN total     SET DEFAULT 0;

ALTER TABLE renglon_comprobante
    ALTER COLUMN descuento_pct SET DEFAULT 0;

ALTER TABLE cliente
    ALTER COLUMN fecha_alta SET DEFAULT CURRENT_DATE;

ALTER TABLE stock_sala
    ALTER COLUMN cantidad SET DEFAULT 0;
ALTER TABLE stock_deposito
    ALTER COLUMN cantidad SET DEFAULT 0;

ALTER TABLE auditoria_precio
    ALTER COLUMN fecha_hora SET DEFAULT now(),                                      -- RN-13
    ALTER COLUMN usuario    SET DEFAULT current_user;

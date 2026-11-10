-- =============================================================================
-- 001_esquema.sql  ·  Bodegas del Atuel  ·  Etapa 1 (Modelado)
-- Tipos, dominios y tablas con PK, FK y NOT NULL.
-- UNIQUE, CHECK y DEFAULT adicionales se agregan en 002_constraints.sql.
--
-- Convenciones: snake_case en español sin tildes ni ñ (anada, campania),
-- una PK por tabla (identity cuando es clave subrogada), FKs justificadas:
--   * RESTRICT  -> la fila referenciada no puede borrarse si hay dependientes
--                  (RN-14 y datos maestros).
--   * CASCADE   -> el dependiente no tiene sentido sin su padre
--                  (renglones, parcelas de una finca, permisos, etc.).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Tipos y dominios
-- -----------------------------------------------------------------------------
CREATE TYPE estado_documento AS ENUM ('en_confeccion', 'terminado', 'procesado');

CREATE DOMAIN cuit_dom AS CHAR(11)
    CHECK (VALUE ~ '^[0-9]{11}$');

-- =============================================================================
-- Módulo A · Estructura geográfica y personal
-- =============================================================================

-- RN-02: un único encargado regional por localidad -> atributo de localidad
-- (depende solo de la clave de localidad, por eso respeta 3FN).
CREATE TABLE localidad (
    cod_postal          VARCHAR(8)   PRIMARY KEY,
    nombre              VARCHAR(80)  NOT NULL,
    provincia           VARCHAR(60)  NOT NULL,
    encargado_regional  VARCHAR(100) NOT NULL
);

CREATE TABLE sala_venta (
    id_sala     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    calle       VARCHAR(80)  NOT NULL,
    numero      INTEGER      NOT NULL,
    dia_cierre  VARCHAR(10)  NOT NULL,
    cod_postal  VARCHAR(8)   NOT NULL
        REFERENCES localidad (cod_postal) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- RN-03: cada empleado trabaja en una sola sala (FK NOT NULL).
CREATE TABLE empleado (
    cuit           cuit_dom     PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    fecha_ingreso  DATE         NOT NULL,
    salario        NUMERIC(12,2) NOT NULL,
    id_sala        INTEGER      NOT NULL
        REFERENCES sala_venta (id_sala) ON DELETE RESTRICT
);

-- =============================================================================
-- Módulo B · Producción agrícola y enológica
-- =============================================================================

CREATE TABLE finca (
    id_finca      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        VARCHAR(80)   NOT NULL,
    superficie_ha NUMERIC(10,2) NOT NULL,
    departamento  VARCHAR(60)   NOT NULL,
    provincia     VARCHAR(60)   NOT NULL
);

CREATE TABLE cepa (
    id_cepa  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre   VARCHAR(60) NOT NULL,
    tipo     VARCHAR(10) NOT NULL
);

CREATE TABLE bodega (
    cuit          cuit_dom     PRIMARY KEY,
    razon_social  VARCHAR(120) NOT NULL,
    domicilio     VARCHAR(160) NOT NULL
);

-- Entidad débil de finca: clave (id_finca, nro_parcela).
-- CASCADE: si se elimina la finca desaparecen sus parcelas (salvo que ya tengan
-- lotes cosechados, que las protegen con RESTRICT).
-- RN-04: una parcela tiene una sola cepa (id_cepa NOT NULL).
CREATE TABLE parcela (
    id_finca         INTEGER  NOT NULL
        REFERENCES finca (id_finca) ON DELETE CASCADE ON UPDATE CASCADE,
    nro_parcela      INTEGER  NOT NULL,
    superficie_ha    NUMERIC(10,2) NOT NULL,
    anio_plantacion  SMALLINT NOT NULL,
    id_cepa          INTEGER  NOT NULL
        REFERENCES cepa (id_cepa) ON DELETE RESTRICT,
    PRIMARY KEY (id_finca, nro_parcela)
);

-- RN-04: máximo una cosecha por parcela y campaña (UNIQUE en 002).
CREATE TABLE lote_uva (
    nro_lote       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_finca       INTEGER  NOT NULL,
    nro_parcela    INTEGER  NOT NULL,
    campania       SMALLINT NOT NULL,
    fecha_cosecha  DATE     NOT NULL,
    kg             NUMERIC(12,2) NOT NULL,
    cuit_bodega    cuit_dom NOT NULL
        REFERENCES bodega (cuit) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_finca, nro_parcela)
        REFERENCES parcela (id_finca, nro_parcela) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE analisis_calidad (
    id_analisis    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nro_lote       INTEGER NOT NULL
        REFERENCES lote_uva (nro_lote) ON DELETE CASCADE,
    fecha          DATE    NOT NULL,
    brix           NUMERIC(4,1) NOT NULL,
    ph             NUMERIC(3,2) NOT NULL,
    acidez_total   NUMERIC(4,2) NOT NULL   -- g/L
);

-- RN-01 / RN-15: precio > 0, graduación 5..20 (CHECK en 002).
-- RN-14: no se borra un vino con movimientos (todas las FK hacia vino son RESTRICT,
-- salvo composicion y vino_maridaje que son atributos propios del vino).
CREATE TABLE vino (
    cod_vino     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre       VARCHAR(80)   NOT NULL,
    tipo         VARCHAR(12)   NOT NULL,
    anada        SMALLINT      NOT NULL,
    volumen_ml   INTEGER       NOT NULL,
    graduacion   NUMERIC(4,2)  NOT NULL,
    precio       NUMERIC(10,2) NOT NULL,
    cuit_bodega  cuit_dom      NOT NULL
        REFERENCES bodega (cuit) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Relación N:M Vino-Cepa con atributo. RN-05 (suma = 100) -> constraint trigger.
CREATE TABLE composicion (
    cod_vino    INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE CASCADE,
    id_cepa     INTEGER NOT NULL
        REFERENCES cepa (id_cepa) ON DELETE RESTRICT,
    porcentaje  NUMERIC(5,2) NOT NULL,
    PRIMARY KEY (cod_vino, id_cepa)
);

CREATE TABLE maridaje (
    id_maridaje           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre                VARCHAR(80)  NOT NULL,
    temperatura_servicio  NUMERIC(4,1) NOT NULL   -- °C
);

CREATE TABLE vino_maridaje (
    cod_vino     INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE CASCADE,
    id_maridaje  INTEGER NOT NULL
        REFERENCES maridaje (id_maridaje) ON DELETE CASCADE,
    PRIMARY KEY (cod_vino, id_maridaje)
);

-- =============================================================================
-- Módulo C · Clientes, ventas y comercialización
-- =============================================================================

-- Jerarquía disjunta y total. El discriminador tipo_cliente + la FK compuesta
-- desde cada subtipo evita que un cliente figure en dos subtipos.
-- 'descuento' (%) se completa por trigger a partir del tipo (RN-06) y puede
-- modificarse luego (consulta U6).
CREATE TABLE cliente (
    id_cliente            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_razon_social   VARCHAR(120) NOT NULL,
    tipo_doc              VARCHAR(10)  NOT NULL,
    nro_doc               VARCHAR(20)  NOT NULL,
    direccion             VARCHAR(160) NOT NULL,
    cod_postal            VARCHAR(8)   NOT NULL
        REFERENCES localidad (cod_postal) ON DELETE RESTRICT ON UPDATE CASCADE,
    fecha_alta            DATE         NOT NULL,
    tipo_cliente          VARCHAR(12)  NOT NULL,
    descuento             NUMERIC(5,2) NOT NULL,
    UNIQUE (id_cliente, tipo_cliente)   -- destino de las FK compuestas de los subtipos
);

CREATE TABLE socio (
    id_cliente    INTEGER     PRIMARY KEY,
    tipo_cliente  VARCHAR(12) NOT NULL DEFAULT 'socio',
    FOREIGN KEY (id_cliente, tipo_cliente)
        REFERENCES cliente (id_cliente, tipo_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE distribuidor (
    id_cliente        INTEGER      PRIMARY KEY,
    tipo_cliente      VARCHAR(12)  NOT NULL DEFAULT 'distribuidor',
    zona_cobertura    VARCHAR(100) NOT NULL,
    nro_habilitacion  VARCHAR(30)  NOT NULL,
    FOREIGN KEY (id_cliente, tipo_cliente)
        REFERENCES cliente (id_cliente, tipo_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE exportador (
    id_cliente    INTEGER      PRIMARY KEY,
    tipo_cliente  VARCHAR(12)  NOT NULL DEFAULT 'exportador',
    pais_destino  VARCHAR(60)  NOT NULL,
    FOREIGN KEY (id_cliente, tipo_cliente)
        REFERENCES cliente (id_cliente, tipo_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

-- RN-07: un exportador puede tener varios permisos.
CREATE TABLE permiso_exportacion (
    cod_permiso        VARCHAR(30) PRIMARY KEY,
    id_cliente         INTEGER NOT NULL
        REFERENCES exportador (id_cliente) ON DELETE CASCADE,
    fecha_emision      DATE NOT NULL,
    fecha_vencimiento  DATE NOT NULL
);

-- RN-08: subtotal, descuento (monto $) y total los calcula la base (trigger).
--   subtotal  = sum(cantidad * precio_unitario)
--   descuento = subtotal - sum(renglon.subtotal)
--   total     = subtotal - descuento
CREATE TABLE comprobante (
    nro_comprobante  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha            DATE NOT NULL,
    id_cliente       INTEGER NOT NULL
        REFERENCES cliente (id_cliente) ON DELETE RESTRICT,
    id_sala          INTEGER NOT NULL
        REFERENCES sala_venta (id_sala) ON DELETE RESTRICT,
    subtotal         NUMERIC(14,2) NOT NULL,
    descuento        NUMERIC(14,2) NOT NULL,
    total            NUMERIC(14,2) NOT NULL
);

-- descuento_pct = % aplicado al renglón; subtotal = cantidad * precio * (1 - pct/100).
CREATE TABLE renglon_comprobante (
    nro_comprobante  INTEGER NOT NULL
        REFERENCES comprobante (nro_comprobante) ON DELETE CASCADE,
    cod_vino         INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad         INTEGER       NOT NULL,
    precio_unitario  NUMERIC(10,2) NOT NULL,
    descuento_pct    NUMERIC(5,2)  NOT NULL,
    subtotal         NUMERIC(14,2) NOT NULL,
    PRIMARY KEY (nro_comprobante, cod_vino)
);

-- =============================================================================
-- Módulo D · Inventario, logística y auditoría
-- =============================================================================

CREATE TABLE transportista (
    cod_transportista  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    razon_social       VARCHAR(120) NOT NULL,
    cuit               cuit_dom     NOT NULL,
    email              VARCHAR(120) NOT NULL,
    telefono           VARCHAR(30)  NOT NULL,
    domicilio          VARCHAR(160) NOT NULL
);

CREATE TABLE cobertura_transportista (
    cod_transportista  INTEGER NOT NULL
        REFERENCES transportista (cod_transportista) ON DELETE CASCADE,
    cod_postal         VARCHAR(8) NOT NULL
        REFERENCES localidad (cod_postal) ON DELETE RESTRICT ON UPDATE CASCADE,
    PRIMARY KEY (cod_transportista, cod_postal)
);

-- RN-10: transiciones en_confeccion -> terminado -> procesado (trigger en 005).
CREATE TABLE ingreso (
    cod_ingreso        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha              DATE NOT NULL,
    estado             estado_documento NOT NULL,
    cod_transportista  INTEGER NOT NULL
        REFERENCES transportista (cod_transportista) ON DELETE RESTRICT,
    cuit_bodega        cuit_dom NOT NULL
        REFERENCES bodega (cuit) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE renglon_ingreso (
    cod_ingreso  INTEGER NOT NULL
        REFERENCES ingreso (cod_ingreso) ON DELETE CASCADE,
    cod_vino     INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad     INTEGER NOT NULL,
    PRIMARY KEY (cod_ingreso, cod_vino)
);

-- RN-11: fecha_confeccion = fecha actual e inmodificable (trigger en 005).
CREATE TABLE transferencia (
    nro_transferencia  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sala            INTEGER NOT NULL
        REFERENCES sala_venta (id_sala) ON DELETE RESTRICT,
    fecha_confeccion   DATE NOT NULL,
    estado             estado_documento NOT NULL
);

CREATE TABLE renglon_transferencia (
    nro_transferencia  INTEGER NOT NULL
        REFERENCES transferencia (nro_transferencia) ON DELETE CASCADE,
    cod_vino           INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad           INTEGER NOT NULL,
    PRIMARY KEY (nro_transferencia, cod_vino)
);

CREATE TABLE stock_sala (
    id_sala   INTEGER NOT NULL
        REFERENCES sala_venta (id_sala) ON DELETE RESTRICT,
    cod_vino  INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad  INTEGER NOT NULL,
    PRIMARY KEY (id_sala, cod_vino)
);

-- Depósito central único: una fila por vino.
CREATE TABLE stock_deposito (
    cod_vino  INTEGER PRIMARY KEY
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad  INTEGER NOT NULL
);

-- RN-13: auditoría de cambios de precio (la completa un trigger AFTER UPDATE).
CREATE TABLE auditoria_precio (
    id_auditoria     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cod_vino         INTEGER NOT NULL
        REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    precio_anterior  NUMERIC(10,2) NOT NULL,
    precio_nuevo     NUMERIC(10,2) NOT NULL,
    fecha_hora       TIMESTAMPTZ   NOT NULL,
    usuario          VARCHAR(63)   NOT NULL
);

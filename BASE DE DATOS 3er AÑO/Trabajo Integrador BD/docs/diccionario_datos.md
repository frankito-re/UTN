# Diccionario de datos · Bodegas del Atuel

Generado a partir del esquema real de PostgreSQL (`001_esquema.sql` y `002_constraints.sql`). Son **29 tablas**, un tipo `ENUM` y un dominio.

## Tipos y dominios

| Nombre | Tipo | Definición | Uso |
| :-- | :-- | :-- | :-- |
| `estado_documento` | ENUM | `en_confeccion`, `terminado`, `procesado` | Estado de `ingreso` y `transferencia` (RN-10, RN-11). |
| `cuit_dom` | DOMAIN sobre `CHAR(11)` | `CHECK (VALUE ~ '^[0-9]{11}$')` | CUIT de empleados, bodegas y transportistas, y las columnas que los referencian. |

**Convenciones:** PK = clave primaria · FK = clave foránea (destino y acciones `ON DELETE`/`ON UPDATE`) · UQ = parte de una restricción `UNIQUE` · `identity` = clave generada por la base. Los nombres van en español, sin tildes ni ñ (`anada`, `campania`).

## Módulo A · Estructura geográfica y personal

### `localidad`

Localidad donde hay salas, clientes y cobertura de transportistas. Tiene un único encargado regional (RN-02).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_postal` | VARCHAR(8) | NO |  | PK | Código postal (clave natural). |
| `nombre` | VARCHAR(80) | NO |  | UQ | Nombre de la localidad. |
| `provincia` | VARCHAR(60) | NO |  | UQ | Provincia. |
| `encargado_regional` | VARCHAR(100) | NO |  |  | Encargado regional de todas las salas de la localidad. |

Restricciones adicionales:

- `uq_localidad_nombre_prov` — `UNIQUE (nombre, provincia)`

### `sala_venta`

Sala de venta de la red. Pertenece a una sola localidad (RN-02).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_sala` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `calle` | VARCHAR(80) | NO |  | UQ | Calle del domicilio. |
| `numero` | INTEGER | NO |  | UQ | Altura de la calle. |
| `dia_cierre` | VARCHAR(10) | NO |  |  | Día de cierre semanal. |
| `cod_postal` | VARCHAR(8) | NO |  | FK → localidad(cod_postal) · DEL RESTRICT, UQ | Localidad de la sala. |

Restricciones adicionales:

- `uq_sala_direccion` — `UNIQUE (calle, numero, cod_postal)`
- `ck_sala_dia_cierre` — `CHECK (((dia_cierre)::text = ANY ((ARRAY['lunes'::character varying, 'martes'::character varying, 'miercoles'::character varying, 'jueves'::character varying, 'viernes'::character varying, 'sabado'::character varying, 'domingo'::character varying])::text[])))`
- `ck_sala_numero_pos` — `CHECK ((numero > 0))`

### `empleado`

Empleado de una sala (RN-03).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cuit` | cuit_dom | NO |  | PK | CUIT del empleado (clave natural). |
| `nombre` | VARCHAR(100) | NO |  |  | Nombre completo. |
| `fecha_ingreso` | DATE | NO |  |  | Fecha de ingreso laboral. |
| `salario` | NUMERIC(12,2) | NO |  |  | Salario mensual. |
| `id_sala` | INTEGER | NO |  | FK → sala_venta(id_sala) · DEL RESTRICT | Sala donde trabaja. |

Restricciones adicionales:

- `ck_empleado_salario_pos` — `CHECK ((salario > (0)::numeric))`

## Módulo B · Producción agrícola y enológica

### `finca`

Finca productora de uva.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_finca` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `nombre` | VARCHAR(80) | NO |  |  | Nombre de la finca. |
| `superficie_ha` | NUMERIC(10,2) | NO |  |  | Superficie total en hectáreas. |
| `departamento` | VARCHAR(60) | NO |  |  | Departamento. |
| `provincia` | VARCHAR(60) | NO |  |  | Provincia. |

Restricciones adicionales:

- `ck_finca_superficie_pos` — `CHECK ((superficie_ha > (0)::numeric))`

### `parcela`

Parcela de una finca (entidad débil). Tiene una sola cepa (RN-04).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_finca` | INTEGER | NO |  | FK → finca(id_finca) · DEL CASCADE, PK | Finca a la que pertenece (parte de la clave). |
| `nro_parcela` | INTEGER | NO |  | PK | Número dentro de la finca (parte de la clave). |
| `superficie_ha` | NUMERIC(10,2) | NO |  |  | Superficie en hectáreas. |
| `anio_plantacion` | SMALLINT | NO |  |  | Año de plantación. |
| `id_cepa` | INTEGER | NO |  | FK → cepa(id_cepa) · DEL RESTRICT | Cepa plantada. |

Restricciones adicionales:

- `ck_parcela_anio_plantacion` — `CHECK (((anio_plantacion >= 1900) AND (anio_plantacion <= 2100)))`
- `ck_parcela_nro_pos` — `CHECK ((nro_parcela > 0))`
- `ck_parcela_superficie_pos` — `CHECK ((superficie_ha > (0)::numeric))`

### `cepa`

Variedad de uva.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_cepa` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `nombre` | VARCHAR(60) | NO |  | UQ | Nombre de la cepa. |
| `tipo` | VARCHAR(10) | NO |  |  | tinta o blanca. |

Restricciones adicionales:

- `uq_cepa_nombre` — `UNIQUE (nombre)`
- `ck_cepa_tipo` — `CHECK (((tipo)::text = ANY ((ARRAY['tinta'::character varying, 'blanca'::character varying])::text[])))`

### `lote_uva`

Cosecha de una parcela en una campaña, enviada a una bodega. Máximo una por parcela y campaña (RN-04).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `nro_lote` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `id_finca` | INTEGER | NO |  | FK → parcela(id_finca, nro_parcela) · DEL RESTRICT, UQ | Finca de la parcela cosechada. |
| `nro_parcela` | INTEGER | NO |  | FK → parcela(id_finca, nro_parcela) · DEL RESTRICT, UQ | Parcela cosechada. |
| `campania` | SMALLINT | NO |  | UQ | Año de campaña. |
| `fecha_cosecha` | DATE | NO |  |  | Fecha de cosecha. |
| `kg` | NUMERIC(12,2) | NO |  |  | Kilos cosechados. |
| `cuit_bodega` | cuit_dom | NO |  | FK → bodega(cuit) · DEL RESTRICT | Bodega destino. |

Restricciones adicionales:

- `uq_lote_parcela_campania` — `UNIQUE (id_finca, nro_parcela, campania)`
- `ck_lote_campania` — `CHECK (((campania >= 1990) AND (campania <= 2100)))`
- `ck_lote_kg_pos` — `CHECK ((kg > (0)::numeric))`

### `analisis_calidad`

Análisis de calidad realizado sobre un lote de uva.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_analisis` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `nro_lote` | INTEGER | NO |  | FK → lote_uva(nro_lote) · DEL CASCADE | Lote analizado. |
| `fecha` | DATE | NO |  |  | Fecha del análisis. |
| `brix` | NUMERIC(4,1) | NO |  |  | Grado Brix (azúcares). |
| `ph` | NUMERIC(3,2) | NO |  |  | pH del mosto. |
| `acidez_total` | NUMERIC(4,2) | NO |  |  | Acidez total en g/L. |

Restricciones adicionales:

- `ck_analisis_acidez` — `CHECK ((acidez_total > (0)::numeric))`
- `ck_analisis_brix` — `CHECK (((brix >= (0)::numeric) AND (brix <= (40)::numeric)))`
- `ck_analisis_ph` — `CHECK (((ph > (0)::numeric) AND (ph < (14)::numeric)))`

### `bodega`

Bodega que elabora vinos y recibe uva.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cuit` | cuit_dom | NO |  | PK | CUIT (clave natural). |
| `razon_social` | VARCHAR(120) | NO |  |  | Razón social. |
| `domicilio` | VARCHAR(160) | NO |  |  | Domicilio. |

### `vino`

Vino del catálogo. Precio único para toda la red (RN-01).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_vino` | INTEGER | NO | `identity` | PK | Código generado. |
| `nombre` | VARCHAR(80) | NO |  | UQ | Nombre comercial. |
| `tipo` | VARCHAR(12) | NO |  |  | tinto, blanco, rosado o espumante. |
| `anada` | SMALLINT | NO |  | UQ | Año de la cosecha del vino. |
| `volumen_ml` | INTEGER | NO |  | UQ | Presentación en ml (375, 750, 1500). |
| `graduacion` | NUMERIC(4,2) | NO |  |  | Graduación alcohólica (5 a 20). |
| `precio` | NUMERIC(10,2) | NO |  |  | Precio de venta vigente (> 0). |
| `cuit_bodega` | cuit_dom | NO |  | FK → bodega(cuit) · DEL RESTRICT | Bodega que lo elabora. |

Restricciones adicionales:

- `uq_vino_nombre_anada_volumen` — `UNIQUE (nombre, anada, volumen_ml)`
- `ck_vino_anada` — `CHECK (((anada >= 1990) AND (anada <= 2100)))`
- `ck_vino_graduacion` — `CHECK (((graduacion >= (5)::numeric) AND (graduacion <= (20)::numeric)))`
- `ck_vino_precio_pos` — `CHECK ((precio > (0)::numeric))`
- `ck_vino_tipo` — `CHECK (((tipo)::text = ANY ((ARRAY['tinto'::character varying, 'blanco'::character varying, 'rosado'::character varying, 'espumante'::character varying])::text[])))`
- `ck_vino_volumen` — `CHECK ((volumen_ml = ANY (ARRAY[375, 750, 1500])))`

### `composicion`

Corte del vino: porcentaje de cada cepa. Los porcentajes de un vino suman 100 (RN-05).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL CASCADE, PK | Vino. |
| `id_cepa` | INTEGER | NO |  | FK → cepa(id_cepa) · DEL RESTRICT, PK | Cepa. |
| `porcentaje` | NUMERIC(5,2) | NO |  |  | Porcentaje de la cepa en el corte. |

Restricciones adicionales:

- `ck_composicion_pct` — `CHECK (((porcentaje > (0)::numeric) AND (porcentaje <= (100)::numeric)))`

### `maridaje`

Maridaje sugerido (comida) con su temperatura de servicio.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_maridaje` | INTEGER | NO | `identity` | PK | Identificador generado. |
| `nombre` | VARCHAR(80) | NO |  | UQ | Nombre (ej. carnes rojas). |
| `temperatura_servicio` | NUMERIC(4,1) | NO |  |  | Temperatura de servicio sugerida en °C. |

Restricciones adicionales:

- `uq_maridaje_nombre` — `UNIQUE (nombre)`
- `ck_maridaje_temp` — `CHECK (((temperatura_servicio >= (0)::numeric) AND (temperatura_servicio <= (30)::numeric)))`

### `vino_maridaje`

Relación N:M entre vinos y maridajes.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL CASCADE, PK | Vino. |
| `id_maridaje` | INTEGER | NO |  | FK → maridaje(id_maridaje) · DEL CASCADE, PK | Maridaje recomendado. |

## Módulo C · Clientes, ventas y comercialización

### `cliente`

Supertipo de la jerarquía de clientes (disjunta y total). Guarda el descuento vigente (RN-06).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_cliente` | INTEGER | NO | `identity` | UQ, PK | Identificador generado. |
| `nombre_razon_social` | VARCHAR(120) | NO |  |  | Apellido y nombre o razón social. |
| `tipo_doc` | VARCHAR(10) | NO |  | UQ | DNI, CUIT, CUIL o PASAPORTE. |
| `nro_doc` | VARCHAR(20) | NO |  | UQ | Número de documento. |
| `direccion` | VARCHAR(160) | NO |  |  | Dirección. |
| `cod_postal` | VARCHAR(8) | NO |  | FK → localidad(cod_postal) · DEL RESTRICT | Localidad del cliente. |
| `fecha_alta` | DATE | NO | `CURRENT_DATE` |  | Fecha de alta. |
| `tipo_cliente` | VARCHAR(12) | NO |  | UQ | Discriminador: socio, distribuidor o exportador. |
| `descuento` | NUMERIC(5,2) | NO |  |  | Porcentaje de descuento vigente (base: 10, 20 o 30). |

Restricciones adicionales:

- `cliente_id_cliente_tipo_cliente_key` — `UNIQUE (id_cliente, tipo_cliente)`
- `uq_cliente_documento` — `UNIQUE (tipo_doc, nro_doc)`
- `ck_cliente_descuento` — `CHECK (((descuento >= (0)::numeric) AND (descuento <= (100)::numeric)))`
- `ck_cliente_tipo` — `CHECK (((tipo_cliente)::text = ANY ((ARRAY['socio'::character varying, 'distribuidor'::character varying, 'exportador'::character varying])::text[])))`
- `ck_cliente_tipo_doc` — `CHECK (((tipo_doc)::text = ANY ((ARRAY['DNI'::character varying, 'CUIT'::character varying, 'CUIL'::character varying, 'PASAPORTE'::character varying])::text[])))`

### `socio`

Subtipo de cliente: socio del club (10 %). Sin atributos propios.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_cliente` | INTEGER | NO |  | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE, PK | Cliente (PK y FK). |
| `tipo_cliente` | VARCHAR(12) | NO | `'socio'` | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE | Fijo 'socio' (garantiza la disjunción). |

Restricciones adicionales:

- `ck_socio_tipo` — `CHECK (((tipo_cliente)::text = 'socio'::text))`

### `distribuidor`

Subtipo de cliente: distribuidor (20 %).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_cliente` | INTEGER | NO |  | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE, PK | Cliente (PK y FK). |
| `tipo_cliente` | VARCHAR(12) | NO | `'distribuidor'` | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE | Fijo 'distribuidor' (garantiza la disjunción). |
| `zona_cobertura` | VARCHAR(100) | NO |  |  | Zona que cubre. |
| `nro_habilitacion` | VARCHAR(30) | NO |  | UQ | Número de habilitación (único). |

Restricciones adicionales:

- `uq_distribuidor_habilitacion` — `UNIQUE (nro_habilitacion)`
- `ck_distribuidor_tipo` — `CHECK (((tipo_cliente)::text = 'distribuidor'::text))`

### `exportador`

Subtipo de cliente: exportador (30 %).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_cliente` | INTEGER | NO |  | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE, PK | Cliente (PK y FK). |
| `tipo_cliente` | VARCHAR(12) | NO | `'exportador'` | FK → cliente(id_cliente, tipo_cliente) · DEL CASCADE | Fijo 'exportador' (garantiza la disjunción). |
| `pais_destino` | VARCHAR(60) | NO |  |  | País de destino principal. |

Restricciones adicionales:

- `ck_exportador_tipo` — `CHECK (((tipo_cliente)::text = 'exportador'::text))`

### `permiso_exportacion`

Permiso de exportación de un exportador. El vencimiento es posterior a la emisión (RN-07).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_permiso` | VARCHAR(30) | NO |  | PK | Código del permiso. |
| `id_cliente` | INTEGER | NO |  | FK → exportador(id_cliente) · DEL CASCADE | Exportador titular. |
| `fecha_emision` | DATE | NO |  |  | Fecha de emisión. |
| `fecha_vencimiento` | DATE | NO |  |  | Fecha de vencimiento. |

Restricciones adicionales:

- `ck_permiso_fechas` — `CHECK ((fecha_vencimiento > fecha_emision))`

### `comprobante`

Cabecera de una venta. Los importes los calcula la base (RN-08).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `nro_comprobante` | INTEGER | NO | `identity` | PK | Número generado. |
| `fecha` | DATE | NO | `CURRENT_DATE` |  | Fecha de la venta. |
| `id_cliente` | INTEGER | NO |  | FK → cliente(id_cliente) · DEL RESTRICT | Cliente comprador. |
| `id_sala` | INTEGER | NO |  | FK → sala_venta(id_sala) · DEL RESTRICT | Sala donde se vendió. |
| `subtotal` | NUMERIC(14,2) | NO | `0` |  | Suma bruta de los renglones (cantidad × precio). |
| `descuento` | NUMERIC(14,2) | NO | `0` |  | Monto de descuento en $. |
| `total` | NUMERIC(14,2) | NO | `0` |  | Subtotal menos descuento. |

Restricciones adicionales:

- `ck_comprobante_montos` — `CHECK (((subtotal >= (0)::numeric) AND (descuento >= (0)::numeric) AND (descuento <= subtotal)))`
- `ck_comprobante_total` — `CHECK ((total = (subtotal - descuento)))`

### `renglon_comprobante`

Renglón de una venta: un vino por comprobante.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `nro_comprobante` | INTEGER | NO |  | FK → comprobante(nro_comprobante) · DEL CASCADE, PK | Comprobante. |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT, PK | Vino vendido. |
| `cantidad` | INTEGER | NO |  |  | Unidades vendidas (> 0). |
| `precio_unitario` | NUMERIC(10,2) | NO |  |  | Precio del vino al momento de la venta. |
| `descuento_pct` | NUMERIC(5,2) | NO | `0` |  | % de descuento aplicado al renglón. |
| `subtotal` | NUMERIC(14,2) | NO |  |  | cantidad × precio × (1 − descuento/100). |

Restricciones adicionales:

- `ck_renglon_cantidad_pos` — `CHECK ((cantidad > 0))`
- `ck_renglon_descuento` — `CHECK (((descuento_pct >= (0)::numeric) AND (descuento_pct <= (100)::numeric)))`
- `ck_renglon_precio_pos` — `CHECK ((precio_unitario > (0)::numeric))`
- `ck_renglon_subtotal` — `CHECK ((subtotal >= (0)::numeric))`

## Módulo D · Inventario, logística y auditoría

### `transportista`

Empresa de transporte que trae vino de las bodegas al depósito.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_transportista` | INTEGER | NO | `identity` | PK | Código generado. |
| `razon_social` | VARCHAR(120) | NO |  |  | Razón social. |
| `cuit` | cuit_dom | NO |  | UQ | CUIT (único). |
| `email` | VARCHAR(120) | NO |  |  | Correo electrónico. |
| `telefono` | VARCHAR(30) | NO |  |  | Teléfono. |
| `domicilio` | VARCHAR(160) | NO |  |  | Domicilio. |

Restricciones adicionales:

- `uq_transportista_cuit` — `UNIQUE (cuit)`
- `ck_transportista_email` — `CHECK (((email)::text ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'::text))`

### `cobertura_transportista`

Localidades que cubre cada transportista (N:M).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_transportista` | INTEGER | NO |  | FK → transportista(cod_transportista) · DEL CASCADE, PK | Transportista. |
| `cod_postal` | VARCHAR(8) | NO |  | FK → localidad(cod_postal) · DEL RESTRICT, PK | Localidad cubierta. |

### `ingreso`

Ingreso de vino al depósito central. Estados: en_confeccion → terminado → procesado (RN-10).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_ingreso` | INTEGER | NO | `identity` | PK | Código generado. |
| `fecha` | DATE | NO | `CURRENT_DATE` |  | Fecha del ingreso. |
| `estado` | estado_documento | NO | `'en_confeccion'` |  | Estado del documento. |
| `cod_transportista` | INTEGER | NO |  | FK → transportista(cod_transportista) · DEL RESTRICT | Transportista que lo trae. |
| `cuit_bodega` | cuit_dom | NO |  | FK → bodega(cuit) · DEL RESTRICT | Bodega de origen. |

### `renglon_ingreso`

Renglón de un ingreso; solo se edita en confección (RN-12).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_ingreso` | INTEGER | NO |  | FK → ingreso(cod_ingreso) · DEL CASCADE, PK | Ingreso. |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT, PK | Vino. |
| `cantidad` | INTEGER | NO |  |  | Unidades que ingresan (> 0). |

Restricciones adicionales:

- `ck_renglon_ingreso_cantidad` — `CHECK ((cantidad > 0))`

### `transferencia`

Solicitud de vino del depósito central a una sala (RN-11).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `nro_transferencia` | INTEGER | NO | `identity` | PK | Número generado. |
| `id_sala` | INTEGER | NO |  | FK → sala_venta(id_sala) · DEL RESTRICT | Sala solicitante. |
| `fecha_confeccion` | DATE | NO | `CURRENT_DATE` |  | Fecha actual al crearla; no se puede modificar. |
| `estado` | estado_documento | NO | `'en_confeccion'` |  | Estado del documento. |

### `renglon_transferencia`

Renglón de una transferencia; solo se edita en confección (RN-12).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `nro_transferencia` | INTEGER | NO |  | FK → transferencia(nro_transferencia) · DEL CASCADE, PK | Transferencia. |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT, PK | Vino. |
| `cantidad` | INTEGER | NO |  |  | Unidades solicitadas (> 0). |

Restricciones adicionales:

- `ck_renglon_transf_cantidad` — `CHECK ((cantidad > 0))`

### `stock_sala`

Stock de cada vino en cada sala; nunca negativo (RN-09).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_sala` | INTEGER | NO |  | FK → sala_venta(id_sala) · DEL RESTRICT, PK | Sala. |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT, PK | Vino. |
| `cantidad` | INTEGER | NO | `0` |  | Unidades disponibles. |

Restricciones adicionales:

- `ck_stock_sala_no_neg` — `CHECK ((cantidad >= 0))`

### `stock_deposito`

Stock del depósito central (único), una fila por vino.

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT, PK | Vino. |
| `cantidad` | INTEGER | NO | `0` |  | Unidades disponibles. |

Restricciones adicionales:

- `ck_stock_deposito_no_neg` — `CHECK ((cantidad >= 0))`

### `auditoria_precio`

Historial de cambios de precio de los vinos (RN-13).

| Columna | Tipo | Nulo | Default | Clave | Descripción |
| :-- | :-- | :-: | :-- | :-- | :-- |
| `id_auditoria` | BIGINT | NO | `identity` | PK | Identificador generado. |
| `cod_vino` | INTEGER | NO |  | FK → vino(cod_vino) · DEL RESTRICT | Vino modificado. |
| `precio_anterior` | NUMERIC(10,2) | NO |  |  | Precio antes del cambio. |
| `precio_nuevo` | NUMERIC(10,2) | NO |  |  | Precio después del cambio. |
| `fecha_hora` | TIMESTAMPTZ | NO | `now()` |  | Momento del cambio. |
| `usuario` | VARCHAR(63) | NO | `CURRENT_USER` |  | Usuario de la base que lo hizo. |

Restricciones adicionales:

- `ck_auditoria_precios` — `CHECK (((precio_anterior > (0)::numeric) AND (precio_nuevo > (0)::numeric) AND (precio_anterior <> precio_nuevo)))`


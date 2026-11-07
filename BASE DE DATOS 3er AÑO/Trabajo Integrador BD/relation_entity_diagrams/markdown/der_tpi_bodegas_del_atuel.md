# Diagrama Entidad-Relación (DER) - TPI Bodegas del Atuel

## 📌 1. Reglas básicas del DER según el TPI

Para que el diagrama esté completo y cumpla con la evaluación, se exige incluir explícitamente:
* **Entidades fuertes y débiles:** Representar los rectángulos de entidades, destacando la entidad débil *Parcela* (que depende de *Finca*).
* **Atributos y Claves:** Marcar las claves primarias (PK) e identificadores.
* **Cardinalidades mínimas y máximas:** Indicar la participación de cada lado de la relación (ej. `(1,1)`, `(0,N)`, `(1,N)`).
* **Jerarquía de herencia:** Representar la especialización de la entidad *Cliente* (Supertipo) en sus 3 subtipos (*Socio*, *Distribuidor*, *Exportador*).
* **Relaciones N:M con atributos propios:** Representar las relaciones muchos a muchos que almacenan datos (como *Composición* o *Renglón de comprobante*).

---

## 🧱 2. Construcción paso a paso del DER por Módulos

### 🗺️ Módulo A: Estructura Geográfica y Personal

1. **Localidad**
   * **Atributos:** `código_postal` (PK), `nombre`, `provincia`, `encargado_regional`.
   * *Regla:* El encargado regional depende de la localidad.
2. **Sala de venta**
   * **Atributos:** `id_sala` (PK), `calle`, `número`, `día_cierre`.
   * **Relación:** `Pertenece` a **Localidad**.
     * Cardinalidad: **Sala de venta** `(1,1)` ─── `Pertenece` ─── `(0,N)` **Localidad**.
3. **Empleado**
   * **Atributos:** `CUIT` (PK), `nombre`, `fecha_ingreso`, `salario`.
   * **Relación:** `Trabaja en` **Sala de venta**.
     * Cardinalidad: **Empleado** `(1,1)` ─── `Trabaja en` ─── `(0,N)` **Sala de venta** (cada empleado trabaja en una sola sala).

---

### 🍇 Módulo B: Producción Agrícola y Enológica

1. **Finca**
   * **Atributos:** `id_finca` (PK), `nombre`, `superficie_ha`, `departamento`, `provincia`.
2. **Parcela** *(Entidad Débil de Finca)*
   * **Atributos:** `nro_parcela` (Clave parcial), `superficie`, `año_plantación`.
   * **Clave identificadora:** `(id_finca, nro_parcela)`.
   * **Relación:** **Finca** `(1,N)` ═══ `Posee` ═══ `(1,1)` **Parcela**.
3. **Cepa**
   * **Atributos:** `id_cepa` (PK), `nombre`, `tipo` (*tinta* o *blanca*).
   * **Relación con Parcela:** **Parcela** `(1,1)` ─── `Tiene` ─── `(0,N)` **Cepa** (una parcela contiene una sola cepa).
4. **Lote de uva**
   * **Atributos:** `nro_lote` (PK), `campaña`, `fecha`, `kg`.
   * **Relaciones:**
     * `Cosechado en` **Parcela**: **Lote** `(1,1)` ─── `Cosechado en` ─── `(0,N)` **Parcela** (máximo una cosecha por parcela y campaña).
     * `Destinado a` **Bodega**: **Lote** `(1,1)` ─── `Enviado a` ─── `(0,N)` **Bodega**.
5. **Análisis de calidad**
   * **Atributos:** `id_análisis` (PK), `fecha`, `brix`, `pH`, `acidez`.
   * **Relación:** **Análisis** `(1,1)` ─── `Analiza` ─── `(0,N)` **Lote de uva**.
6. **Bodega**
   * **Atributos:** `CUIT` (PK), `razón_social`, `domicilio`.
7. **Vino**
   * **Atributos:** `código_vino` (PK), `nombre`, `tipo`, `añada`, `volumen_ml`, `graduación`, `precio`.
   * **Relación:** **Vino** `(1,1)` ─── `Elaborado por` ─── `(0,N)` **Bodega**.
8. **Composición (Vino - Cepa)** *(Relación N:M con atributo)*
   * **Atributo propio:** `porcentaje` (la suma por vino debe dar exactamente 100%).
   * **Cardinalidad:** **Vino** `(1,N)` ─── `<Composición>` ─── `(1,N)` **Cepa**.
9. **Maridaje y Vino-Maridaje** *(Relación N:M)*
   * **Maridaje:** `id_maridaje` (PK), `nombre`, `temperatura_servicio`.
   * **Cardinalidad:** **Vino** `(0,N)` ─── `<Recomienda>` ─── `(0,N)` **Maridaje**.

---

### 👥 Módulo C: Clientes, Ventas y Comercialización

1. **Jerarquía de Cliente (Supertipo / Subtipos)**
   * **Cliente (Supertipo):** `id_cliente` (PK), `nombre_o_razón_social`, `tipo_doc`, `nro_doc`, `dirección`, `localidad`, `fecha_alta`, `descuento`.
   * **Subtipos (Especialización disjunta y total):**
     * **Socio:** `zona`, `habilitación`.
     * **Distribuidor:** datos comerciales propios.
     * **Exportador:** `país_destino`.
2. **Permiso de exportación**
   * **Atributos:** `código_permiso` (PK), `fecha_emisión`, `fecha_vencimiento`.
   * **Relación:** **Permiso** `(1,1)` ─── `Otorgado a` ─── `(0,N)` **Exportador**.
3. **Comprobante (Venta)**
   * **Atributos:** `nro_comprobante` (PK), `fecha`, `subtotal`, `descuento`, `total`.
   * **Relaciones:**
     * `Emitido a` **Cliente**: **Comprobante** `(1,1)` ─── `Emitido a` ─── `(0,N)` **Cliente**.
     * `Realizado en` **Sala de venta**: **Comprobante** `(1,1)` ─── `Realizado en` ─── `(0,N)` **Sala de venta**.
4. **Renglón de comprobante** *(Relación / Entidad débil asociativa)*
   * **Atributos propios:** `cantidad`, `precio_unitario`, `descuento`, `subtotal`.
   * **Clave identificadora:** `(nro_comprobante, código_vino)`.
   * **Cardinalidad:** **Comprobante** `(1,N)` ─── `<Renglón>` ─── `(1,N)` **Vino**.

---

### 🚚 Módulo D: Inventario, Logística y Auditoría

1. **Transportista**
   * **Atributos:** `código_transportista` (PK), `razón_social`, `CUIT`, `email`, `teléfono`, `domicilio`.
   * **Relación N:M:** **Transportista** `(0,N)` ─── `<Cubre>` ─── `(0,N)` **Localidad**.
2. **Ingreso de Depósito** *(Cabecera y Renglón)*
   * **Cabecera Ingreso:** `código_ingreso` (PK), `fecha`, `estado` (*ENUM: en_confeccion, terminado, procesado*).
   * **Relaciones:** Conectado con **Transportista** `(1,1)` y **Bodega** `(1,1)`.
   * **Renglón de Ingreso (N:M):** conecta **Ingreso** con **Vino** storing `cantidad`.
3. **Transferencia a Sala** *(Cabecera y Renglón)*
   * **Cabecera Transferencia:** `nro_transferencia` (PK), `fecha_confección`, `estado` (*ENUM*).
   * **Relación:** Conectado con **Sala de venta** `(1,1)`.
   * **Renglón de Transferencia (N:M):** conecta **Transferencia** con **Vino** storing `cantidad`.
4. **Stock de Sala y Stock de Depósito**
   * **Stock de Sala (N:M):** `(id_sala, código_vino)` (PK compuesta), `cantidad`.
   * **Stock de Depósito:** `código_vino` (PK), `cantidad` (Depósito central único).
5. **Auditoría de precio**
   * **Atributos:** `id_auditoría` (PK), `precio_anterior`, `precio_nuevo`, `fecha_hora`, `usuario`.
   * **Relación:** **Auditoría** `(1,1)` ─── `Audita` ─── `(0,N)` **Vino**.

---

## 📊 Resumen de cardinalidades y claves del modelo

| Entidad / Relación | Clave Primaria (PK) | Dependencia / Tipo | Cardinalidades Principales |
| :--- | :--- | :--- | :--- |
| **Finca** | `id_finca` | Fuerte | `(1,N)` con Parcela |
| **Parcela** | `(id_finca, nro_parcela)` | Débil de Finca | `(1,1)` con Finca; `(1,1)` con Cepa |
| **Vino** | `código_vino` | Fuerte | `(1,1)` con Bodega |
| **Composición** | `(código_vino, id_cepa)` | N:M con atributo | `(1,N)` Vino a `(1,N)` Cepa |
| **Cliente** | `id_cliente` | Supertipo | Jerarquía Disjunta Total |
| **Renglón Comprobante**| `(nro_comprobante, código_vino)`| Débil / N:M | `(1,N)` Comprobante a `(1,N)` Vino |
| **Stock de Sala** | `(id_sala, código_vino)` | N:M | `(0,N)` Sala a `(0,N)` Vino |

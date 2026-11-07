# Trabajo Práctico Integrador: Sistema de Gestión y Distribución «Bodegas del Atuel»

**Bases de Datos · Ingeniería en Sistemas · 3.° Año**  
**UTN Facultad Regional San Rafael — Ciclo Lectivo 2026**

---

## Datos Generales del Proyecto

| Dato | Detalle |
| :--- | :--- |
| **Cátedra / Facultad** | UTN Facultad Regional San Rafael |
| **Ciclo lectivo** | 2026 |
| **Modalidad** | Grupal (3 a 4 integrantes), con roles rotativos |
| **Motor de Base de Datos** | PostgreSQL (versión 14 o superior) |
| **Acceso a datos desde API** | SQL directo con driver nativo. **No se permite ORM.** |
| **Fecha de lanzamiento** | 13/10/2026 |
| **Entrega final y defensa oral** | A definir |

---

## Índices y Contenido
1. Presentación y objetivos
2. Modalidad de trabajo y cronograma
3. Escenario propuesto
4. Reglas de negocio
5. Modelo de datos: entidades mínimas
6. Tecnologías y restricciones
7. Etapas del proyecto (1 a 9)
8. Consultas SQL requeridas
9. Rúbrica de evaluación
10. Estructura del repositorio y entrega final
- **Anexos:** Ejemplos en PostgreSQL, catálogos sugeridos, preguntas típicas de defensa

---

## 1. Presentación y Objetivos

Este trabajo práctico integra todo lo visto en la materia en un único proyecto: se parte de un escenario real, se modela la base de datos, se implementa con PostgreSQL, se carga con un volumen de datos importante, se protege con reglas de integridad escritas en la propia base, se optimiza con índices y finalmente se conecta con una API y un front que se publican en un servidor en la nube.

La idea central es que la base de datos deje de ser un ejercicio aislado y pase a ser el corazón de un sistema que otros programas consumen. Por eso **la parte que más pesa en la evaluación es la capa de datos:** modelo, constraints, índices, funciones, procedimientos, triggers y consultas.

### 1.1 Objetivos de Aprendizaje
- Modelar un escenario real con un diagrama entidad-relación (incluyendo jerarquías, entidades débiles y relaciones N:M con atributos) y transformarlo a un esquema relacional normalizado hasta 3FN.
- Implementar el esquema físico en PostgreSQL aplicando **constraints** (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`), tipos enumerados y dominios.
- Escribir **funciones, procedimientos almacenados y triggers** en PL/pgSQL para garantizar reglas de negocio dentro de la base de datos.
- Cargar masivamente datos coherentes (más de 100.000 registros en al menos una tabla) con scripts reproducibles.
- Diseñar **índices** con evidencia: interpretar planes de ejecución con `EXPLAIN (ANALYZE, BUFFERS)` y medir mejoras.
- Resolver consultas SQL básicas y avanzadas (subconsultas, CTE, funciones de ventana, división relacional, agregaciones por período) y operaciones de inserción, modificación y borrado.
- Manejar **transacciones y concurrencia** y entender qué garantiza la base de datos frente a dos usuarios simultáneos.
- Conectar la base de datos con una **API REST** y un **front** sin ocultar el SQL, y traducir los errores de la base a respuestas HTTP claras.
- Desplegar el sistema en la **nube** con criterios básicos de seguridad: roles con privilegios mínimos, secretos fuera del repositorio, conexión cifrada, backup y restauración probados.

### 1.2 Qué se evalúa y qué no
- **Se evalúa:** la calidad del diseño, la corrección de las reglas implementadas en la base, la evidencia de rendimiento, el dominio de SQL y la capacidad de explicar y defender cada decisión.
- **La API y el front son el medio** para demostrar que la base funciona como parte de un sistema. No se pide un diseño visual sofisticado ni autenticación compleja.
- **No se permite ORM ni generadores que oculten el SQL.** El esquema, las migraciones y todas las consultas las escriben los alumnos a mano.

---

## 2. Modalidad de Trabajo y Cronograma

### 2.1 Organización del Grupo
- Grupos de **3 a 4 integrantes.** Se sugieren cuatro roles que **rotan por etapa:** Datos (modelo y SQL), API, Front/Integración e Infraestructura (Docker, nube, backups).
- Aunque haya roles, **todos los integrantes deben poder explicar el modelo y las reglas de la base de datos** en la defensa.
- Repositorio **Git** obligatorio (GitHub o GitLab) con commits de todos los integrantes.
- Integridad académica: Todo el trabajo debe ser del grupo. La nota final es individual según la defensa oral.

### 2.2 Cronograma Sugerido

| Hito | Etapa | Entregable |
| :--- | :--- | :--- |
| **H1** | 1. Modelado | DER, esquema relacional, diccionario de datos y DDL base |
| **H2** | 2. Integridad y lógica en la base | Constraints, funciones, procedimientos, triggers, vistas, roles y pruebas SQL |
| **H3** | 3. Carga masiva | Scripts de carga reproducibles y reporte de conteos y tiempos |
| **H4** | 4. Índices y rendimiento | Informe con planes de ejecución antes y después |
| **H5** | 5. Consultas SQL | Archivos de consultas INSERT, UPDATE, DELETE y SELECT comentadas |
| **H6** | 6. API | API REST funcionando en local con Docker Compose |
| **H7** | 7. Front | Front conectado a la API |
| **H8** | 8. Nube | Sistema desplegado con URL pública, backup y restauración probados |
| **H9** | 9. Documentación y defensa | Informe final, README, demo en vivo y defensa oral |

---

## 3. Escenario Propuesto: «Bodegas del Atuel»

Se desea mantener una base de datos para la gestión de «Bodegas del Atuel», una empresa vitivinícola ficticia que integra la producción de uva y de vino con su distribución y venta a través de una red de salas de venta distribuidas en distintas localidades.

### 3.1 Localidades, Salas de Venta y Empleados
- **Localidades:** Nombre, provincia, código postal. Existe un único encargado regional por localidad (afectado a todas las salas de esa localidad).
- **Salas de Venta:** ID, dirección (calle y número), día de cierre semanal, localidad.
- **Empleados:** CUIT, nombre, fecha de ingreso laboral, salario, sala de venta en la que trabaja.

### 3.2 Producción de Uva
- **Fincas:** ID, nombre, superficie total en hectáreas, departamento y provincia.
- **Parcelas:** Número de parcela dentro de la finca (entidad débil de finca), superficie, año de plantación, cepa plantada (única).
- **Cepas:** Nombre, tipo (tinta o blanca).
- **Lotes de Uva:** Número, fecha de cosecha, kilos cosechados, bodega destino, campaña (año). Máximo una cosecha por parcela y campaña.
- **Análisis de Calidad:** Fecha, grado Brix, pH, acidez total (g/L).

### 3.3 Bodegas y Vinos
- **Bodegas:** CUIT, razón social, domicilio.
- **Vinos:** Código, nombre comercial, tipo (tinto, blanco, rosado, espumante), añada, presentación (ml: 375, 750, 1500), graduación alcohólica, precio de venta (único para todas las salas).
- **Composición (Corte):** Porcentajes de corte por cepa (la suma debe dar exactamente 100%).
- **Maridajes:** Nombre (ej. «carnes rojas»), temperatura de servicio sugerida (°C).

### 3.4 Clientes y Ventas
- **Clientes:** ID, apellido y nombre/razón social, tipo y número de documento, dirección, localidad, fecha de alta.
  - *Socios del club:* 10% de descuento.
  - *Distribuidores:* 20% de descuento, zona de cobertura, número de habilitación.
  - *Exportadores:* 30% de descuento, país de destino principal, permisos de exportación (código, emisión, vencimiento).
- **Comprobantes y Ventas:** Número, fecha, cliente, sala, subtotal, descuento, total. Incluye renglones (vino, cantidad, precio unitario, descuento aplicado, subtotal).

### 3.5 Stock, Depósito Central, Ingresos y Transferencias
- **Stock:** Cada sala posee su stock por vino. Existe un Depósito Central con su propio stock.
- **Ingresos:** Vinos que ingresan al depósito central desde una bodega vía transportista. Código, fecha, estado (`en_confeccion`, `terminado`, `procesado`). Sólo un ingreso `terminado` puede impactar el stock.
- **Transportistas:** Código, razón social, CUIT, e-mail, teléfono, domicilio, localidades que cubre.
- **Transferencias:** Solicitudes de vino de una sala al depósito central. Número, sala, fecha de confección, estado. Impacta descontando del depósito central y sumando al stock de la sala (requiere stock suficiente).

---

## 4. Reglas de Negocio (RN-01 a RN-15)

| N.° | Regla | Mecanismo Esperado |
| :--- | :--- | :--- |
| **RN-01** | El precio de un vino es único para toda la red de salas y siempre mayor que cero. | Atributo en vino + `CHECK` |
| **RN-02** | Una sala pertenece a una sola localidad. Cada localidad tiene un único encargado regional. | FK + diseño normalizado (3FN) |
| **RN-03** | Cada empleado trabaja en una sola sala. | FK `NOT NULL` |
| **RN-04** | Una parcela tiene una sola cepa y se cosecha como máximo una vez por campaña. | FK + `UNIQUE (parcela, campaña)` |
| **RN-05** | Los porcentajes de corte de un vino suman exactamente 100. | Constraint trigger diferido |
| **RN-06** | El descuento depende del tipo de cliente: socio 10 %, distribuidor 20 %, exportador 30 %. | Función de descuento + `CHECK` de rango |
| **RN-07** | Un exportador puede tener varios permisos; el vencimiento es posterior a la emisión. | Tabla de permisos + `CHECK` entre columnas |
| **RN-08** | El total del comprobante es la suma de sus renglones con el descuento aplicado. No se carga a mano. | Función de cálculo + trigger |
| **RN-09** | No se puede vender más de lo que hay en stock de la sala. El stock nunca es negativo. | Trigger `BEFORE INSERT` + `CHECK (cantidad >= 0)` |
| **RN-10** | Sólo un ingreso terminado impacta en el depósito y pasa a procesado. Transiciones: `en_confeccion` → `terminado` → `procesado`. | Tipo `ENUM` + trigger de estados + procedimiento |
| **RN-11** | Igual que RN-10 para transferencias. La fecha de confección es la actual y no se puede modificar. | Trigger de estados y de fecha + procedimiento |
| **RN-12** | Un ingreso o una transferencia que no está en confección no admite agregar, modificar ni quitar renglones. | Trigger sobre los renglones |
| **RN-13** | Todo cambio de precio de un vino queda auditado (fecha, usuario, precio anterior y nuevo). | Trigger `AFTER UPDATE` + tabla de auditoría |
| **RN-14** | No se puede borrar un transportista, una bodega ni un vino que tengan movimientos asociados. | FK con `ON DELETE RESTRICT` |
| **RN-15** | Cantidades, superficies, kilos y precios son siempre positivos. La graduación está entre 5 y 20. | `CHECK` |

---

## 5. Modelo de Datos: Entidades Mínimas

- **Localidad:** Código postal, nombre, provincia, encargado regional.
- **Sala de Venta:** ID, calle, número, día de cierre, localidad.
- **Empleado:** CUIT, nombre, fecha de ingreso, salario, sala.
- **Finca:** ID, nombre, superficie (ha), departamento, provincia.
- **Parcela:** N.° de parcela, finca, superficie, año de plantación, cepa. *(Clave: finca, n.° parcela)*.
- **Cepa:** ID, nombre, tipo (tinta/blanca).
- **Lote de Uva:** N.° de lote, parcela, campaña, fecha, kg, bodega destino.
- **Análisis de Calidad:** ID, lote, fecha, Brix, pH, acidez.
- **Bodega:** CUIT, razón social, domicilio.
- **Vino:** Código, nombre, tipo, añada, volumen (ml), graduación, precio, bodega.
- **Composición (Vino-Cepa):** Vino, cepa, porcentaje.
- **Maridaje / Vino-Maridaje:** ID, nombre, temperatura servicio.
- **Cliente / Subtipos:** ID, nombre/razón social, tipo/nro documento, dirección, localidad, fecha alta, descuento. *(Socios, Distribuidores, Exportadores)*.
- **Permiso de Exportación:** Código, exportador, emisión, vencimiento.
- **Comprobante / Renglón:** Número, fecha, cliente, sala, subtotal, descuento, total.
- **Transportista / Cobertura:** Código, razón social, CUIT, e-mail, teléfono, domicilio, localidad.
- **Ingreso / Transferencia (y renglones):** Código/Número, estado (`ENUM`), fechas, vino, cantidad.
- **Stock Sala / Depósito:** Cantidades por vino y sala/depósito (`cantidad >= 0`).
- **Auditoría de Precio:** ID, vino, precio anterior, precio nuevo, fecha/hora, usuario.

---

## 6. Tecnologías y Restricciones

- **Motor:** PostgreSQL 14+.
- **Acceso a datos:** Driver nativo (**Prohibido ORM**).
- **API:** REST con JSON (OpenAPI/Swagger).
- **Front:** libre (HTML/JS, React, Vue, etc.).
- **Contenedores:** Docker y Docker Compose.
- **Regla de Oro:** La API **no recalcula** totales, descuentos ni stock: invoca las funciones y procedimientos de la base de datos.

---

## 7. Etapas del Proyecto (1 a 9)

### Etapa 1. Modelado
- **Objetivo:** DER, esquema relacional en 3FN, diccionario de datos y `001_esquema.sql`.

### Etapa 2. Integridad y Lógica en la Base de Datos (Mayor Peso)
- **Requisitos:** 
  - PKs, FKs (`RESTRICT`/`CASCADE` justificados), `NOT NULL`, `UNIQUE` (4+), `CHECK` (8+), `DEFAULT` (3+).
  - 1 `ENUM`, 1 `DOMAIN`.
  - 4 Funciones (`fn_total_comprobante`, `fn_stock_sala`, etc.).
  - 2 Procedimientos transaccionales (`sp_procesar_ingreso`, `sp_procesar_transferencia`).
  - 6 Triggers (`BEFORE`, `AFTER`, constraint trigger diferido).
  - 3 Vistas (incluyendo materializada).
  - 3 Roles (propietario, API `rw`, reportes `ro`).
  - Pruebas SQL (`db_tests.sql`) y demo de concurrencia con `FOR UPDATE`.

### Etapa 3. Carga Masiva de Datos
- **Volúmenes:** Al menos una tabla > 100.000 filas (ej. renglón de comprobante 500.000), 3+ tablas > 10.000 filas.
- **Script:** Python (`psycopg`, `Faker`) con semilla fija. Carga eficiente por lotes (`execute_values` / `COPY`).

### Etapa 4. Índices y Rendimiento
- **Requisitos:** 5+ índices (`008_indices.sql`): compuesto, parcial, sobre FK, de expresión/BRIN/INCLUDE.
- Mediciones con `EXPLAIN (ANALYZE, BUFFERS)` antes y después en al menos 3 consultas.

### Etapa 5. Consultas SQL
- Archivos: `consultas/update.sql`, `insert.sql`, `delete.sql`, `select.sql`. Probadas dentro de transacciones (`BEGIN` ... `ROLLBACK`).

### Etapa 6. API REST
- Endpoints CRUD y transaccionales. Paginación, filtros, traductor de SQLSTATE a HTTP (409, 422, 400). Pruebas automáticas y demostración de inyección SQL fallida.

### Etapa 7. Front
- Pantallas: Catálogo paginado, Alta/Edición vino, Nueva venta, Transferencias, Tablero de reportes. Sin lógica de cálculo en el cliente.

### Etapa 8. Despliegue en la Nube
- Servidor en la nube (Render, Railway, Supabase, Neon, AWS, etc.). HTTPS, puerto restringido, secretos en `.env`, backup y restauración probados.

### Etapa 9. Documentación y Defensa
- `README.md` reproducible, informe final completo, demo en vivo (10-15 min) y defensa oral individual.

---

## 8. Consultas SQL Requeridas

### 8.1 Modificación de datos (UPDATE)
- **U1:** Recalcular total de comprobantes aplicando descuento según tipo de cliente.
- **U2:** Aumentar 20% salario a empleados con >5 años de antigüedad.
- **U3:** Incrementar 13% precio de vinos de una bodega determinada.
- **U4:** Cambiar día de cierre de lunes a miércoles y viceversa en una sola sentencia.
- **U5:** Aplicar 15% descuento a los 10 vinos menos vendidos.
- **U6:** Subir a 35% el descuento a exportadores con más de 3 permisos.

### 8.2 Inserción de datos (INSERT)
- **I1:** Asociar cobertura de General Alvear al transportista con menos envíos en el último trimestre.
- **I2:** Crear maridaje «cordero al disco» y asociarlo a vinos tintos con graduación >= 14°.
- **I3:** Crear comprobante con 3 renglones dentro de una transacción.
- **I4:** Insertar nueva bodega.
- **I5:** Insertar nueva sala de venta.
- **I6:** Crear ingreso en confección de 120 botellas.

### 8.3 Borrado de datos (DELETE)
- **D1:** Borrar comprobantes de >5 años de socios del club.
- **D2:** Eliminar cepas no usadas en vinos ni parcelas.
- **D3:** Eliminar empleados de una sala dada de baja con <2 años trabajados.
- **D4:** Borrar socios sin compras dados de alta hace >5 años.
- **D5:** Eliminar ingresos procesados de hace >365 días.
- **D6:** Borrar socios sin compras de una localidad específica.

### 8.4 Consultas (SELECT)
- **S1:** Top 10 vinos más vendidos en la red.
- **S2:** Vinos vendidos en **todas** las salas (división relacional).
- **S3:** Cantidad de clientes por tipo que compraron en una sala en la última semana.
- **S4:** Top 5 salas con mayor solicitud de transferencias de un vino en últimos 15 días.
- **S5:** Salas con menor cantidad de transferencias pendientes.
- **S6:** Vinos sin stock en sala pero con stock en depósito central.
- **S7:** Transportista con mayor actividad en el último mes.
- **S8:** Ventas por sala en el último trimestre (orden descendente).

### 8.5 Consultas avanzadas (SELECT)
- **S9:** Ficha de un vino (cepas, %, bodega, maridajes, stock total).
- **S10:** Rendimiento en kg/ha por parcela y campaña (CTE + subconsulta correlacionada).
- **S11:** Ranking de vinos por sala y ventas acumuladas mensuales (`RANK() OVER`, ventana).
- **S12:** Clientes que compraron todos los vinos de una bodega / clientes sin compras de vino tinto (`NOT EXISTS` / anti-join).

---

## 9. Rúbrica de Evaluación

| Criterio | Puntos | Detalles |
| :--- | :--- | :--- |
| **Modelado (Etapa 1)** | 15 | DER, 3FN, diccionario y DDL reproducible |
| **Constraints (Etapa 2)** | 8 | Cobertura PK, FK, NOT NULL, UNIQUE, CHECK, DEFAULT |
| **Lógica y Transacciones (Etapa 2)** | 17 | Reglas RN-01 a RN-15, funciones, procedimientos, triggers, concurrencia |
| **Carga Masiva (Etapa 3)** | 8 | Volúmenes (>100k), reproducibilidad, scripts |
| **Índices y Rendimiento (Etapa 4)** | 10 | EXPLAIN, variedad de índices, costo de escritura |
| **Consultas SQL (Etapa 5)** | 12 | UPDATE, INSERT, DELETE, SELECT avanzados |
| **API (Etapa 6)** | 10 | SQL parametrizado, transacciones, traducción errores |
| **Front (Etapa 7)** | 5 | Pantallas operativas, manejo de errores de negocio |
| **Nube y Seguridad (Etapa 8)** | 10 | Despliegue, HTTPS, SSL, backup/restauración |
| **Documentación y Demo (Etapa 9)** | 5 | README, informe, commits Git, demo en vivo |
| **TOTAL** | **100** | **Nota individual ajustada por defensa oral** |

---

## 10. Estructura del Repositorio

```
/
├── README.md
├── docker-compose.yml
├── .env.example
├── db/
│   ├── migrations/
│   │   ├── 001_esquema.sql
│   │   ├── 002_constraints.sql
│   │   ├── 003_funciones.sql
│   │   ├── 004_procedimientos.sql
│   │   ├── 005_triggers.sql
│   │   ├── 006_vistas.sql
│   │   ├── 007_roles.sql
│   │   └── 008_indices.sql
│   ├── seed/
│   └── tests/
├── consultas/
│   ├── insert.sql
│   ├── update.sql
│   ├── delete.sql
│   └── select.sql
├── api/
├── front/
└── docs/
```

---

## Anexo A. Ejemplos de Código PostgreSQL

### A.1 Tipos y Dominios
```sql
CREATE TYPE estado_documento AS ENUM ('en_confeccion', 'terminado', 'procesado');
CREATE DOMAIN cuit_dom AS CHAR(11) CHECK (VALUE ~ '^[0-9]{11}$');
```

### A.2 Tabla con Constraints
```sql
CREATE TABLE vino (
    cod_vino INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    tipo VARCHAR(12) NOT NULL CHECK (tipo IN ('tinto', 'blanco', 'rosado', 'espumante')),
    anada SMALLINT NOT NULL CHECK (anada BETWEEN 1990 AND 2100),
    volumen_ml INTEGER NOT NULL CHECK (volumen_ml IN (187, 375, 750, 1500, 3000)),
    graduacion NUMERIC(4,2) NOT NULL CHECK (graduacion BETWEEN 5 AND 20),
    precio NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    cuit_bodega cuit_dom NOT NULL REFERENCES bodega (cuit) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE (nombre, anada, volumen_ml)
);

CREATE TABLE stock_sala (
    id_sala INTEGER NOT NULL REFERENCES sala_venta (id_sala) ON DELETE RESTRICT,
    cod_vino INTEGER NOT NULL REFERENCES vino (cod_vino) ON DELETE RESTRICT,
    cantidad INTEGER NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    PRIMARY KEY (id_sala, cod_vino)
);
```

### A.3 Trigger de Validación de Stock (RN-09)
```sql
CREATE OR REPLACE FUNCTION trg_validar_stock_venta() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_sala INTEGER;
BEGIN
    SELECT id_sala INTO v_sala FROM comprobante WHERE nro = NEW.nro_comprobante;
    IF fn_stock_sala(v_sala, NEW.cod_vino) < NEW.cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente del vino % en la sala % (RN-09)', NEW.cod_vino, v_sala;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_renglon_valida_stock
BEFORE INSERT ON renglon_comprobante
FOR EACH ROW EXECUTE FUNCTION trg_validar_stock_venta();
```

---

## Anexo B. Catálogos Sugeridos

- **Cepas Tintas:** Malbec, Cabernet Sauvignon, Merlot, Syrah, Bonarda, Tempranillo, Pinot Noir.
- **Cepas Blancas:** Chardonnay, Sauvignon Blanc, Torrontés, Chenin Blanc, Semillón.
- **Maridajes:** Carnes rojas (17°C), Quesos duros (16°C), Pastas salsa roja (16°C), Carnes blancas (12°C), Quesos blandos (10°C), Pescados y mariscos (8°C), Entradas (10°C), Postres (8°C).
- **Departamentos de Mendoza:** San Rafael, General Alvear, Malargüe, Luján de Cuyo, Maipú, Tupungato, Tunuyán, San Carlos, Lavalle, Rivadavia, Junín, San Martín, Santa Rosa, La Paz, Godoy Cruz, Guaymallén, Las Heras, Capital.

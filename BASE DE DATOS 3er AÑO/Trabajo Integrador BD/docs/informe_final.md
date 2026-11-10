# Informe final · Bodegas del Atuel

**Bases de Datos · Ingeniería en Sistemas · 3.º año · UTN Facultad Regional San Rafael · 2026**
Integrantes: *(completar)* · Repositorio: este · Hitos H1–H9 (ver [README](../README.md#entregables-por-hito))

## 1. Resumen

Se construyó el sistema de gestión y distribución de una vitivinícola ficticia: **29 tablas** en PostgreSQL 16 con las
**15 reglas de negocio** del enunciado implementadas *dentro de la base* (39 `CHECK`, 34 FK, 10 `UNIQUE`, 17 `DEFAULT`, 9 funciones,
3 procedimientos, 14 triggers —3 de ellos constraint triggers diferidos—, 3 vistas más 1 materializada y 3 roles), una carga
reproducible de **~500.000 renglones de venta**, 15 índices medidos con `EXPLAIN (ANALYZE, BUFFERS)`, 30 consultas SQL, una **API REST
sin ORM** de 38 operaciones, un front web y un despliegue de producción con HTTPS y TLS en la base, con backup y restauración probados.

| Número | Valor |
| :-- | --: |
| Tablas / FK / CHECK en tablas | 29 / 34 / 39 |
| Triggers / funciones / procedimientos / vistas | 14 / 9 / 3 / 4 (1 materializada) |
| Filas cargadas (`renglon_comprobante` / `comprobante` / `cliente`) | 507.134 / 160.000 / 20.000 |
| Tiempo de la carga completa | ≈ 15 s (base de 105 MB) |
| Operaciones de la API / pruebas de la API | 38 / 54 |
| Pruebas: SQL (6 suites) · consultas · front · controles de despliegue | 6 · 1 script · 9 · 29 |
| Mejora de consultas con índices | de 4× a 294× (una consulta sin mejora, documentada) |

## 2. Escenario y alcance

«Bodegas del Atuel» integra **producción** (fincas, parcelas, cepas, lotes y análisis de calidad), **elaboración** (bodegas, vinos, cortes,
maridajes), **comercialización** (clientes socio/distribuidor/exportador, comprobantes con renglones) y **logística** (depósito central,
ingresos desde bodegas por transportistas, transferencias a salas, stock por sala). El diccionario completo está en
[diccionario_datos.md](diccionario_datos.md) y el DER por módulos en [relation_entity_diagrams/](../relation_entity_diagrams/markdown/der_tpi_bodegas_del_atuel.md).

Alcance fuera del TP, por decisión explícita: autenticación de usuarios finales, multi-moneda, impuestos, devoluciones.

## 3. Modelo de datos

**Decisiones de diseño y por qué:**

* **Entidad débil `parcela`** con PK `(id_finca, nro_parcela)`; `lote_uva` la referencia por FK compuesta y `UNIQUE (parcela, campaña)` implementa RN-04.
* **Jerarquía de clientes disjunta y total.** El supertipo `cliente` guarda el discriminador `tipo_cliente`; cada subtipo tiene PK = FK compuesta
  `(id_cliente, tipo_cliente)` más un `CHECK` fijo, por lo que **un cliente no puede pertenecer a dos subtipos** (la base lo rechaza; ver
  `002_constraints_test.sql`). La *totalidad* (todo cliente tiene su fila de subtipo) la garantiza un constraint trigger diferido.
* **Relaciones N:M con atributos:** `composicion` (porcentaje), `renglon_comprobante`, `renglon_ingreso`, `renglon_transferencia`, `stock_sala`.
* **Documentos con estado** (`ingreso`, `transferencia`): `ENUM estado_documento` y transiciones por trigger (RN-10/11).
* **Normalización hasta 3FN.** El encargado regional depende de la localidad, no de la sala (RN-02), por eso es un atributo de `localidad`
  y las salas solo la referencian. Cada atributo no clave depende de toda la clave y solo de ella.
* **Redundancia controlada (y justificada):**
  `comprobante.subtotal/descuento/total` son datos derivados que se guardan para listar y reportar rápido; los **mantiene un trigger** y un
  `CHECK (total = subtotal − descuento)` los protege, nadie los carga a mano (RN-08). `renglon_comprobante.precio_unitario` no es redundante: es el
  *precio al momento de la venta* (el vino cambia de precio después). `cliente.descuento` se guarda porque la política puede diverger del
  valor base (consulta U6). El stock es *estado* mantenido por procedimientos y triggers, no derivado de los movimientos, para poder bloquearlo
  con `FOR UPDATE` y consultarlo en O(1).

## 4. Implementación en la base de datos

| Archivo | Contenido |
| :-- | :-- |
| `001_esquema.sql` | `ENUM estado_documento`, `DOMAIN cuit_dom`, 29 tablas con PK, FK (`RESTRICT`/`CASCADE` justificados en comentarios), `NOT NULL` |
| `002_constraints.sql` | `UNIQUE`, `CHECK` (positivos, rangos, listas, `vencimiento > emisión`, `total = subtotal − descuento`), `DEFAULT` |
| `003_funciones.sql` | descuento por tipo, subtotal de renglón, cálculo del comprobante, stock de sala/depósito, suma del corte, transición de estado |
| `004_procedimientos.sql` | `sp_procesar_ingreso`, `sp_procesar_transferencia` (transaccionales), `sp_refrescar_reportes` (en `006`) |
| `005_triggers.sql` | 14 triggers (3 diferidos) con SQLSTATE propios `RN005`…`RN012` |
| `006_vistas.sql` | `v_stock_vino`, `v_catalogo_vino`, `v_comprobante_detalle`, `mv_ventas_mensuales_sala` (materializada, refresco concurrente) |
| `007_roles.sql` | `bodegas_owner` / `bodegas_api` / `bodegas_ro`, `REVOKE` de PUBLIC, límites por rol |
| `008_indices.sql` | 15 índices + `random_page_cost = 1.1` |

**Detalles que conviene saber defender**

* **Constraint triggers diferidos** (`DEFERRABLE INITIALLY DEFERRED`) para RN-05 (el corte suma 100): el corte se carga en varias filas, así que
  la validación debe ocurrir al `COMMIT`, no fila por fila. También exigen que un vino nunca exista sin corte.
* **El impacto en el stock lo hacen los procedimientos**, no un `UPDATE` suelto: un trigger de estado rechaza `terminado → procesado` salvo que el
  procedimiento haya encendido un indicador de transacción (`atuel.sp_activo`). Así nadie puede saltearse el movimiento de stock.
* **`SECURITY DEFINER`** (con `search_path` fijo) en los procedimientos de proceso, los triggers de venta y la auditoría de precio: el rol de la API **no
  tiene permiso de escritura** sobre `stock_sala`, `stock_deposito` ni `auditoria_precio`, pero el stock igual se mueve, y solo por los caminos permitidos.
* **Borrar un renglón de venta no devuelve stock** a propósito (la consulta D1 depura historial; no debe fabricar stock). Un renglón de venta
  no se puede modificar en cantidad ni vino (`RN008`): se elimina y se carga otro.
* **Códigos de error propios** (`RN005`…`RN012`) para que la API traduzca por código y no por texto.

## 5. Transacciones y concurrencia

* El aislamiento por defecto de PostgreSQL es `READ COMMITTED`. La corrección de RN-09 **no depende de subir el aislamiento**: el trigger de venta
  toma `SELECT … FOR UPDATE` sobre la fila de `stock_sala` antes de validar, de modo que dos ventas del mismo vino en la misma sala se serializan
  y la segunda ve el stock ya descontado. Es más barato que `SERIALIZABLE` y evita reintentos.
* **Demostración** (`db/tests/concurrencia_demo.sh`): stock 10; la sesión A vende 8 y tarda 4 s en confirmar; la B intenta vender 8 y **queda esperando 3 s**;
  al desbloquearse ve `disponible 2` y es rechazada con `RN009`. Resultado: stock 2 y un solo renglón.
* **Sin deadlocks entre procedimientos:** `sp_procesar_*` bloquean el documento y luego las filas de stock **siempre ordenadas por `cod_vino`**.
* La API ejecuta **una transacción por operación**: una venta con un renglón sin stock no deja nada a medias (verificado: el primer renglón válido también se revierte).

## 6. Trazabilidad de las reglas de negocio

| RN | Regla | Mecanismo | Prueba |
| :-- | :-- | :-- | :-- |
| 01 | Precio único y > 0 | `vino.precio` + `ck_vino_precio_pos` | `002_constraints_test`, API `test_reglas_de_integridad…` |
| 02 | Sala en una localidad; un encargado por localidad | FK + 3FN (`localidad.encargado_regional`) | `002_constraints_test` |
| 03 | Empleado en una sola sala | `empleado.id_sala NOT NULL` FK | `002_constraints_test` |
| 04 | Una cepa por parcela; una cosecha por parcela y campaña | `parcela.id_cepa NOT NULL`, `uq_lote_parcela_campania` | `002_constraints_test`; la carga masiva (13.640 lotes) |
| 05 | El corte suma 100 | constraint trigger diferido `trg_composicion_corte` / `trg_vino_corte` | `005_reglas_test`, API `test_corte_que_no_suma_100…` |
| 06 | Descuento por tipo de cliente | `fn_descuento_tipo_cliente` + `trg_cliente_descuento` + `CHECK` de rango | `003`, `005`, API `test_el_descuento_lo_fija_la_base…` |
| 07 | Permisos de exportación, vencimiento > emisión | tabla `permiso_exportacion` + `ck_permiso_fechas` | `002_constraints_test` |
| 08 | Total = suma de renglones con descuento; no se carga a mano | `fn_calcular_comprobante` + `trg_renglon_calcula` + `trg_comprobante_importes` | `005`, API (el cliente no puede enviar `total`), 8 chequeos de la carga |
| 09 | No vender más que el stock; stock ≥ 0 | `trg_validar_stock_venta` (`FOR UPDATE`) + `CHECK (cantidad >= 0)` | `005`, `concurrencia_demo.sh`, API |
| 10 | Ingreso: `en_confeccion → terminado → procesado` | `ENUM` + `trg_ingreso_estado` + `sp_procesar_ingreso` | `005`, API `test_ciclo_completo_de_un_ingreso` |
| 11 | Ídem transferencias; fecha = hoy e inmodificable | `trg_transferencia_estado` + `sp_procesar_transferencia` | `005`, API `test_transferencia_*` |
| 12 | Documento no en confección: sin cambios en renglones | `trg_renglon_ingreso_edicion` / `trg_renglon_transf_edicion` | `005`, API |
| 13 | Auditoría de cambios de precio | `trg_vino_audita_precio` (`AFTER UPDATE`, `SECURITY DEFINER`) | `005`, API `test_edicion_audita…` |
| 14 | No borrar transportista/bodega/vino con movimientos | FK `ON DELETE RESTRICT` (+ índices de FK) | `002_constraints_test`, API `test_baja_de_vino`, medición Q9 |
| 15 | Positivos; graduación 5–20 | `CHECK` | `002_constraints_test`, API |

## 7. Carga masiva (H3)

`db/seed/cargar_datos.py` genera todo en memoria con `random.Random(42)` y `Faker.seed(42)` y carga con `COPY` en **una transacción**
(`--escala` para cargas chicas, `--fecha-ref hoy` para que «última semana/mes» tenga datos). Detalle y tiempos por tabla en
[reporte_carga.md](reporte_carga.md).

* **Reproducible:** dos corridas con la misma semilla dan hashes MD5 idénticos en cinco tablas; otra semilla da hashes distintos.
* **Coherente:** el stock final de salas y depósito sale de lo transferido, ingresado y vendido; **8 chequeos** al terminar (totales de comprobantes y
  renglones, stock de sala = transferido − vendido, stock de depósito = ingresado − transferido, cortes = 100, subtipos de cliente, triggers reactivados).
* **Triggers durante la carga:** se apagan solo los que recalculan o rechazan datos *históricos* (estados, stock, importes); los diferidos
  (corte, subtipos) quedan **activos** y validan lo cargado al `COMMIT`. Todo en una transacción: si falla, no queda nada.
* Datos pensados para las consultas del TP: ventas de más de 5 años, socios sin compras, exportadores con más de 3 permisos, vinos agotados
  en sala con stock en depósito, ventanas recientes. Volumen: 160.000 comprobantes, 507.134 renglones, 20.000 clientes, 27.241 análisis, 13.640 lotes.

## 8. Índices y rendimiento (H4)

Informe completo con planes: [informe_indices.md](informe_indices.md). Medición con `EXPLAIN (ANALYZE, BUFFERS)`, mediana de 7 corridas, tres estados
(sin índices / solo índices / índices + `random_page_cost`).

* **Compuesto** `(id_cliente, fecha DESC)`: últimas compras de un cliente, **6.2 ms → 0.02 ms** (el `Sort` desaparece).
* **BRIN** en `comprobante.fecha`: mismo tiempo que un B-tree (1.4 ms) con **24 kB en lugar de 1.112 kB**.
* **Parcial** `WHERE estado <> 'procesado'`, **de expresión** `lower(nombre)` y **`INCLUDE`** (covering) en los renglones.
* **FK sin índice cuesta (RN-14):** borrar un vino sin movimientos tardaba 22.5 ms recorriendo 507.000 renglones; con índice, 0.28 ms.
* **El índice solo no alcanzó:** hizo falta `random_page_cost = 1.1` (SSD) para que el planificador lo use (27.5 → 3.8 ms).
* **Lo que no mejora, dicho:** el ranking global de vinos recorre el 100 % de los renglones (≈ 70 ms, sin cambio); se resolvería con una vista materializada.
* **Costo de escritura:** +20 % por venta (0.75 → 0.90 ms), +14 % en la carga masiva, +27 MB de espacio.

## 9. Consultas SQL (H5)

30 consultas en [consultas/](../consultas/): 6 `UPDATE`, 6 `INSERT`, 6 `DELETE`, 12 `SELECT` (división relacional con `NOT EXISTS`, CTE + subconsulta
correlacionada, `RANK()` y `SUM() OVER`, anti-join). Cada modificación corre en su transacción con `ROLLBACK`.
`db/tests/consultas_test.sh` compara las filas afectadas con conteos independientes y verifica que la base quede intacta; al alterar a propósito dos
sentencias, el script lo detectó. Interpretaciones tomadas (U1, U5, I1, D1, S12a) están documentadas en los comentarios de cada archivo.

## 10. API REST (H6)

FastAPI + `psycopg` ([api/README.md](../api/README.md), [openapi.json](openapi.json)). **38 operaciones**: CRUD de vinos y clientes, ventas transaccionales,
ciclo de vida de ingresos y transferencias, reportes y catálogos. Paginación (`page`, `page_size ≤ 100`), filtros y orden por lista blanca.

* **La API no recalcula nada** (regla de oro): un comprobante se crea enviando solo cliente, sala, vinos y cantidades.
* **Traductor SQLSTATE → HTTP:** 400 mal formada, 404 no existe, **409** conflicto (`RN009` sin stock, `RN010-012` estado, `23505`, borrado con
  dependencias), **422** regla violada (`RN005`, `CHECK`, referencia inexistente), 403/503. Cuerpo uniforme `{error:{estado,sqlstate,mensaje,regla}}`;
  nunca se filtran detalles internos de SQL.
* **Seguridad:** conecta como `bodegas_api` (sin superusuario ni DDL ni escritura de stock). SQL parametrizado; el `ORDER BY` sale de un `Enum` cerrado;
  los `LIKE` escapan `%`/`_`/`\`. **Demostración de inyección fallida** en vivo (`api/demo_inyeccion.sh`: 7 ataques, conteos idénticos) y 15 pruebas automáticas.
* **54 pruebas** contra una base descartable armada con las migraciones reales.

## 11. Front (H7)

HTML + JS de módulos ES, sin dependencias ([front/README.md](../front/README.md)). Catálogo paginado con filtros, alta/edición/baja de vino con su corte,
**nueva venta**, transferencias e ingresos (confeccionar → terminar → procesar) y **tablero de reportes**. **Sin lógica de cálculo en el cliente**:
los importes llegan de la base; los errores de negocio se muestran con su regla («Conflicto · RN-09 — Stock insuficiente…»). Datos como texto, nunca HTML
(sin XSS) y CSP sin `unsafe-inline`; ambos controles son pruebas automáticas. Verificado en un navegador real, en escritorio y móvil.

## 12. Nube y seguridad (H8)

[despliegue_nube.md](despliegue_nube.md). Stack de producción (`docker-compose.prod.yml`): Caddy con HTTPS y HSTS → nginx → API → PostgreSQL **con TLS
obligatorio** (`hostssl`, SCRAM-SHA-256, la API verifica el certificado con `verify-full`), único puerto publicado 80/443, redes internas sin salida a internet,
API sin root y con sistema de archivos de solo lectura, secretos solo en `.env.prod`/`certs/` (ignorados por git).
`scripts/verificar_despliegue.sh` ejecuta **29 controles** sobre el stack en marcha. **Backup y restauración probados:** `pg_dump -Fc` + SHA-256 + cifrado AES-256;
el simulacro restaura en una base temporal y compara todo (29 tablas, huellas de contenido, privilegios, índices, triggers); un archivo alterado se rechaza; y se
verificó una **recuperación ante desastre** (backup de desarrollo restaurado sobre producción, la API por HTTPS devolvió los datos).

> **Pendiente y declarado:** publicar el stack en un servidor con URL pública (requiere una cuenta de nube y un dominio). Los pasos están listos y el
> mismo stack se verificó localmente; la sección 6 de `despliegue_nube.md` queda para registrar la URL.

## 13. Evidencia de pruebas

| Suite | Qué valida | Resultado |
| :-- | :-- | :-- |
| `db/tests/002…008_*_test.sql` (6) | constraints, funciones, procedimientos, triggers, vistas, roles, índices (SQLSTATE exacto en los casos negativos) | OK |
| mutaciones | al desactivar 6 triggers y dar un permiso de más, las pruebas fallan (no pasan «en vacío») | verificado |
| `cargar_datos.py` | 8 chequeos de coherencia + reproducibilidad por hash | OK |
| `consultas_test.sh` | filas afectadas = conteo independiente; base intacta | OK (y detecta mutaciones) |
| `concurrencia_demo.sh` | RN-09 bajo concurrencia | OK |
| `api/tests` (54) | CRUD, reglas → HTTP, atomicidad, paginación, inyección, privilegios | OK |
| `front/test` (9) | utilidades y controles estáticos (sin `innerHTML`, sin cálculos de importes) | OK |
| `probar_backup.sh` | backup cifrado → restauración → comparación | OK (desarrollo y producción) |
| `verificar_despliegue.sh` (29) | red, HTTPS, TLS en la base, contenedores, secretos | OK |

Todo se ejecuta desde cero con `scripts/verificar_todo.sh`.

## 14. Decisiones y compromisos

* **Triggers sobre lógica en la aplicación:** una regla en la API se puede saltear con otro cliente SQL; en la base, no. Costo: más difícil de depurar y de portar.
* **Stock como estado, no derivado:** lecturas O(1) y bloqueo por fila, a cambio de mantenerlo en cada movimiento (por eso solo lo escriben procedimientos y triggers).
* **FastAPI sobre Node/Spring:** OpenAPI automático y `psycopg` expone el SQL sin capa intermedia; el TP prohíbe ORM.
* **Front sin framework:** cero dependencias y nada que compilar; menos superficie de ataque y fácil de explicar.
* **Caddy en producción:** HTTPS automático (Let's Encrypt) con 10 líneas de configuración.

## 15. Limitaciones y trabajo futuro

* Publicar en un servidor real y registrar la URL (pendiente).
* Autenticación de usuarios finales (OIDC/JWT) y límite de peticiones; hoy la API es abierta detrás del proxy (el TP no pide autenticación compleja).
* Vista materializada para el ranking global de vinos (la única consulta que no se acelera con índices).
* Recuperación a un instante exacto (PITR con archivado de WAL); el backup actual es lógico y diario.
* Anulación de ventas con devolución de stock (hoy borrar es depuración de historial).
* Particionado de `comprobante` por fecha si el volumen creciera un orden de magnitud.

# Guía de defensa

Todos los integrantes deben poder explicar el modelo y las reglas (la nota final es individual). Este documento tiene
(1) un **guion de demo en vivo de 12 minutos**, (2) **respuestas preparadas** a las preguntas típicas y (3) un **plan B** si algo falla.

## 1. Antes de entrar (5 minutos)

```bash
docker compose up -d --build
.venv/bin/python db/seed/cargar_datos.py --limpiar --fecha-ref hoy     # datos con ventanas "última semana" vigentes
docker compose ps                                                      # base (healthy), api y front arriba
open http://localhost:8080 ; open http://localhost:8000/docs
```
Tener abiertas: una terminal con `psql` (`docker exec -it bodegas_atuel_postgres sh -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB'`),
`docs/informe_indices.md` y el DER. Si hay tiempo: `scripts/verificar_todo.sh` (~3 min) deja un resumen verde para mostrar.

## 2. Guion de la demo (12 min)

| Min | Qué mostrar | Qué decir |
| :-- | :-- | :-- |
| 0–1 | DER (módulos A–D) y `docs/diccionario_datos.md` | Jerarquía de clientes disjunta y total, entidad débil `parcela`, N:M con atributos. 3FN: el encargado depende de la localidad. |
| 1–4 | **Reglas en la base, desde `psql`:** `INSERT` de un vino sin corte → `COMMIT` falla (`RN005`); `UPDATE vino SET precio=0` → `ck_vino_precio_pos`; `DELETE` de un vino vendido → FK (RN-14) | La regla vive en la base: da igual qué cliente la ataque. Constraint trigger **diferido** porque el corte se carga en varias filas. |
| 4–6 | **Venta desde el front** (`/ventas/nueva`): cliente socio + 2 vinos → mostrar importes calculados · repetir con cantidad enorme → cartel «Conflicto · RN-09» | La API/Front solo envían cliente, sala, vinos y cantidades. Precio, descuento 10 %, totales y stock los hace la base. |
| 6–7 | **Concurrencia:** `bash db/tests/concurrencia_demo.sh` | Dos ventas simultáneas: la segunda **espera** (`FOR UPDATE`) y se rechaza con `disponible 2`. Sin subir el aislamiento. |
| 7–8 | **Ciclo de una transferencia** en el front: crear → terminar → procesar; intentar procesar una de 9.999.999 unidades → RN-11 | Estados por trigger; `procesado` solo lo fija el procedimiento (`atuel.sp_activo`); atómico: no queda nada a medias. |
| 8–10 | **Rendimiento:** `docs/informe_indices.md` — Q2 (6.2 → 0.02 ms), Q9 (FK sin índice: 22 ms), BRIN 24 kB vs 1.112 kB, el caso **sin mejora** | Cada índice responde a una consulta medida; mostramos también lo que no mejora y lo que cuesta (+20 % escritura). |
| 10–11 | **Seguridad:** `bash api/demo_inyeccion.sh` (7 ataques, conteos iguales) · `scripts/verificar_despliegue.sh` | Parámetros `%s`, lista blanca de `ORDER BY`, rol sin permiso de escritura de stock, TLS en la base. |
| 11–12 | **Backup:** `scripts/probar_backup.sh` | Backup cifrado → restauración → comparación; un archivo alterado se rechaza. |

## 3. Preguntas típicas y respuestas

**Modelado**
* *¿Por qué `encargado_regional` está en `localidad` y no en `sala`?* RN-02: es único por localidad. Si estuviera en la sala se repetiría por cada sala de la localidad (dependencia parcial → viola 3FN y permite inconsistencias).
* *¿Cómo garantizan que un cliente es de un solo subtipo?* El discriminador `tipo_cliente` + FK compuesta `(id_cliente, tipo_cliente)` desde cada subtipo + `CHECK` fijo. Intentar cargarlo en dos subtipos da error de FK (probado). La **totalidad** la fuerza un constraint trigger diferido.
* *¿Por qué guardan `total` si se puede calcular?* Dato derivado deliberado para listar/reportar rápido; lo mantiene un trigger y lo protege `CHECK (total = subtotal − descuento)`. Nadie lo carga a mano.
* *¿Y `precio_unitario` en el renglón, no es redundante?* No: es el precio *al momento de la venta*; el vino cambia de precio después (auditado por RN-13).

**Lógica en la base**
* *¿Por qué triggers y no validar en la API?* Una regla en la aplicación se saltea con otro cliente SQL, una migración o un script. En la base es la última línea de defensa y vale para todos.
* *¿Qué es un constraint trigger diferido y cuándo hace falta?* Se evalúa al `COMMIT` (`DEFERRABLE INITIALLY DEFERRED`). Hace falta cuando la regla involucra varias filas que se cargan juntas (el corte suma 100) o varias tablas (cliente ↔ subtipo).
* *¿Para qué `SECURITY DEFINER`?* Para que el rol de la API **no pueda escribir el stock** pero el stock igual se mueva, solo por procedimientos y triggers. Siempre con `search_path` fijo para evitar suplantación de objetos.
* *¿Qué impide hacer `UPDATE ingreso SET estado='procesado'` a mano?* El trigger de estado exige que el procedimiento haya encendido `atuel.sp_activo` en esa transacción; si no, `RN010`.
* *¿Por qué borrar un renglón de venta no devuelve stock?* Es una decisión: D1 depura historial viejo; devolver stock fabricaría inventario. Anular una venta sería otra operación (trabajo futuro).

**Transacciones y concurrencia**
* *¿Qué nivel de aislamiento usan y por qué alcanza?* `READ COMMITTED` (default). RN-09 se asegura con `SELECT … FOR UPDATE` de la fila de stock antes de validar: serializa ventas del mismo vino y sala sin los reintentos de `SERIALIZABLE`.
* *¿Qué pasa si dos procesos procesan documentos a la vez?* Cada procedimiento bloquea el documento y luego las filas de stock **ordenadas por `cod_vino`**: mismo orden de bloqueos → sin deadlock. Probado en `concurrencia_demo.sh`.
* *¿Qué es atomicidad acá?* Una venta con un renglón sin stock no deja nada: ni comprobante ni los renglones válidos (probado en la API y con `ROLLBACK`).

**Índices**
* *¿Por qué ese índice?* Cada uno está ligado a una consulta medida (tabla de §3 del informe de índices). Ejemplo: `(id_cliente, fecha DESC)` entrega las filas ya ordenadas, el `LIMIT 20` corta sin `Sort`.
* *¿Cuándo un índice no sirve?* Cuando la consulta lee casi toda la tabla: el ranking global de vinos no mejoró (≈70 ms antes y después). Lo dijimos y propusimos una vista materializada.
* *¿Por qué BRIN en `comprobante.fecha`?* Los comprobantes se insertan en orden cronológico → la fecha está ordenada en disco. Misma velocidad que B-tree con 24 kB en vez de 1.112 kB. Si los datos dejaran de estar ordenados, habría que `CLUSTER` o volver a B-tree.
* *¿Qué hizo `random_page_cost = 1.1`?* El valor por defecto (4.0) asume disco giratorio y hacía preferir un `Seq Scan` de 160.000 filas antes que 1.600 búsquedas por PK. Con 1.1 (SSD) la consulta bajó de 27 a 3.8 ms.
* *¿Qué cuesta tener índices?* +20 % por venta (0.75 → 0.90 ms), +27 MB. Por eso no se indexó todo (tablas chicas y FK que nunca se borran).
* *¿Para qué sirve un índice sobre una FK?* PostgreSQL no lo crea solo. Sin él, `DELETE` en la tabla padre recorre la hija entera para verificar RN-14: 22.5 ms vs 0.28 ms al borrar un vino.

**API y seguridad**
* *¿Por qué sin ORM?* El TP lo prohíbe y además el SQL queda a la vista: se ve exactamente qué consulta corre y con qué parámetros.
* *¿Cómo evitan la inyección SQL?* Todo valor del usuario va como parámetro `%s`; lo único interpolado son fragmentos constantes; el `ORDER BY` viene de un `Enum` cerrado; los `LIKE` escapan `%`, `_`, `\`. Demo y 15 pruebas.
* *¿Por qué 409 y 422?* 409 = conflicto con el *estado actual* (sin stock, transición inválida, borrar con dependencias); 422 = el dato es válido en forma pero viola una *regla* (CHECK, corte ≠ 100). 400 = mal formado. Se traduce por SQLSTATE, no por texto.
* *¿Qué puede hacer la API en la base?* Es `bodegas_api`: CRUD de datos de negocio y `EXECUTE` de funciones/procedimientos; **no** escribe stock ni auditoría, no hace DDL, no es superusuario.
* *¿Dónde están los secretos?* En `.env` / `.env.prod` y `certs/`, ignorados por git; hay un control automático que busca esos valores en los archivos versionados.

**Nube y backup**
* *¿Qué conexiones van cifradas?* HTTPS en el borde (HSTS) y TLS en la base (`hostssl`, la API verifica con `verify-full`). El control lo comprueba contra `pg_stat_ssl`: todas las conexiones de la API usan TLS 1.3.
* *¿Cómo saben que el backup sirve?* Lo restauramos de verdad (`probar_backup.sh`): 29 tablas, huellas MD5 de contenido, privilegios, índices, triggers y la vista materializada coinciden con el original; un byte alterado se rechaza. También se restauró sobre producción (recuperación ante desastre).
* *¿RPO/RTO?* Con backup diario: RPO 24 h. Restaurar toma segundos a minutos con este volumen. Para RPO menor haría falta archivado de WAL (PITR): trabajo futuro.
* *¿Está publicado en la nube?* **Todavía no**: el stack de producción está listo y verificado localmente; falta la cuenta/servidor/dominio (pasos en `docs/despliegue_nube.md`). Decirlo con claridad.

## 4. Plan B

| Si falla… | Hacer |
| :-- | :-- |
| Docker no levanta | Mostrar el informe final + `docs/reporte_carga.md` + `docs/informe_indices.md` y correr solo las suites SQL contra Postgres local |
| Datos con ventanas vacías (consultas «última semana» sin filas) | `cargar_datos.py --limpiar --fecha-ref hoy` (15 s) |
| La demo de concurrencia queda colgada | Es normal que B espere ~3 s; si se cuelga, `docker compose restart db` y repetir |
| Pregunta que no sabés | Decir qué mecanismo usaste y dónde está el código; todo está en `db/migrations/` con comentarios que citan la RN |

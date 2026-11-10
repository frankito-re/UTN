# API REST · Bodegas del Atuel

FastAPI + `psycopg` (driver nativo, **sin ORM**). La API no calcula nada: totales, descuentos,
precios de venta, stock y estados los resuelven las funciones, procedimientos y triggers de la base.

## Levantar

```bash
docker compose up -d --build        # base + API
open http://localhost:8000/docs     # Swagger UI (OpenAPI en /openapi.json y en docs/openapi.json)
```

La API se conecta como **`bodegas_api`** (privilegios mínimos, `db/migrations/007_roles.sql`): no puede
escribir stock ni auditoría directamente ni hacer DDL. La clave sale de `API_DB_PASSWORD` en `.env`.

## Endpoints

| Recurso | Operaciones |
| :-- | :-- |
| `/vinos` | `GET` paginado con filtros (`q`, `tipo`, `cuit_bodega`, `precio_min/max`, `con_stock`, `orden`, `sentido`) · `GET/PUT/DELETE /{cod}` · `POST` (con corte) · `GET /{cod}/precios` |
| `/clientes` | `GET` (búsqueda por prefijo) · `GET /{id}` · `POST` (con subtipo) |
| `/comprobantes` | `GET` paginado (`id_sala`, `id_cliente`, `desde`, `hasta`) · `GET /{nro}` · `POST` venta transaccional |
| `/ingresos`, `/transferencias` | `GET`, `GET /{id}`, `POST`, `POST /{id}/renglones`, `DELETE /{id}/renglones/{vino}`, `POST /{id}/terminar`, `POST /{id}/procesar` |
| `/reportes` | `GET /ventas-mensuales`, `POST /refrescar`, `GET /top-vinos`, `GET /stock-critico` |
| catálogos | `/cepas`, `/bodegas`, `/maridajes`, `/transportistas`, `/localidades`, `/salas`, `/salas/{id}/stock` |

Paginación: `?page=1&page_size=20` (máx. 100) → `{items, page, page_size, total, pages}`.

## Errores (SQLSTATE → HTTP)

Cuerpo uniforme: `{"error": {"estado", "sqlstate", "mensaje", "regla"?, "restriccion"?}}`.

| HTTP | Cuándo | Ejemplos |
| :-- | :-- | :-- |
| 400 | petición mal formada (tipo, formato, campo desconocido, parámetro fuera de rango) | `orden=inventado`, `page_size=1000` |
| 404 | no existe el recurso | `GET /vinos/999999` |
| 409 | conflicto de estado o de integridad | `RN009` sin stock · `RN010/011/012` transición o edición inválida · `23505` duplicado · borrar con dependencias (RN-14) |
| 422 | viola una regla de integridad | `RN005` corte ≠ 100 · `23514` CHECK (precio ≤ 0, graduación) · `23503` referencia inexistente · `23502` dato obligatorio |
| 403 / 503 | privilegio insuficiente / base no disponible | |

La tabla vive en `app/errores.py`. Los detalles internos de SQL nunca se devuelven.

## Seguridad frente a inyección SQL

* Todo valor del usuario va como parámetro (`%s`); nunca se concatena en el texto SQL.
* Lo único que se interpola son fragmentos constantes del código; el `ORDER BY` sale de un `Enum` cerrado.
* Los `LIKE` escapan `%`, `_` y `\` (`db.like_literal`).
* Demostración en vivo: `bash api/demo_inyeccion.sh` (envía 7 ataques reales y cuenta las filas antes y después).

## Pruebas

```bash
.venv/bin/pip install -r api/requirements-dev.txt
cd api && ../.venv/bin/python -m pytest          # 54 pruebas
```

Las pruebas crean una base descartable `bodegas_api_test` con las migraciones reales `001..008`, corren
la API contra ella conectándose como `bodegas_api` y la borran al terminar. Requieren el contenedor de
Postgres levantado y `.env`. La base del proyecto no se toca.

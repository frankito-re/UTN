# Bodegas del Atuel · Sistema de gestión y distribución

Trabajo Práctico Integrador de **Bases de Datos** (Ingeniería en Sistemas, 3.º año · UTN FRSR · 2026).
Una empresa vitivinícola ficticia que integra producción de uva y vino con su distribución y venta en una red de salas.
**El corazón del sistema es la base de datos PostgreSQL**: el modelo, las reglas de negocio (constraints, funciones,
procedimientos y triggers), los índices y las consultas viven en SQL; la API y el front solo la exponen.

| | |
| :-- | :-- |
| **Motor** | PostgreSQL 16 (el TP pide ≥ 14) |
| **API** | FastAPI + `psycopg` (driver nativo, **sin ORM**), SQL escrito a mano y parametrizado |
| **Front** | HTML + JavaScript sin dependencias, servido por nginx |
| **Contenedores** | Docker Compose (desarrollo y producción) |
| **Integrantes** | *(completar: nombres y rol de cada etapa)* |
| **URL pública** | *(pendiente de publicar: ver [docs/despliegue_nube.md](docs/despliegue_nube.md))* |

## Arranque rápido

Requisitos: Docker con Compose. Para la carga de datos y las pruebas: Python 3.11+ y Node 20+.

```bash
cp .env.example .env                       # y cambiar las claves (POSTGRES_PASSWORD, API_DB_PASSWORD, RO_DB_PASSWORD)
docker compose up -d --build               # base (migraciones 001..008 automáticas) + API + front
python3 -m venv .venv && .venv/bin/pip install -r api/requirements-dev.txt -r db/seed/requirements.txt
.venv/bin/python db/seed/cargar_datos.py --limpiar --fecha-ref hoy    # ~500.000 renglones de venta en ~15 s
```

| Servicio | URL |
| :-- | :-- |
| Aplicación (front) | http://localhost:8080 |
| API + Swagger UI | http://localhost:8000/docs (contrato OpenAPI: [docs/openapi.json](docs/openapi.json)) |
| PostgreSQL | `localhost:5435` (usuario propietario del `.env`) |

> Las migraciones de `db/migrations/` corren solo **la primera vez** que se crea el volumen. Para rehacer la base:
> `docker compose down -v && docker compose up -d`.

## Verificar todo desde cero (una sola orden)

```bash
scripts/verificar_todo.sh       # recrea el stack y corre las 15 verificaciones de abajo (~3 min)
```

| Qué se prueba | Comando suelto |
| :-- | :-- |
| Constraints, funciones, procedimientos, triggers, vistas, roles e índices (6 suites SQL, base vacía) | `docker exec -i bodegas_atuel_postgres sh -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/005_reglas_test.sql` |
| Carga masiva reproducible + 8 chequeos de coherencia (stock, totales, cortes, subtipos) | `.venv/bin/python db/seed/cargar_datos.py --limpiar` |
| Consultas U1-U6, I1-I6, D1-D6, S1-S12 | `bash db/tests/consultas_test.sh` |
| Concurrencia (dos ventas simultáneas, `FOR UPDATE`) | `bash db/tests/concurrencia_demo.sh` |
| API (54 pruebas + inyección SQL) | `cd api && ../.venv/bin/python -m pytest` · `bash api/demo_inyeccion.sh` |
| Front (utilidades y controles estáticos de seguridad) | `node --test "front/test/*.test.mjs"` |
| Backup cifrado → restauración → comparación | `scripts/probar_backup.sh` |
| Seguridad del despliegue de producción (29 controles) | `scripts/verificar_despliegue.sh` |

## Entregables por hito

| Hito | Etapa | Dónde está |
| :-- | :-- | :-- |
| H1 | Modelado | DER en [relation_entity_diagrams/](relation_entity_diagrams/markdown/der_tpi_bodegas_del_atuel.md), esquema [`001_esquema.sql`](db/migrations/001_esquema.sql), [diccionario de datos](docs/diccionario_datos.md) |
| H2 | Integridad y lógica en la base | [`002_constraints`](db/migrations/002_constraints.sql) · [`003_funciones`](db/migrations/003_funciones.sql) · [`004_procedimientos`](db/migrations/004_procedimientos.sql) · [`005_triggers`](db/migrations/005_triggers.sql) · [`006_vistas`](db/migrations/006_vistas.sql) · [`007_roles`](db/migrations/007_roles.sql) · pruebas en [db/tests/](db/tests/) |
| H3 | Carga masiva | [db/seed/cargar_datos.py](db/seed/cargar_datos.py) · [reporte de conteos y tiempos](docs/reporte_carga.md) |
| H4 | Índices y rendimiento | [`008_indices.sql`](db/migrations/008_indices.sql) · [informe con EXPLAIN antes/después](docs/informe_indices.md) |
| H5 | Consultas SQL | [consultas/](consultas/) (`insert`, `update`, `delete`, `select`) |
| H6 | API | [api/](api/README.md) · [OpenAPI](docs/openapi.json) |
| H7 | Front | [front/](front/README.md) |
| H8 | Nube y seguridad | [docs/despliegue_nube.md](docs/despliegue_nube.md) · `docker-compose.prod.yml` · `scripts/` (**publicación en un servidor real: pendiente**) |
| H9 | Documentación y defensa | [Informe final](docs/informe_final.md) · [Guía de defensa](docs/guia_defensa.md) · este README |

## Estructura del repositorio

```
├── docker-compose.yml          desarrollo (base + API + front)        ├── api/        FastAPI + pruebas
├── docker-compose.prod.yml     producción (HTTPS, TLS en la base)     ├── front/      HTML/JS + nginx
├── .env.example                variables (los .env reales NO se versionan)
├── db/
│   ├── migrations/             001_esquema … 008_indices, 090_roles_passwords.sh
│   ├── seed/                   carga masiva reproducible (Python + COPY)
│   └── tests/                  pruebas SQL, consultas, concurrencia, medición de rendimiento
├── consultas/                  insert.sql · update.sql · delete.sql · select.sql
├── scripts/                    backup, restore, simulacro, despliegue, verificación integral
├── deploy/                     Caddyfile, pg_hba.conf, entrypoint de la base con TLS
└── docs/                       informe final, guía de defensa, diccionario, informes de carga e índices, OpenAPI, despliegue
```

## Las ideas que sostienen el diseño

1. **La base es la autoridad.** Las 15 reglas de negocio (RN-01 a RN-15) están implementadas en PostgreSQL; la API solo
   traduce sus errores a HTTP (`RN009` → 409 «sin stock», `RN005` → 422 «el corte no suma 100»…). Ninguna capa recalcula
   totales, descuentos ni stock. Matriz de trazabilidad regla → mecanismo → prueba en el [informe final](docs/informe_final.md#6-trazabilidad-de-las-reglas-de-negocio).
2. **Cada decisión está medida.** Los índices se justifican con `EXPLAIN (ANALYZE, BUFFERS)` antes y después, **incluido lo
   que no mejora** (ranking global) y lo que costó (escritura +20 %).
3. **Reproducible de punta a punta.** Misma semilla → mismos datos (verificado con hashes); un comando recrea y verifica todo.
4. **Seguridad por capas, con evidencia:** roles de mínimo privilegio, `SECURITY DEFINER` para el stock, SQL parametrizado,
   CSP estricta, TLS en la base, secretos fuera del repositorio, backups cifrados y restauración probada.

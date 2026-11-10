"""Acceso a la base: pool de conexiones y helpers de SQL PARAMETRIZADO.

Regla del proyecto: SQL escrito a mano con el driver nativo (psycopg), sin ORM.
Todo valor del usuario viaja como parametro (%s); lo unico que se interpola en
el texto SQL son fragmentos constantes definidos en el codigo (columnas,
ORDER BY elegidos de un diccionario cerrado), nunca texto recibido del cliente.
"""
import math
import os
from contextlib import contextmanager

from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

_pool: ConnectionPool | None = None


def conninfo() -> str:
    """La API se conecta SIEMPRE como bodegas_api (privilegios minimos, 007_roles.sql)."""
    return make_conninfo(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5435"),
        dbname=os.environ.get("DB_NAME", "bodegas_atuel"),
        user=os.environ.get("DB_USER", "bodegas_api"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout="5",
        application_name="bodegas-api",
        # En produccion: DB_SSLMODE=verify-full + DB_SSLROOTCERT (la conexion a la base va cifrada
        # y se verifica el certificado del servidor). make_conninfo descarta los valores None.
        sslmode=os.environ.get("DB_SSLMODE") or None,
        sslrootcert=os.environ.get("DB_SSLROOTCERT") or None,
    )


def abrir_pool() -> None:
    global _pool
    _pool = ConnectionPool(conninfo(), min_size=1, max_size=int(os.environ.get("DB_POOL_MAX", "10")),
                           kwargs={"row_factory": dict_row}, open=False)
    # Reintenta hasta 60 s: al arrancar con docker compose la base puede estar iniciando.
    _pool.open(wait=True, timeout=60)


def cerrar_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


@contextmanager
def transaccion():
    """Una transaccion por operacion: COMMIT al salir bien, ROLLBACK si hay excepcion."""
    with _pool.connection() as conn:
        yield conn


def uno(conn, sql, params=()):
    return conn.execute(sql, params).fetchone()


def todos(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()


def validar_diferidos(conn) -> None:
    """Dispara ahora los constraint triggers diferidos (corte = 100 %, subtipo de
    cliente): un error aparece dentro de la operacion y no recien en el COMMIT."""
    conn.execute("SET CONSTRAINTS ALL IMMEDIATE")


def like_literal(texto: str) -> str:
    """Escapa % _ \\ para que el texto del usuario se busque literalmente en un LIKE."""
    return texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def pagina(conn, columnas: str, desde_donde: str, params: tuple, orden: str, page: int, page_size: int) -> dict:
    """Pagina una consulta. `columnas`, `desde_donde` y `orden` son constantes del
    codigo (el ORDER BY sale de una lista blanca); `params` son los valores."""
    total = uno(conn, f"SELECT count(*) AS n {desde_donde}", params)["n"]
    items = todos(conn, f"SELECT {columnas} {desde_donde} ORDER BY {orden} LIMIT %s OFFSET %s",
                  (*params, page_size, (page - 1) * page_size))
    return {"items": items, "page": page, "page_size": page_size, "total": total,
            "pages": math.ceil(total / page_size) if total else 0}

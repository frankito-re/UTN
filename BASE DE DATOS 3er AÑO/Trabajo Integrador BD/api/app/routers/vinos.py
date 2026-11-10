from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from .. import db
from ..schemas import Pagina, PrecioHistorico, TipoVino, VinoDetalle, VinoIn, VinoOut, VinoUpdate
from .comun import Paginacion

router = APIRouter(prefix="/vinos", tags=["Vinos"])

COLUMNAS = ("cod_vino, nombre, tipo, anada, volumen_ml, graduacion, precio, bodega, corte, "
            "stock_deposito::int, stock_salas::int, stock_total::int")


class Orden(str, Enum):
    nombre = "nombre"
    precio = "precio"
    anada = "anada"
    stock = "stock"


class Sentido(str, Enum):
    asc = "asc"
    desc = "desc"


# Lista blanca: el valor del enum elige un fragmento constante; el texto del cliente nunca llega al SQL.
ORDEN_SQL = {Orden.nombre: "nombre", Orden.precio: "precio", Orden.anada: "anada", Orden.stock: "stock_total"}


def _detalle(conn, cod_vino: int) -> dict:
    v = db.uno(conn, f"""SELECT {COLUMNAS},
                                (SELECT v.cuit_bodega FROM vino v WHERE v.cod_vino = c.cod_vino) AS cuit_bodega
                           FROM v_catalogo_vino c WHERE cod_vino = %s""", (cod_vino,))
    if v is None:
        raise HTTPException(404, f"No existe el vino {cod_vino}.")
    v["detalle_corte"] = db.todos(conn, """
        SELECT ce.id_cepa, ce.nombre AS cepa, co.porcentaje FROM composicion co
          JOIN cepa ce USING (id_cepa) WHERE co.cod_vino = %s ORDER BY co.porcentaje DESC, ce.nombre""", (cod_vino,))
    v["maridajes"] = db.todos(conn, """
        SELECT m.id_maridaje, m.nombre, m.temperatura_servicio FROM vino_maridaje vm
          JOIN maridaje m USING (id_maridaje) WHERE vm.cod_vino = %s ORDER BY m.nombre""", (cod_vino,))
    return v


def _guardar_corte(conn, cod_vino: int, corte) -> None:
    conn.execute("DELETE FROM composicion WHERE cod_vino = %s", (cod_vino,))
    with conn.cursor() as cur:
        cur.executemany("INSERT INTO composicion (cod_vino, id_cepa, porcentaje) VALUES (%s, %s, %s)",
                        [(cod_vino, c.id_cepa, c.porcentaje) for c in corte])


def _guardar_maridajes(conn, cod_vino: int, maridajes: list[int]) -> None:
    conn.execute("DELETE FROM vino_maridaje WHERE cod_vino = %s", (cod_vino,))
    with conn.cursor() as cur:
        cur.executemany("INSERT INTO vino_maridaje (cod_vino, id_maridaje) VALUES (%s, %s)",
                        [(cod_vino, m) for m in sorted(set(maridajes))])


@router.get("", response_model=Pagina[VinoOut], summary="Catalogo de vinos (paginado, con filtros)")
def listar(pag: Paginacion = Depends(),
           q: str | None = Query(None, max_length=80, description="Texto contenido en el nombre"),
           tipo: TipoVino | None = None,
           cuit_bodega: str | None = Query(None, pattern=r"^\d{11}$"),
           precio_min: Decimal | None = None,
           precio_max: Decimal | None = None,
           con_stock: bool | None = Query(None, description="true: stock total > 0; false: sin stock"),
           orden: Orden = Orden.nombre,
           sentido: Sentido = Sentido.asc):
    cond, params = [], []
    if q:
        cond.append("nombre ILIKE %s")
        params.append(f"%{db.like_literal(q)}%")
    if tipo:
        cond.append("tipo = %s")
        params.append(tipo.value)
    if cuit_bodega:
        cond.append("cod_vino IN (SELECT cod_vino FROM vino WHERE cuit_bodega = %s)")
        params.append(cuit_bodega)
    if precio_min is not None:
        cond.append("precio >= %s")
        params.append(precio_min)
    if precio_max is not None:
        cond.append("precio <= %s")
        params.append(precio_max)
    if con_stock is not None:
        cond.append("stock_total > 0" if con_stock else "stock_total = 0")
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, COLUMNAS, f"FROM v_catalogo_vino {donde}", tuple(params),
                         f"{ORDEN_SQL[orden]} {sentido.value}, cod_vino", pag.page, pag.page_size)


@router.get("/{cod_vino}", response_model=VinoDetalle, summary="Ficha de un vino")
def obtener(cod_vino: int):
    with db.transaccion() as conn:
        return _detalle(conn, cod_vino)


@router.post("", response_model=VinoDetalle, status_code=201, summary="Alta de un vino con su corte")
def crear(vino: VinoIn, response: Response):
    with db.transaccion() as conn:
        cod = db.uno(conn, """
            INSERT INTO vino (nombre, tipo, anada, volumen_ml, graduacion, precio, cuit_bodega)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING cod_vino""",
                     (vino.nombre, vino.tipo.value, vino.anada, vino.volumen_ml, vino.graduacion,
                      vino.precio, vino.cuit_bodega))["cod_vino"]
        _guardar_corte(conn, cod, vino.corte)
        if vino.maridajes:
            _guardar_maridajes(conn, cod, vino.maridajes)
        db.validar_diferidos(conn)           # RN-05: el corte debe sumar 100
        resultado = _detalle(conn, cod)
    response.headers["Location"] = f"/vinos/{cod}"
    return resultado


@router.put("/{cod_vino}", response_model=VinoDetalle, summary="Edicion de un vino (el cambio de precio queda auditado)")
def editar(cod_vino: int, vino: VinoUpdate):
    with db.transaccion() as conn:
        fila = db.uno(conn, """
            UPDATE vino SET nombre = %s, tipo = %s, anada = %s, volumen_ml = %s, graduacion = %s,
                            precio = %s, cuit_bodega = %s
             WHERE cod_vino = %s RETURNING cod_vino""",
                      (vino.nombre, vino.tipo.value, vino.anada, vino.volumen_ml, vino.graduacion,
                       vino.precio, vino.cuit_bodega, cod_vino))
        if fila is None:
            raise HTTPException(404, f"No existe el vino {cod_vino}.")
        if vino.corte is not None:
            _guardar_corte(conn, cod_vino, vino.corte)
        if vino.maridajes is not None:
            _guardar_maridajes(conn, cod_vino, vino.maridajes)
        db.validar_diferidos(conn)
        return _detalle(conn, cod_vino)


@router.delete("/{cod_vino}", status_code=204, summary="Baja de un vino (409 si tiene movimientos, RN-14)")
def borrar(cod_vino: int):
    with db.transaccion() as conn:
        if db.uno(conn, "DELETE FROM vino WHERE cod_vino = %s RETURNING cod_vino", (cod_vino,)) is None:
            raise HTTPException(404, f"No existe el vino {cod_vino}.")
    return Response(status_code=204)


@router.get("/{cod_vino}/precios", response_model=list[PrecioHistorico], summary="Historial de cambios de precio (RN-13)")
def historial_precios(cod_vino: int):
    with db.transaccion() as conn:
        if db.uno(conn, "SELECT 1 FROM vino WHERE cod_vino = %s", (cod_vino,)) is None:
            raise HTTPException(404, f"No existe el vino {cod_vino}.")
        return db.todos(conn, """
            SELECT id_auditoria, precio_anterior, precio_nuevo, fecha_hora, usuario FROM auditoria_precio
             WHERE cod_vino = %s ORDER BY fecha_hora DESC, id_auditoria DESC LIMIT 100""", (cod_vino,))

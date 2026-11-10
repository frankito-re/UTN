from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from .. import db
from ..schemas import ComprobanteDetalle, ComprobanteIn, ComprobanteResumen, Pagina
from .comun import Paginacion

router = APIRouter(prefix="/comprobantes", tags=["Ventas"])

COLUMNAS = ("nro_comprobante, fecha, id_cliente, cliente, tipo_cliente, id_sala, sala, localidad_sala, "
            "subtotal, descuento, total, renglones, unidades::int")


def _detalle(conn, nro: int) -> dict:
    c = db.uno(conn, f"SELECT {COLUMNAS} FROM v_comprobante_detalle WHERE nro_comprobante = %s", (nro,))
    if c is None:
        raise HTTPException(404, f"No existe el comprobante {nro}.")
    c["detalle"] = db.todos(conn, """
        SELECT r.cod_vino, v.nombre AS vino, r.cantidad, r.precio_unitario, r.descuento_pct, r.subtotal
          FROM renglon_comprobante r JOIN vino v USING (cod_vino)
         WHERE r.nro_comprobante = %s ORDER BY v.nombre""", (nro,))
    return c


@router.get("", response_model=Pagina[ComprobanteResumen], summary="Comprobantes (paginado, con filtros)")
def listar(pag: Paginacion = Depends(),
           id_sala: int | None = None,
           id_cliente: int | None = None,
           desde: date | None = Query(None, description="Fecha minima (inclusive)"),
           hasta: date | None = Query(None, description="Fecha maxima (inclusive)")):
    cond, params = [], []
    for sql, valor in (("id_sala = %s", id_sala), ("id_cliente = %s", id_cliente),
                       ("fecha >= %s", desde), ("fecha <= %s", hasta)):
        if valor is not None:
            cond.append(sql)
            params.append(valor)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, COLUMNAS, f"FROM v_comprobante_detalle {donde}", tuple(params),
                         "fecha DESC, nro_comprobante DESC", pag.page, pag.page_size)


@router.get("/{nro_comprobante}", response_model=ComprobanteDetalle, summary="Un comprobante con sus renglones")
def obtener(nro_comprobante: int):
    with db.transaccion() as conn:
        return _detalle(conn, nro_comprobante)


@router.post("", response_model=ComprobanteDetalle, status_code=201,
             summary="Nueva venta: la base calcula precios, descuento, totales y descuenta el stock")
def crear(venta: ComprobanteIn, response: Response):
    """Transaccion unica: si CUALQUIER renglon falla (sin stock -> 409 RN-09, vino inexistente -> 422)
    no se crea nada. La API solo informa cliente, sala, vinos y cantidades."""
    with db.transaccion() as conn:
        nro = db.uno(conn, "INSERT INTO comprobante (id_cliente, id_sala) VALUES (%s, %s) RETURNING nro_comprobante",
                     (venta.id_cliente, venta.id_sala))["nro_comprobante"]
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (%s, %s, %s)",
                            [(nro, r.cod_vino, r.cantidad) for r in venta.renglones])
        resultado = _detalle(conn, nro)
    response.headers["Location"] = f"/comprobantes/{nro}"
    return resultado

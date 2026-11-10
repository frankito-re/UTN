from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from .. import db
from ..schemas import EstadoDocumento, IngresoDetalle, IngresoIn, IngresoResumen, Pagina, RenglonIn
from .comun import Paginacion

router = APIRouter(prefix="/ingresos", tags=["Ingresos al deposito"])

COLUMNAS = """i.cod_ingreso, i.fecha, i.estado, i.cod_transportista, t.razon_social AS transportista,
              i.cuit_bodega, b.razon_social AS bodega,
              COALESCE(r.renglones, 0)::int AS renglones, COALESCE(r.unidades, 0)::int AS unidades"""
DESDE = """FROM ingreso i
           JOIN transportista t ON t.cod_transportista = i.cod_transportista
           JOIN bodega b ON b.cuit = i.cuit_bodega
           LEFT JOIN (SELECT cod_ingreso, count(*) AS renglones, sum(cantidad) AS unidades
                        FROM renglon_ingreso GROUP BY cod_ingreso) r ON r.cod_ingreso = i.cod_ingreso"""


def _detalle(conn, cod: int) -> dict:
    i = db.uno(conn, f"SELECT {COLUMNAS} {DESDE} WHERE i.cod_ingreso = %s", (cod,))
    if i is None:
        raise HTTPException(404, f"No existe el ingreso {cod}.")
    i["detalle"] = db.todos(conn, """
        SELECT ri.cod_vino, v.nombre AS vino, ri.cantidad FROM renglon_ingreso ri
          JOIN vino v USING (cod_vino) WHERE ri.cod_ingreso = %s ORDER BY v.nombre""", (cod,))
    return i


@router.get("", response_model=Pagina[IngresoResumen], summary="Ingresos (paginado, con filtros)")
def listar(pag: Paginacion = Depends(), estado: EstadoDocumento | None = None,
           cod_transportista: int | None = None, desde: date | None = Query(None), hasta: date | None = Query(None)):
    cond, params = [], []
    for sql, valor in (("i.estado = %s", estado.value if estado else None),
                       ("i.cod_transportista = %s", cod_transportista),
                       ("i.fecha >= %s", desde), ("i.fecha <= %s", hasta)):
        if valor is not None:
            cond.append(sql)
            params.append(valor)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, COLUMNAS, f"{DESDE} {donde}", tuple(params),
                         "i.fecha DESC, i.cod_ingreso DESC", pag.page, pag.page_size)


@router.get("/{cod_ingreso}", response_model=IngresoDetalle, summary="Un ingreso con sus renglones")
def obtener(cod_ingreso: int):
    with db.transaccion() as conn:
        return _detalle(conn, cod_ingreso)


@router.post("", response_model=IngresoDetalle, status_code=201, summary="Nuevo ingreso (nace en confeccion, RN-10)")
def crear(ingreso: IngresoIn, response: Response):
    with db.transaccion() as conn:
        cod = db.uno(conn, "INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (%s, %s) RETURNING cod_ingreso",
                     (ingreso.cod_transportista, ingreso.cuit_bodega))["cod_ingreso"]
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO renglon_ingreso (cod_ingreso, cod_vino, cantidad) VALUES (%s, %s, %s)",
                            [(cod, r.cod_vino, r.cantidad) for r in ingreso.renglones])
        resultado = _detalle(conn, cod)
    response.headers["Location"] = f"/ingresos/{cod}"
    return resultado


@router.post("/{cod_ingreso}/renglones", response_model=IngresoDetalle, status_code=201,
             summary="Agregar un renglon (solo en confeccion, RN-12)")
def agregar_renglon(cod_ingreso: int, renglon: RenglonIn):
    with db.transaccion() as conn:
        if db.uno(conn, "SELECT 1 FROM ingreso WHERE cod_ingreso = %s", (cod_ingreso,)) is None:
            raise HTTPException(404, f"No existe el ingreso {cod_ingreso}.")
        conn.execute("INSERT INTO renglon_ingreso (cod_ingreso, cod_vino, cantidad) VALUES (%s, %s, %s)",
                     (cod_ingreso, renglon.cod_vino, renglon.cantidad))
        return _detalle(conn, cod_ingreso)


@router.delete("/{cod_ingreso}/renglones/{cod_vino}", status_code=204,
               summary="Quitar un renglon (solo en confeccion, RN-12)")
def quitar_renglon(cod_ingreso: int, cod_vino: int):
    with db.transaccion() as conn:
        if db.uno(conn, "DELETE FROM renglon_ingreso WHERE cod_ingreso = %s AND cod_vino = %s RETURNING 1",
                  (cod_ingreso, cod_vino)) is None:
            raise HTTPException(404, "El ingreso no tiene ese renglon.")
    return Response(status_code=204)


@router.post("/{cod_ingreso}/terminar", response_model=IngresoDetalle,
             summary="en_confeccion -> terminado (no puede estar vacio)")
def terminar(cod_ingreso: int):
    with db.transaccion() as conn:
        if db.uno(conn, "UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = %s RETURNING 1", (cod_ingreso,)) is None:
            raise HTTPException(404, f"No existe el ingreso {cod_ingreso}.")
        return _detalle(conn, cod_ingreso)


@router.post("/{cod_ingreso}/procesar", response_model=IngresoDetalle,
             summary="terminado -> procesado: suma al stock del deposito (CALL sp_procesar_ingreso)")
def procesar(cod_ingreso: int):
    with db.transaccion() as conn:
        conn.execute("CALL sp_procesar_ingreso(%s)", (cod_ingreso,))
        return _detalle(conn, cod_ingreso)

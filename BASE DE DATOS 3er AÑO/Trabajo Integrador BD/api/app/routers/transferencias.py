from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from .. import db
from ..schemas import EstadoDocumento, Pagina, RenglonIn, TransferenciaDetalle, TransferenciaIn, TransferenciaResumen
from .comun import Paginacion

router = APIRouter(prefix="/transferencias", tags=["Transferencias a salas"])

COLUMNAS = """t.nro_transferencia, t.id_sala, s.calle || ' ' || s.numero AS sala, t.fecha_confeccion, t.estado,
              COALESCE(r.renglones, 0)::int AS renglones, COALESCE(r.unidades, 0)::int AS unidades"""
DESDE = """FROM transferencia t
           JOIN sala_venta s ON s.id_sala = t.id_sala
           LEFT JOIN (SELECT nro_transferencia, count(*) AS renglones, sum(cantidad) AS unidades
                        FROM renglon_transferencia GROUP BY nro_transferencia) r
                  ON r.nro_transferencia = t.nro_transferencia"""


def _detalle(conn, nro: int) -> dict:
    t = db.uno(conn, f"SELECT {COLUMNAS} {DESDE} WHERE t.nro_transferencia = %s", (nro,))
    if t is None:
        raise HTTPException(404, f"No existe la transferencia {nro}.")
    t["detalle"] = db.todos(conn, """
        SELECT rt.cod_vino, v.nombre AS vino, rt.cantidad FROM renglon_transferencia rt
          JOIN vino v USING (cod_vino) WHERE rt.nro_transferencia = %s ORDER BY v.nombre""", (nro,))
    return t


@router.get("", response_model=Pagina[TransferenciaResumen], summary="Transferencias (paginado, con filtros)")
def listar(pag: Paginacion = Depends(), estado: EstadoDocumento | None = None, id_sala: int | None = None,
           desde: date | None = Query(None), hasta: date | None = Query(None)):
    cond, params = [], []
    for sql, valor in (("t.estado = %s", estado.value if estado else None), ("t.id_sala = %s", id_sala),
                       ("t.fecha_confeccion >= %s", desde), ("t.fecha_confeccion <= %s", hasta)):
        if valor is not None:
            cond.append(sql)
            params.append(valor)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, COLUMNAS, f"{DESDE} {donde}", tuple(params),
                         "t.fecha_confeccion DESC, t.nro_transferencia DESC", pag.page, pag.page_size)


@router.get("/{nro_transferencia}", response_model=TransferenciaDetalle, summary="Una transferencia con sus renglones")
def obtener(nro_transferencia: int):
    with db.transaccion() as conn:
        return _detalle(conn, nro_transferencia)


@router.post("", response_model=TransferenciaDetalle, status_code=201,
             summary="Nueva transferencia (fecha = hoy, la fija la base; nace en confeccion, RN-11)")
def crear(transferencia: TransferenciaIn, response: Response):
    with db.transaccion() as conn:
        nro = db.uno(conn, "INSERT INTO transferencia (id_sala) VALUES (%s) RETURNING nro_transferencia",
                     (transferencia.id_sala,))["nro_transferencia"]
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO renglon_transferencia (nro_transferencia, cod_vino, cantidad) VALUES (%s, %s, %s)",
                            [(nro, r.cod_vino, r.cantidad) for r in transferencia.renglones])
        resultado = _detalle(conn, nro)
    response.headers["Location"] = f"/transferencias/{nro}"
    return resultado


@router.post("/{nro_transferencia}/renglones", response_model=TransferenciaDetalle, status_code=201,
             summary="Agregar un renglon (solo en confeccion, RN-12)")
def agregar_renglon(nro_transferencia: int, renglon: RenglonIn):
    with db.transaccion() as conn:
        if db.uno(conn, "SELECT 1 FROM transferencia WHERE nro_transferencia = %s", (nro_transferencia,)) is None:
            raise HTTPException(404, f"No existe la transferencia {nro_transferencia}.")
        conn.execute("INSERT INTO renglon_transferencia (nro_transferencia, cod_vino, cantidad) VALUES (%s, %s, %s)",
                     (nro_transferencia, renglon.cod_vino, renglon.cantidad))
        return _detalle(conn, nro_transferencia)


@router.delete("/{nro_transferencia}/renglones/{cod_vino}", status_code=204,
               summary="Quitar un renglon (solo en confeccion, RN-12)")
def quitar_renglon(nro_transferencia: int, cod_vino: int):
    with db.transaccion() as conn:
        if db.uno(conn, "DELETE FROM renglon_transferencia WHERE nro_transferencia = %s AND cod_vino = %s RETURNING 1",
                  (nro_transferencia, cod_vino)) is None:
            raise HTTPException(404, "La transferencia no tiene ese renglon.")
    return Response(status_code=204)


@router.post("/{nro_transferencia}/terminar", response_model=TransferenciaDetalle,
             summary="en_confeccion -> terminado (no puede estar vacia)")
def terminar(nro_transferencia: int):
    with db.transaccion() as conn:
        if db.uno(conn, "UPDATE transferencia SET estado = 'terminado' WHERE nro_transferencia = %s RETURNING 1",
                  (nro_transferencia,)) is None:
            raise HTTPException(404, f"No existe la transferencia {nro_transferencia}.")
        return _detalle(conn, nro_transferencia)


@router.post("/{nro_transferencia}/procesar", response_model=TransferenciaDetalle,
             summary="terminado -> procesado: mueve stock deposito -> sala (CALL sp_procesar_transferencia)")
def procesar(nro_transferencia: int):
    with db.transaccion() as conn:
        conn.execute("CALL sp_procesar_transferencia(%s)", (nro_transferencia,))
        return _detalle(conn, nro_transferencia)

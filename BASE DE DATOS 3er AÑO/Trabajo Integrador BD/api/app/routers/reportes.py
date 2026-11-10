from datetime import date

from fastapi import APIRouter, Depends, Query

from .. import db
from ..schemas import Pagina, StockCritico, TopVino, VentaMensual
from .comun import Paginacion

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/ventas-mensuales", response_model=Pagina[VentaMensual],
            summary="Ventas por mes y sala (vista materializada; se actualiza con POST /reportes/refrescar)")
def ventas_mensuales(pag: Paginacion = Depends(), id_sala: int | None = None,
                     desde: date | None = Query(None, description="Primer mes (inclusive)"),
                     hasta: date | None = Query(None, description="Ultimo mes (inclusive)")):
    cond, params = [], []
    for sql, valor in (("id_sala = %s", id_sala), ("mes >= %s", desde), ("mes <= %s", hasta)):
        if valor is not None:
            cond.append(sql)
            params.append(valor)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, "mes, id_sala, comprobantes::int, unidades::int, total_vendido",
                         f"FROM mv_ventas_mensuales_sala {donde}", tuple(params), "mes DESC, id_sala",
                         pag.page, pag.page_size)


@router.post("/refrescar", summary="Refresca la vista materializada (CALL sp_refrescar_reportes)")
def refrescar():
    with db.transaccion() as conn:
        conn.execute("CALL sp_refrescar_reportes()")
    return {"estado": "ok", "mensaje": "Reportes actualizados."}


@router.get("/top-vinos", response_model=list[TopVino], summary="Vinos mas vendidos (por unidades)")
def top_vinos(limite: int = Query(10, ge=1, le=50), id_sala: int | None = None,
              desde: date | None = None, hasta: date | None = None):
    cond, params = [], []
    for sql, valor in (("c.id_sala = %s", id_sala), ("c.fecha >= %s", desde), ("c.fecha <= %s", hasta)):
        if valor is not None:
            cond.append(sql)
            params.append(valor)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.todos(conn, f"""
            SELECT v.cod_vino, v.nombre, SUM(r.cantidad)::int AS unidades, SUM(r.subtotal) AS importe
              FROM renglon_comprobante r
              JOIN comprobante c ON c.nro_comprobante = r.nro_comprobante
              JOIN vino v ON v.cod_vino = r.cod_vino
              {donde}
             GROUP BY v.cod_vino, v.nombre
             ORDER BY unidades DESC, v.cod_vino LIMIT %s""", (*params, limite))


@router.get("/stock-critico", response_model=Pagina[StockCritico], summary="Vinos con stock total por debajo de un umbral")
def stock_critico(pag: Paginacion = Depends(), umbral: int = Query(50, ge=0)):
    with db.transaccion() as conn:
        return db.pagina(conn, "cod_vino, nombre, stock_deposito::int, stock_salas::int, stock_total::int",
                         "FROM v_stock_vino WHERE stock_total < %s", (umbral,), "stock_total, cod_vino",
                         pag.page, pag.page_size)

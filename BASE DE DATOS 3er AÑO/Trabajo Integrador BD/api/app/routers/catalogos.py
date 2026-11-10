from fastapi import APIRouter, Depends, HTTPException, Query

from .. import db
from ..schemas import BodegaOut, CepaOut, MaridajeOut, Pagina, SalaOut, StockSalaItem, TransportistaOut
from .comun import Paginacion

router = APIRouter(tags=["Catalogos"])


@router.get("/cepas", response_model=list[CepaOut], summary="Cepas")
def cepas():
    with db.transaccion() as conn:
        return db.todos(conn, "SELECT id_cepa, nombre, tipo FROM cepa ORDER BY nombre")


@router.get("/bodegas", response_model=list[BodegaOut], summary="Bodegas")
def bodegas():
    with db.transaccion() as conn:
        return db.todos(conn, "SELECT cuit, razon_social, domicilio FROM bodega ORDER BY razon_social")


@router.get("/maridajes", response_model=list[MaridajeOut], summary="Maridajes")
def maridajes():
    with db.transaccion() as conn:
        return db.todos(conn, "SELECT id_maridaje, nombre, temperatura_servicio FROM maridaje ORDER BY nombre")


@router.get("/transportistas", response_model=list[TransportistaOut], summary="Transportistas")
def transportistas():
    with db.transaccion() as conn:
        return db.todos(conn, "SELECT cod_transportista, razon_social FROM transportista ORDER BY razon_social")


@router.get("/localidades", summary="Localidades (para altas de clientes)")
def localidades():
    with db.transaccion() as conn:
        return db.todos(conn, "SELECT cod_postal, nombre, provincia FROM localidad ORDER BY provincia, nombre")


@router.get("/salas", response_model=list[SalaOut], summary="Salas de venta")
def salas():
    with db.transaccion() as conn:
        return db.todos(conn, """
            SELECT s.id_sala, s.calle || ' ' || s.numero AS direccion, s.dia_cierre, l.nombre AS localidad, l.provincia
              FROM sala_venta s JOIN localidad l USING (cod_postal) ORDER BY s.id_sala""")


@router.get("/salas/{id_sala}/stock", response_model=Pagina[StockSalaItem], summary="Stock de una sala")
def stock_de_sala(id_sala: int, pag: Paginacion = Depends(),
                  solo_con_stock: bool = Query(True, description="false: incluye los vinos agotados")):
    with db.transaccion() as conn:
        if db.uno(conn, "SELECT 1 FROM sala_venta WHERE id_sala = %s", (id_sala,)) is None:
            raise HTTPException(404, f"No existe la sala {id_sala}.")
        donde = "FROM stock_sala s JOIN vino v USING (cod_vino) WHERE s.id_sala = %s" + (" AND s.cantidad > 0" if solo_con_stock else "")
        return db.pagina(conn, "s.cod_vino, v.nombre, s.cantidad", donde, (id_sala,), "v.nombre, s.cod_vino",
                         pag.page, pag.page_size)

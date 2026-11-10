from fastapi import APIRouter, Depends, HTTPException, Query, Response

from .. import db
from ..schemas import ClienteDetalle, ClienteIn, ClienteOut, Pagina, TipoCliente
from .comun import Paginacion

router = APIRouter(prefix="/clientes", tags=["Clientes"])

COLUMNAS = "id_cliente, nombre_razon_social, tipo_doc, nro_doc, direccion, cod_postal, fecha_alta, tipo_cliente, descuento"


def _detalle(conn, id_cliente: int) -> dict:
    c = db.uno(conn, """
        SELECT c.id_cliente, c.nombre_razon_social, c.tipo_doc, c.nro_doc, c.direccion, c.cod_postal,
               c.fecha_alta, c.tipo_cliente, c.descuento,
               d.zona_cobertura, d.nro_habilitacion, e.pais_destino
          FROM cliente c
          LEFT JOIN distribuidor d ON d.id_cliente = c.id_cliente
          LEFT JOIN exportador e   ON e.id_cliente = c.id_cliente
         WHERE c.id_cliente = %s""", (id_cliente,))
    if c is None:
        raise HTTPException(404, f"No existe el cliente {id_cliente}.")
    c["ultimas_compras"] = db.todos(conn, """
        SELECT nro_comprobante, fecha, total FROM comprobante
         WHERE id_cliente = %s ORDER BY fecha DESC LIMIT 10""", (id_cliente,))
    return c


@router.get("", response_model=Pagina[ClienteOut], summary="Clientes (busqueda por prefijo del nombre)")
def listar(pag: Paginacion = Depends(),
           q: str | None = Query(None, max_length=80, description="Prefijo del nombre o razon social (sin distinguir mayusculas)"),
           tipo: TipoCliente | None = None):
    cond, params = [], []
    if q:
        cond.append("lower(nombre_razon_social) LIKE %s")     # usa idx_cliente_nombre_lower (008)
        params.append(db.like_literal(q.lower()) + "%")
    if tipo:
        cond.append("tipo_cliente = %s")
        params.append(tipo.value)
    donde = ("WHERE " + " AND ".join(cond)) if cond else ""
    with db.transaccion() as conn:
        return db.pagina(conn, COLUMNAS, f"FROM cliente {donde}", tuple(params),
                         "nombre_razon_social, id_cliente", pag.page, pag.page_size)


@router.get("/{id_cliente}", response_model=ClienteDetalle, summary="Ficha de un cliente con sus ultimas compras")
def obtener(id_cliente: int):
    with db.transaccion() as conn:
        return _detalle(conn, id_cliente)


@router.post("", response_model=ClienteDetalle, status_code=201,
             summary="Alta de un cliente; el descuento lo fija la base segun el tipo (RN-06)")
def crear(cliente: ClienteIn, response: Response):
    with db.transaccion() as conn:
        id_cliente = db.uno(conn, """
            INSERT INTO cliente (nombre_razon_social, tipo_doc, nro_doc, direccion, cod_postal, tipo_cliente)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_cliente""",
                            (cliente.nombre_razon_social, cliente.tipo_doc, cliente.nro_doc, cliente.direccion,
                             cliente.cod_postal, cliente.tipo_cliente.value))["id_cliente"]
        if cliente.tipo_cliente == TipoCliente.socio:
            conn.execute("INSERT INTO socio (id_cliente) VALUES (%s)", (id_cliente,))
        elif cliente.tipo_cliente == TipoCliente.distribuidor:
            conn.execute("INSERT INTO distribuidor (id_cliente, zona_cobertura, nro_habilitacion) VALUES (%s, %s, %s)",
                         (id_cliente, cliente.zona_cobertura, cliente.nro_habilitacion))
        else:
            conn.execute("INSERT INTO exportador (id_cliente, pais_destino) VALUES (%s, %s)",
                         (id_cliente, cliente.pais_destino))
        db.validar_diferidos(conn)
        resultado = _detalle(conn, id_cliente)
    response.headers["Location"] = f"/clientes/{id_cliente}"
    return resultado

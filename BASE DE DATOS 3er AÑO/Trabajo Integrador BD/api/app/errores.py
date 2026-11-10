"""Traductor de errores de PostgreSQL (SQLSTATE) a respuestas HTTP.

La base es la autoridad de las reglas de negocio; la API solo las traduce:
  400  la peticion llego mal formada (tipo/rango/formato invalido)
  403  el rol de la API no tiene permiso
  404  no existe lo que se pidio
  409  conflicto con el estado actual (duplicado, estado invalido, sin stock, FK al borrar)
  422  la peticion es valida pero viola una regla de integridad (CHECK, corte, FK inexistente)
  503  la base no esta disponible / se cancelo la consulta
Los codigos RNxxx son los SQLSTATE propios que lanzan los triggers (005_triggers.sql).
Los detalles internos de SQL nunca se devuelven al cliente.
"""
import logging

import psycopg
from fastapi import Request
from fastapi.responses import JSONResponse

log = logging.getLogger("bodegas.api")

REGLAS = {  # SQLSTATE -> (HTTP, regla)
    "RN005": (422, "RN-05"), "RN006": (422, "RN-06"), "RN008": (409, "RN-08"), "RN009": (409, "RN-09"),
    "RN010": (409, "RN-10"), "RN011": (409, "RN-11"), "RN012": (409, "RN-12"),
}

CHECKS = {  # constraint CHECK -> mensaje para el usuario
    "ck_vino_precio_pos": "El precio debe ser mayor que cero (RN-01).",
    "ck_vino_graduacion": "La graduacion alcoholica debe estar entre 5 y 20 (RN-15).",
    "ck_vino_volumen": "La presentacion debe ser 375, 750 o 1500 ml.",
    "ck_vino_tipo": "El tipo de vino debe ser tinto, blanco, rosado o espumante.",
    "ck_vino_anada": "La anada esta fuera del rango permitido.",
    "ck_composicion_pct": "El porcentaje de una cepa debe estar entre 0 y 100 (exclusivo el 0).",
    "ck_renglon_cantidad_pos": "La cantidad debe ser mayor que cero (RN-15).",
    "ck_renglon_ingreso_cantidad": "La cantidad debe ser mayor que cero (RN-15).",
    "ck_renglon_transf_cantidad": "La cantidad debe ser mayor que cero (RN-15).",
    "ck_cliente_tipo_doc": "El tipo de documento debe ser DNI, CUIT, CUIL o PASAPORTE.",
    "ck_stock_sala_no_neg": "El stock de la sala no puede quedar negativo (RN-09).",
    "ck_stock_deposito_no_neg": "El stock del deposito no puede quedar negativo (RN-09).",
}


def _cuerpo(estado: int, sqlstate: str, mensaje: str, regla: str | None = None, restriccion: str | None = None):
    e = {"estado": estado, "sqlstate": sqlstate, "mensaje": mensaje}
    if regla:
        e["regla"] = regla
    if restriccion:
        e["restriccion"] = restriccion
    return {"error": e}


def traducir(exc: psycopg.Error) -> tuple[int, dict]:
    codigo = exc.sqlstate or ""
    d = exc.diag
    restriccion = d.constraint_name

    if codigo in REGLAS:
        estado, regla = REGLAS[codigo]
        return estado, _cuerpo(estado, codigo, d.message_primary or "Regla de negocio violada.", regla)
    if codigo == "23505":
        return 409, _cuerpo(409, codigo, "Ya existe un registro con esos datos.", restriccion=restriccion)
    if codigo == "23503":
        if "update or delete" in (d.message_primary or ""):
            return 409, _cuerpo(409, codigo, "No se puede borrar: hay registros que dependen de este (RN-14).",
                                restriccion=restriccion)
        return 422, _cuerpo(422, codigo, "Se hace referencia a un registro que no existe.", restriccion=restriccion)
    if codigo == "23514":
        return 422, _cuerpo(422, codigo, CHECKS.get(restriccion or "", "Un dato no cumple una regla de integridad."),
                            restriccion=restriccion)
    if codigo == "23502":
        return 422, _cuerpo(422, codigo, f"Falta un dato obligatorio ({d.column_name}).")
    if codigo.startswith("22"):
        return 400, _cuerpo(400, codigo, "Un dato tiene un formato o un valor fuera de rango.")
    if codigo == "P0002":
        return 404, _cuerpo(404, codigo, d.message_primary or "No existe el recurso pedido.")
    if codigo == "42501":
        return 403, _cuerpo(403, codigo, "La operacion no esta permitida para este servicio.")
    if codigo in ("40001", "40P01"):
        return 409, _cuerpo(409, codigo, "Conflicto de concurrencia: reintente la operacion.")
    if codigo == "57014" or codigo.startswith(("08", "53", "57P")) or isinstance(exc, psycopg.OperationalError):
        return 503, _cuerpo(503, codigo or "08000", "Servicio de datos no disponible; reintente en unos segundos.")
    log.error("Error de base no mapeado: sqlstate=%s mensaje=%s", codigo, exc)
    return 500, _cuerpo(500, codigo or "XX000", "Error interno.")


async def manejar_error_de_base(request: Request, exc: psycopg.Error) -> JSONResponse:
    estado, cuerpo = traducir(exc)
    return JSONResponse(status_code=estado, content=cuerpo)

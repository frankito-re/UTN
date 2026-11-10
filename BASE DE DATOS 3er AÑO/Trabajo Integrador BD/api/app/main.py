"""API REST de Bodegas del Atuel.

La API NO calcula nada: totales, descuentos, precios de venta, stock y estados los
resuelven las funciones, procedimientos y triggers de la base de datos. Aca solo
se valida la forma de las peticiones, se ejecuta SQL parametrizado y se traducen
los errores de la base a HTTP (errores.py).
"""
import logging
import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import db
from .errores import manejar_error_de_base
from .routers import catalogos, clientes, ingresos, reportes, transferencias, ventas, vinos

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    db.abrir_pool()
    yield
    db.cerrar_pool()


app = FastAPI(
    title="Bodegas del Atuel · API REST",
    version="1.0.0",
    description=("API sobre PostgreSQL con SQL parametrizado y driver nativo (sin ORM). "
                 "Las reglas de negocio viven en la base; los errores se traducen asi: "
                 "**400** peticion mal formada · **404** no existe · **409** conflicto de estado o de integridad "
                 "(sin stock, transicion invalida, borrado con dependencias) · **422** regla de integridad violada "
                 "(CHECK, corte distinto de 100, referencia inexistente) · **503** base no disponible."),
    lifespan=ciclo_de_vida,
)

app.add_middleware(CORSMiddleware, allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
                   allow_methods=["*"], allow_headers=["*"], expose_headers=["Location"])

app.add_exception_handler(psycopg.Error, manejar_error_de_base)


@app.exception_handler(RequestValidationError)
async def peticion_invalida(request: Request, exc: RequestValidationError):
    detalle = [{"campo": ".".join(str(p) for p in e["loc"] if p != "body"), "problema": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=400, content={"error": {"estado": 400, "mensaje": "Peticion invalida.", "detalle": detalle}})


@app.exception_handler(StarletteHTTPException)
async def error_http(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": {"estado": exc.status_code, "mensaje": str(exc.detail)}})


for modulo in (catalogos, vinos, clientes, ventas, ingresos, transferencias, reportes):
    app.include_router(modulo.router)


@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse("/docs")


@app.get("/health", tags=["Salud"], summary="Estado del servicio y de la conexion a la base")
def salud():
    with db.transaccion() as conn:
        conn.execute("SELECT 1")
    return {"estado": "ok", "base": "ok"}

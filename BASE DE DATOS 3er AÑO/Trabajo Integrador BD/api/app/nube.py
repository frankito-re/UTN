"""Servicio unico para plataformas tipo Render/Railway: la API bajo /api y el front en /.

Un solo contenedor y un solo origen (sin CORS, sin proxy). El TLS lo termina la plataforma; aca se
agregan las cabeceras de seguridad (HSTS, CSP estricta, etc.), equivalentes a las del nginx de docker-compose.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import db
from .main import app as api

FRONT = Path(os.environ.get("FRONT_DIR", "/srv/front"))

CSP_FRONT = ("default-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; "
             "base-uri 'self'; form-action 'self'")
# Swagger UI (/api/docs) carga su JS desde un CDN y usa un script en linea: solo esa pagina tiene una CSP mas laxa.
CSP_DOCS = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; "
            "connect-src 'self'; frame-ancestors 'none'")


@asynccontextmanager
async def ciclo_de_vida(_):
    db.abrir_pool()          # el ciclo de vida de una sub-aplicacion montada no se ejecuta: se abre aca
    yield
    db.cerrar_pool()


principal = FastAPI(lifespan=ciclo_de_vida, docs_url=None, redoc_url=None, openapi_url=None)


@principal.middleware("http")
async def cabeceras_de_seguridad(request, call_next):
    respuesta = await call_next(request)
    es_docs = request.url.path.startswith(("/api/docs", "/api/redoc"))
    respuesta.headers["Content-Security-Policy"] = CSP_DOCS if es_docs else CSP_FRONT
    respuesta.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Referrer-Policy"] = "no-referrer"
    return respuesta


principal.mount("/api", api)
principal.mount("/", StaticFiles(directory=FRONT, html=True), name="front")

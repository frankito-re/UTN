"""Piezas compartidas por los routers."""
from fastapi import Query


class Paginacion:
    """?page=1&page_size=20 (maximo 100 por pagina)."""

    def __init__(self, page: int = Query(1, ge=1, description="Numero de pagina, desde 1"),
                 page_size: int = Query(20, ge=1, le=100, description="Filas por pagina (maximo 100)")):
        self.page = page
        self.page_size = page_size

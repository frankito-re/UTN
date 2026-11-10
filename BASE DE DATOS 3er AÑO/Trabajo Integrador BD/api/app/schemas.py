"""Modelos de entrada y salida (Pydantic).

Validan solo la FORMA de lo que llega (tipos, formatos, campos desconocidos).
Las reglas de negocio (precio > 0, graduacion 5-20, cantidad > 0, corte = 100 ...)
NO se repiten aca: las decide la base de datos y la API las traduce (errores.py).
"""
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

T = TypeVar("T")


class Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid")      # un campo desconocido es un error 400


class TipoVino(str, Enum):
    tinto = "tinto"
    blanco = "blanco"
    rosado = "rosado"
    espumante = "espumante"


class EstadoDocumento(str, Enum):
    en_confeccion = "en_confeccion"
    terminado = "terminado"
    procesado = "procesado"


class TipoCliente(str, Enum):
    socio = "socio"
    distribuidor = "distribuidor"
    exportador = "exportador"


# ---------------------------------------------------------------------------- paginacion
class Pagina(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int
    pages: int


# ---------------------------------------------------------------------------- vinos
class CorteItem(Estricto):
    id_cepa: int
    porcentaje: Decimal


class VinoIn(Estricto):
    nombre: str = Field(min_length=1, max_length=80)
    tipo: TipoVino
    anada: int
    volumen_ml: int
    graduacion: Decimal
    precio: Decimal
    cuit_bodega: str = Field(pattern=r"^\d{11}$")
    corte: list[CorteItem] = Field(min_length=1, description="Cepas y porcentajes; la base exige que sumen 100 (RN-05).")
    maridajes: list[int] = []

    @field_validator("corte")
    @classmethod
    def sin_cepas_repetidas(cls, v):
        if len({c.id_cepa for c in v}) != len(v):
            raise ValueError("una cepa no puede repetirse en el corte")
        return v


class VinoUpdate(Estricto):
    """Edicion completa del vino. `corte` y `maridajes` son opcionales: si se omiten no se tocan."""
    nombre: str = Field(min_length=1, max_length=80)
    tipo: TipoVino
    anada: int
    volumen_ml: int
    graduacion: Decimal
    precio: Decimal
    cuit_bodega: str = Field(pattern=r"^\d{11}$")
    corte: list[CorteItem] | None = Field(default=None, min_length=1)
    maridajes: list[int] | None = None


class VinoOut(BaseModel):
    cod_vino: int
    nombre: str
    tipo: str
    anada: int
    volumen_ml: int
    graduacion: float
    precio: float
    bodega: str
    corte: str | None
    stock_deposito: int
    stock_salas: int
    stock_total: int


class CorteOut(BaseModel):
    id_cepa: int
    cepa: str
    porcentaje: float


class MaridajeOut(BaseModel):
    id_maridaje: int
    nombre: str
    temperatura_servicio: float


class VinoDetalle(VinoOut):
    cuit_bodega: str
    detalle_corte: list[CorteOut]
    maridajes: list[MaridajeOut]


class PrecioHistorico(BaseModel):
    id_auditoria: int
    precio_anterior: float
    precio_nuevo: float
    fecha_hora: datetime
    usuario: str


# ---------------------------------------------------------------------------- catalogos
class CepaOut(BaseModel):
    id_cepa: int
    nombre: str
    tipo: str


class BodegaOut(BaseModel):
    cuit: str
    razon_social: str
    domicilio: str


class SalaOut(BaseModel):
    id_sala: int
    direccion: str
    dia_cierre: str
    localidad: str
    provincia: str


class StockSalaItem(BaseModel):
    cod_vino: int
    nombre: str
    cantidad: int


class TransportistaOut(BaseModel):
    cod_transportista: int
    razon_social: str


# ---------------------------------------------------------------------------- clientes
class ClienteIn(Estricto):
    nombre_razon_social: str = Field(min_length=1, max_length=120)
    tipo_doc: str = Field(max_length=10)
    nro_doc: str = Field(min_length=1, max_length=20)
    direccion: str = Field(min_length=1, max_length=160)
    cod_postal: str = Field(min_length=1, max_length=8)
    tipo_cliente: TipoCliente
    # datos del subtipo (los que correspondan al tipo)
    zona_cobertura: str | None = None
    nro_habilitacion: str | None = None
    pais_destino: str | None = None


class ClienteOut(BaseModel):
    id_cliente: int
    nombre_razon_social: str
    tipo_doc: str
    nro_doc: str
    direccion: str
    cod_postal: str
    fecha_alta: date
    tipo_cliente: str
    descuento: float


class ClienteDetalle(ClienteOut):
    zona_cobertura: str | None = None
    nro_habilitacion: str | None = None
    pais_destino: str | None = None
    ultimas_compras: list[dict]


# ---------------------------------------------------------------------------- ventas
class RenglonIn(Estricto):
    cod_vino: int
    cantidad: int


class ComprobanteIn(Estricto):
    id_cliente: int
    id_sala: int
    renglones: list[RenglonIn] = Field(min_length=1)

    @field_validator("renglones")
    @classmethod
    def sin_vinos_repetidos(cls, v):
        if len({r.cod_vino for r in v}) != len(v):
            raise ValueError("un vino no puede repetirse en el comprobante: sume las cantidades")
        return v


class RenglonComprobanteOut(BaseModel):
    cod_vino: int
    vino: str
    cantidad: int
    precio_unitario: float
    descuento_pct: float
    subtotal: float


class ComprobanteResumen(BaseModel):
    nro_comprobante: int
    fecha: date
    id_cliente: int
    cliente: str
    tipo_cliente: str
    id_sala: int
    sala: str
    localidad_sala: str
    subtotal: float
    descuento: float
    total: float
    renglones: int
    unidades: int


class ComprobanteDetalle(ComprobanteResumen):
    detalle: list[RenglonComprobanteOut]


# ---------------------------------------------------------------------------- ingresos / transferencias
class RenglonDocumentoOut(BaseModel):
    cod_vino: int
    vino: str
    cantidad: int


class IngresoIn(Estricto):
    cod_transportista: int
    cuit_bodega: str = Field(pattern=r"^\d{11}$")
    renglones: list[RenglonIn] = Field(min_length=1)

    @field_validator("renglones")
    @classmethod
    def sin_vinos_repetidos(cls, v):
        if len({r.cod_vino for r in v}) != len(v):
            raise ValueError("un vino no puede repetirse: sume las cantidades")
        return v


class TransferenciaIn(Estricto):
    id_sala: int
    renglones: list[RenglonIn] = Field(min_length=1)

    @field_validator("renglones")
    @classmethod
    def sin_vinos_repetidos(cls, v):
        if len({r.cod_vino for r in v}) != len(v):
            raise ValueError("un vino no puede repetirse: sume las cantidades")
        return v


class IngresoResumen(BaseModel):
    cod_ingreso: int
    fecha: date
    estado: EstadoDocumento
    cod_transportista: int
    transportista: str
    cuit_bodega: str
    bodega: str
    renglones: int
    unidades: int


class IngresoDetalle(IngresoResumen):
    detalle: list[RenglonDocumentoOut]


class TransferenciaResumen(BaseModel):
    nro_transferencia: int
    id_sala: int
    sala: str
    fecha_confeccion: date
    estado: EstadoDocumento
    renglones: int
    unidades: int


class TransferenciaDetalle(TransferenciaResumen):
    detalle: list[RenglonDocumentoOut]


# ---------------------------------------------------------------------------- reportes
class VentaMensual(BaseModel):
    mes: date
    id_sala: int
    comprobantes: int
    unidades: int
    total_vendido: float


class TopVino(BaseModel):
    cod_vino: int
    nombre: str
    unidades: int
    importe: float


class StockCritico(BaseModel):
    cod_vino: int
    nombre: str
    stock_deposito: int
    stock_salas: int
    stock_total: int

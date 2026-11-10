"""Fixtures: una base de datos DESCARTABLE (bodegas_api_test) armada con las migraciones
reales 001..008 y datos minimos. La API corre contra ella conectandose como
bodegas_api, igual que en produccion; la base del proyecto no se toca.

Requiere el contenedor de Postgres levantado y el archivo .env con las claves.
"""
import os
import uuid
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

RAIZ = Path(__file__).resolve().parents[2]
NOMBRE_BD = "bodegas_api_test"


def _leer_env() -> dict:
    env = {}
    for linea in (RAIZ / ".env").read_text().splitlines():
        if "=" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip()
    return env


def _conectar(env, dbname, autocommit=True):
    return psycopg.connect(host="localhost", port=int(env["POSTGRES_PORT"]), user=env["POSTGRES_USER"],
                           password=env["POSTGRES_PASSWORD"], dbname=dbname, autocommit=autocommit)


@pytest.fixture(scope="session")
def admin():
    """Conexion del propietario a la base de prueba (para preparar y consultar datos)."""
    env = _leer_env()
    with _conectar(env, "postgres") as c:
        c.execute(f"DROP DATABASE IF EXISTS {NOMBRE_BD} WITH (FORCE)")
        c.execute(f"CREATE DATABASE {NOMBRE_BD}")
    con = _conectar(env, NOMBRE_BD)
    for archivo in sorted((RAIZ / "db" / "migrations").glob("*.sql")):
        con.execute(archivo.read_text())
    con.execute("""
        INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Encargado Uno'),
                                     ('5620', 'General Alvear', 'Mendoza', 'Encargado Dos');
        INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES
            ('Calle A', 100, 'lunes', '5600'), ('Calle B', 200, 'martes', '5620');
        INSERT INTO bodega VALUES ('30111111119', 'Bodega Uno', 'Domicilio 1'), ('30222222223', 'Bodega Dos', 'Domicilio 2');
        INSERT INTO cepa (nombre, tipo) VALUES ('Malbec', 'tinta'), ('Syrah', 'tinta'), ('Chardonnay', 'blanca');
        INSERT INTO transportista (razon_social, cuit, email, telefono, domicilio)
            VALUES ('Transporte Uno', '30333333339', 't1@test.com', '1', 'Ruta 1');
        INSERT INTO maridaje (nombre, temperatura_servicio) VALUES ('Carnes rojas', 17);
    """)
    yield con
    con.close()
    with _conectar(env, "postgres") as c:
        c.execute(f"DROP DATABASE IF EXISTS {NOMBRE_BD} WITH (FORCE)")


@pytest.fixture(scope="session")
def client(admin):
    from app.main import app
    env = _leer_env()
    os.environ.update({"DB_HOST": "localhost", "DB_PORT": env["POSTGRES_PORT"], "DB_NAME": NOMBRE_BD,
                       "DB_USER": "bodegas_api", "DB_PASSWORD": env["API_DB_PASSWORD"]})
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def datos(admin):
    """Ids de los datos base."""
    q = lambda sql: admin.execute(sql).fetchall()
    return {
        "sala1": q("SELECT id_sala FROM sala_venta ORDER BY id_sala")[0][0],
        "sala2": q("SELECT id_sala FROM sala_venta ORDER BY id_sala")[1][0],
        "cepas": [r[0] for r in q("SELECT id_cepa FROM cepa ORDER BY id_cepa")],
        "bodega1": "30111111119", "bodega2": "30222222223",
        "transportista": q("SELECT cod_transportista FROM transportista")[0][0],
        "maridaje": q("SELECT id_maridaje FROM maridaje")[0][0],
    }


def unico(prefijo="T") -> str:
    return f"{prefijo}-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def fabrica(client, admin, datos):
    """Crea datos de prueba por la propia API y prepara stock directamente en la base."""
    class Fabrica:
        def vino(self, **cambios):
            cuerpo = {"nombre": unico("Vino"), "tipo": "tinto", "anada": 2022, "volumen_ml": 750,
                      "graduacion": "13.5", "precio": "1000.00", "cuit_bodega": datos["bodega1"],
                      "corte": [{"id_cepa": datos["cepas"][0], "porcentaje": "60"},
                                {"id_cepa": datos["cepas"][1], "porcentaje": "40"}]}
            cuerpo.update(cambios)
            r = client.post("/vinos", json=cuerpo)
            assert r.status_code == 201, r.text
            return r.json()

        def cliente(self, tipo="socio", **cambios):
            cuerpo = {"nombre_razon_social": unico("Cliente"), "tipo_doc": "DNI", "nro_doc": unico("D"),
                      "direccion": "Calle 1", "cod_postal": "5600", "tipo_cliente": tipo}
            if tipo == "distribuidor":
                cuerpo.update(zona_cobertura="Cuyo", nro_habilitacion=unico("HAB"))
            if tipo == "exportador":
                cuerpo.update(pais_destino="Brasil")
            cuerpo.update(cambios)
            r = client.post("/clientes", json=cuerpo)
            assert r.status_code == 201, r.text
            return r.json()

        def stock_sala(self, id_sala, cod_vino, cantidad):
            admin.execute("""INSERT INTO stock_sala (id_sala, cod_vino, cantidad) VALUES (%s, %s, %s)
                             ON CONFLICT (id_sala, cod_vino) DO UPDATE SET cantidad = EXCLUDED.cantidad""",
                          (id_sala, cod_vino, cantidad))

        def stock_deposito(self, cod_vino, cantidad):
            admin.execute("""INSERT INTO stock_deposito (cod_vino, cantidad) VALUES (%s, %s)
                             ON CONFLICT (cod_vino) DO UPDATE SET cantidad = EXCLUDED.cantidad""",
                          (cod_vino, cantidad))

        def venta(self, id_cliente, id_sala, *renglones):
            return client.post("/comprobantes", json={"id_cliente": id_cliente, "id_sala": id_sala,
                                                      "renglones": [{"cod_vino": v, "cantidad": c} for v, c in renglones]})
    return Fabrica()

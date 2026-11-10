"""Inyeccion SQL y privilegios. Los intentos de inyeccion NO funcionan porque todo valor del
usuario viaja como parametro (%s) y el ORDER BY sale de una lista blanca."""
import pytest

from app import db
from app.errores import traducir
from tests.conftest import unico

PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE vino; --",
    "x'); DELETE FROM cliente; --",
    "1 UNION SELECT usename, passwd, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 FROM pg_shadow --",
    "\\'; TRUNCATE comprobante CASCADE; --",
]


def conteos(admin):
    return {t: admin.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            for t in ("vino", "cliente", "comprobante", "stock_sala", "bodega")}


@pytest.mark.parametrize("payload", PAYLOADS)
def test_la_inyeccion_en_filtros_es_texto_inerte(client, admin, fabrica, payload):
    fabrica.vino()
    fabrica.cliente()
    antes = conteos(admin)
    for ruta in ("/vinos", "/clientes"):
        r = client.get(ruta, params={"q": payload})
        assert r.status_code == 200 and r.json()["total"] == 0, (ruta, payload)
    assert client.get("/vinos", params={"cuit_bodega": payload}).status_code == 400
    assert client.get("/comprobantes", params={"desde": payload}).status_code == 400
    assert conteos(admin) == antes                                  # nada se borro ni se filtro


@pytest.mark.parametrize("payload", PAYLOADS)
def test_la_inyeccion_en_el_orden_se_rechaza(client, admin, payload):
    antes = conteos(admin)
    for parametro in ("orden", "sentido"):
        r = client.get("/vinos", params={parametro: payload})
        assert r.status_code == 400
    assert conteos(admin) == antes


@pytest.mark.parametrize("payload", PAYLOADS)
def test_la_inyeccion_en_el_cuerpo_se_guarda_como_dato(client, admin, datos, payload):
    antes = conteos(admin)
    nombre = (payload + unico())[:80]
    r = client.post("/vinos", json={"nombre": nombre, "tipo": "tinto", "anada": 2022, "volumen_ml": 750,
                                    "graduacion": "13", "precio": "100", "cuit_bodega": datos["bodega1"],
                                    "corte": [{"id_cepa": datos["cepas"][0], "porcentaje": "100"}]})
    assert r.status_code == 201
    assert client.get(f"/vinos/{r.json()['cod_vino']}").json()["nombre"] == nombre      # idéntico, sin interpretar
    despues = conteos(admin)
    assert despues["vino"] == antes["vino"] + 1 and {k: v for k, v in despues.items() if k != "vino"} == \
        {k: v for k, v in antes.items() if k != "vino"}
    r = client.post("/clientes", json={"nombre_razon_social": payload[:120], "tipo_doc": "DNI", "nro_doc": unico("D"),
                                       "direccion": payload[:160], "cod_postal": "5600", "tipo_cliente": "socio"})
    assert r.status_code == 201 and r.json()["nombre_razon_social"] == payload[:120]


def test_los_comodines_de_like_se_buscan_literalmente(client, fabrica):
    marca = unico("Lit")
    fabrica.vino(nombre=f"{marca}-100% puro")
    fabrica.vino(nombre=f"{marca}-100 otro")
    fabrica.vino(nombre=f"{marca}-A_B")
    fabrica.vino(nombre=f"{marca}-AxB")
    assert client.get("/vinos", params={"q": f"{marca}-100%"}).json()["total"] == 1     # '%' no es comodin (daria 2)
    assert client.get("/vinos", params={"q": f"{marca}-A_B"}).json()["total"] == 1      # '_' no es comodin (daria 2)
    assert client.get("/vinos", params={"q": f"{marca}-"}).json()["total"] == 4


def test_los_parametros_de_ruta_solo_aceptan_enteros(client):
    for ruta in ("/vinos/1;DROP TABLE vino", "/comprobantes/1 OR 1=1", "/clientes/x", "/ingresos/1'--"):
        assert client.get(ruta).status_code in (400, 404)


def test_la_api_corre_con_el_rol_de_privilegios_minimos(client):
    with db.transaccion() as conn:
        assert db.uno(conn, "SELECT current_user AS u, (SELECT rolsuper FROM pg_roles WHERE rolname = current_user) AS su") \
            == {"u": "bodegas_api", "su": False}


def test_traduccion_de_privilegios_insuficientes_a_403():
    import psycopg
    with db.transaccion() as conn:
        with pytest.raises(psycopg.errors.InsufficientPrivilege) as ei:
            conn.execute("UPDATE stock_sala SET cantidad = 999999")
    estado, cuerpo = traducir(ei.value)
    assert estado == 403 and cuerpo["error"]["sqlstate"] == "42501"
    assert "stock_sala" not in str(cuerpo)            # no se filtran detalles internos


@pytest.mark.parametrize("sqlstate,esperado", [("RN005", 422), ("RN006", 422), ("RN008", 409), ("RN009", 409),
                                                 ("RN010", 409), ("RN011", 409), ("RN012", 409)])
def test_tabla_de_reglas_propias(sqlstate, esperado):
    from app.errores import REGLAS
    assert REGLAS[sqlstate][0] == esperado

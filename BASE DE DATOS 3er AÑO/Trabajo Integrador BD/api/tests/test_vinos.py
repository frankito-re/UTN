import pytest

from tests.conftest import unico


def cuerpo_vino(datos, **cambios):
    base = {"nombre": unico("Vino"), "tipo": "tinto", "anada": 2022, "volumen_ml": 750, "graduacion": "13.5",
            "precio": "1000.00", "cuit_bodega": datos["bodega1"],
            "corte": [{"id_cepa": datos["cepas"][0], "porcentaje": "100"}]}
    base.update(cambios)
    return base


def test_salud_y_documentacion(client):
    assert client.get("/health").json() == {"estado": "ok", "base": "ok"}
    assert client.get("/docs").status_code == 200
    rutas = client.get("/openapi.json").json()["paths"]
    for ruta in ("/vinos", "/vinos/{cod_vino}", "/comprobantes", "/transferencias/{nro_transferencia}/procesar",
                 "/ingresos/{cod_ingreso}/procesar", "/reportes/ventas-mensuales", "/clientes"):
        assert ruta in rutas


def test_alta_de_vino_con_corte(client, datos):
    r = client.post("/vinos", json=cuerpo_vino(datos, corte=[{"id_cepa": datos["cepas"][0], "porcentaje": "60"},
                                                             {"id_cepa": datos["cepas"][1], "porcentaje": "40"}],
                                               maridajes=[datos["maridaje"]]))
    assert r.status_code == 201
    v = r.json()
    assert r.headers["Location"] == f"/vinos/{v['cod_vino']}"
    assert v["corte"] == "Malbec 60%, Syrah 40%"
    assert [c["porcentaje"] for c in v["detalle_corte"]] == [60.0, 40.0]
    assert v["maridajes"][0]["nombre"] == "Carnes rojas"
    assert v["stock_total"] == 0


def test_corte_que_no_suma_100_es_422_y_no_deja_nada(client, datos):
    nombre = unico("Corte90")
    r = client.post("/vinos", json=cuerpo_vino(datos, nombre=nombre, corte=[{"id_cepa": datos["cepas"][0], "porcentaje": "90"}]))
    assert r.status_code == 422
    assert r.json()["error"]["sqlstate"] == "RN005" and r.json()["error"]["regla"] == "RN-05"
    assert client.get("/vinos", params={"q": nombre}).json()["total"] == 0      # la transaccion se revirtio


@pytest.mark.parametrize("cambio,restriccion", [
    ({"precio": "0"}, "ck_vino_precio_pos"),
    ({"graduacion": "25"}, "ck_vino_graduacion"),
    ({"volumen_ml": 1000}, "ck_vino_volumen"),
])
def test_reglas_de_integridad_vienen_de_la_base(client, datos, cambio, restriccion):
    r = client.post("/vinos", json=cuerpo_vino(datos, **cambio))
    assert r.status_code == 422
    assert r.json()["error"]["restriccion"] == restriccion
    assert r.json()["error"]["sqlstate"] == "23514"


def test_peticiones_mal_formadas_son_400(client, datos):
    assert client.post("/vinos", json=cuerpo_vino(datos, tipo="rojo")).status_code == 400
    assert client.post("/vinos", json=cuerpo_vino(datos, cuit_bodega="123")).status_code == 400
    assert client.post("/vinos", json={**cuerpo_vino(datos), "campo_inventado": 1}).status_code == 400
    assert client.post("/vinos", json={**cuerpo_vino(datos), "corte": []}).status_code == 400
    assert client.post("/vinos", content="no es json", headers={"content-type": "application/json"}).status_code == 400
    assert client.get("/vinos/abc").status_code == 400
    assert client.get("/vinos", params={"page_size": 1000}).status_code == 400
    assert client.get("/vinos", params={"page": 0}).status_code == 400
    e = client.get("/vinos", params={"page": 0}).json()["error"]
    assert e["estado"] == 400 and e["detalle"][0]["campo"] == "query.page"


def test_duplicado_es_409_y_referencias_inexistentes_422(client, datos):
    cuerpo = cuerpo_vino(datos)
    assert client.post("/vinos", json=cuerpo).status_code == 201
    r = client.post("/vinos", json={**cuerpo, "nombre": cuerpo["nombre"]})
    assert r.status_code == 409 and r.json()["error"]["sqlstate"] == "23505"
    r = client.post("/vinos", json=cuerpo_vino(datos, cuit_bodega="30999999999"))
    assert r.status_code == 422 and r.json()["error"]["sqlstate"] == "23503"
    r = client.post("/vinos", json=cuerpo_vino(datos, corte=[{"id_cepa": 99999, "porcentaje": "100"}]))
    assert r.status_code == 422


def test_listado_paginado_filtros_y_orden(client, fabrica, datos):
    marca = unico("Lista")
    for i, precio in enumerate(["500.00", "1500.00", "900.00", "2500.00", "100.00"]):
        fabrica.vino(nombre=f"{marca}-{i}", precio=precio, tipo="blanco" if i == 3 else "tinto",
                     corte=[{"id_cepa": datos["cepas"][2 if i == 3 else 0], "porcentaje": "100"}])
    p = client.get("/vinos", params={"q": marca, "page_size": 2, "orden": "precio", "sentido": "desc"}).json()
    assert (p["total"], p["pages"], p["page"], p["page_size"]) == (5, 3, 1, 2)
    assert [v["precio"] for v in p["items"]] == [2500.0, 1500.0]
    p3 = client.get("/vinos", params={"q": marca, "page_size": 2, "page": 3, "orden": "precio", "sentido": "desc"}).json()
    assert [v["precio"] for v in p3["items"]] == [100.0]
    assert client.get("/vinos", params={"q": marca, "tipo": "blanco"}).json()["total"] == 1
    assert client.get("/vinos", params={"q": marca, "precio_min": 900, "precio_max": 1500}).json()["total"] == 2
    assert client.get("/vinos", params={"q": marca, "con_stock": "true"}).json()["total"] == 0
    assert client.get("/vinos", params={"q": marca, "orden": "inventado"}).status_code == 400
    assert client.get("/vinos", params={"q": marca, "sentido": "arriba"}).status_code == 400


def test_edicion_audita_el_cambio_de_precio(client, fabrica, datos):
    v = fabrica.vino(precio="1000.00")
    r = client.put(f"/vinos/{v['cod_vino']}", json={
        "nombre": v["nombre"], "tipo": "tinto", "anada": 2022, "volumen_ml": 750, "graduacion": "13.5",
        "precio": "1250.50", "cuit_bodega": datos["bodega1"]})
    assert r.status_code == 200 and r.json()["precio"] == 1250.5
    hist = client.get(f"/vinos/{v['cod_vino']}/precios").json()
    assert len(hist) == 1 and (hist[0]["precio_anterior"], hist[0]["precio_nuevo"]) == (1000.0, 1250.5)
    assert hist[0]["usuario"] == "bodegas_api"
    # mismo precio: no se audita
    client.put(f"/vinos/{v['cod_vino']}", json={"nombre": v["nombre"], "tipo": "tinto", "anada": 2022, "volumen_ml": 750,
                                                "graduacion": "13.5", "precio": "1250.50", "cuit_bodega": datos["bodega1"]})
    assert len(client.get(f"/vinos/{v['cod_vino']}/precios").json()) == 1
    # el corte se puede reemplazar
    r = client.put(f"/vinos/{v['cod_vino']}", json={
        "nombre": v["nombre"], "tipo": "tinto", "anada": 2022, "volumen_ml": 750, "graduacion": "13.5",
        "precio": "1250.50", "cuit_bodega": datos["bodega1"],
        "corte": [{"id_cepa": datos["cepas"][1], "porcentaje": "100"}]})
    assert r.json()["corte"] == "Syrah 100%"
    r = client.put(f"/vinos/{v['cod_vino']}", json={
        "nombre": v["nombre"], "tipo": "tinto", "anada": 2022, "volumen_ml": 750, "graduacion": "13.5",
        "precio": "1250.50", "cuit_bodega": datos["bodega1"], "corte": [{"id_cepa": datos["cepas"][1], "porcentaje": "70"}]})
    assert r.status_code == 422 and r.json()["error"]["sqlstate"] == "RN005"
    assert client.get(f"/vinos/{v['cod_vino']}").json()["corte"] == "Syrah 100%"     # sin cambios
    assert client.put("/vinos/999999", json={"nombre": "x", "tipo": "tinto", "anada": 2022, "volumen_ml": 750,
                                             "graduacion": "13", "precio": "1", "cuit_bodega": datos["bodega1"]}).status_code == 404


def test_baja_de_vino(client, fabrica, datos):
    libre = fabrica.vino()
    assert client.delete(f"/vinos/{libre['cod_vino']}").status_code == 204
    assert client.get(f"/vinos/{libre['cod_vino']}").status_code == 404
    assert client.delete(f"/vinos/{libre['cod_vino']}").status_code == 404

    usado = fabrica.vino()
    fabrica.stock_sala(datos["sala1"], usado["cod_vino"], 5)
    cli = fabrica.cliente()
    assert fabrica.venta(cli["id_cliente"], datos["sala1"], (usado["cod_vino"], 1)).status_code == 201
    r = client.delete(f"/vinos/{usado['cod_vino']}")
    assert r.status_code == 409 and r.json()["error"]["sqlstate"] == "23503"
    assert "RN-14" in r.json()["error"]["mensaje"]
    assert client.get(f"/vinos/{usado['cod_vino']}").status_code == 200

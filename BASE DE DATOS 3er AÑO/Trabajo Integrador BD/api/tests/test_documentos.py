import pytest


def stock_deposito(client, cod_vino):
    return client.get(f"/vinos/{cod_vino}").json()["stock_deposito"]


def stock_sala(client, id_sala, cod_vino):
    items = client.get(f"/salas/{id_sala}/stock", params={"page_size": 100, "solo_con_stock": "false"}).json()["items"]
    return next((i["cantidad"] for i in items if i["cod_vino"] == cod_vino), 0)


def ingreso(client, datos, *renglones):
    return client.post("/ingresos", json={"cod_transportista": datos["transportista"], "cuit_bodega": datos["bodega1"],
                                          "renglones": [{"cod_vino": v, "cantidad": c} for v, c in renglones]})


def transferencia(client, id_sala, *renglones):
    return client.post("/transferencias", json={"id_sala": id_sala,
                                                "renglones": [{"cod_vino": v, "cantidad": c} for v, c in renglones]})


def test_ciclo_completo_de_un_ingreso(client, fabrica, datos):
    v = fabrica.vino()
    r = ingreso(client, datos, (v["cod_vino"], 120))
    assert r.status_code == 201
    i = r.json()
    cod = i["cod_ingreso"]
    assert i["estado"] == "en_confeccion" and i["unidades"] == 120
    assert stock_deposito(client, v["cod_vino"]) == 0                       # en confeccion no toca el stock

    # procesar sin terminar -> 409 (RN-10)
    r = client.post(f"/ingresos/{cod}/procesar")
    assert r.status_code == 409 and r.json()["error"]["sqlstate"] == "RN010"

    assert client.post(f"/ingresos/{cod}/terminar").json()["estado"] == "terminado"
    assert client.post(f"/ingresos/{cod}/terminar").status_code == 409      # ya no esta en confeccion

    # terminado: no admite renglones (RN-12)
    otro = fabrica.vino()
    r = client.post(f"/ingresos/{cod}/renglones", json={"cod_vino": otro["cod_vino"], "cantidad": 5})
    assert r.status_code == 409 and r.json()["error"]["sqlstate"] == "RN012"
    assert client.delete(f"/ingresos/{cod}/renglones/{v['cod_vino']}").status_code == 409

    p = client.post(f"/ingresos/{cod}/procesar")
    assert p.status_code == 200 and p.json()["estado"] == "procesado"
    assert stock_deposito(client, v["cod_vino"]) == 120
    assert client.post(f"/ingresos/{cod}/procesar").status_code == 409      # no se procesa dos veces
    assert stock_deposito(client, v["cod_vino"]) == 120


def test_edicion_de_renglones_en_confeccion(client, fabrica, datos):
    a, b = fabrica.vino(), fabrica.vino()
    cod = ingreso(client, datos, (a["cod_vino"], 10)).json()["cod_ingreso"]
    r = client.post(f"/ingresos/{cod}/renglones", json={"cod_vino": b["cod_vino"], "cantidad": 5})
    assert r.status_code == 201 and r.json()["renglones"] == 2
    assert client.post(f"/ingresos/{cod}/renglones", json={"cod_vino": b["cod_vino"], "cantidad": 5}).status_code == 409  # duplicado
    assert client.post(f"/ingresos/{cod}/renglones", json={"cod_vino": b["cod_vino"] + 9999, "cantidad": 5}).status_code in (409, 422)
    assert client.delete(f"/ingresos/{cod}/renglones/{b['cod_vino']}").status_code == 204
    assert client.delete(f"/ingresos/{cod}/renglones/{b['cod_vino']}").status_code == 404
    assert client.post("/ingresos/99999999/renglones", json={"cod_vino": a["cod_vino"], "cantidad": 1}).status_code == 404


def test_ingreso_invalido(client, fabrica, datos):
    v = fabrica.vino()
    assert client.post("/ingresos", json={"cod_transportista": datos["transportista"], "cuit_bodega": datos["bodega1"],
                                          "renglones": []}).status_code == 400
    r = ingreso(client, datos, (v["cod_vino"], -5))
    assert r.status_code == 422 and r.json()["error"]["restriccion"] == "ck_renglon_ingreso_cantidad"
    assert client.post("/ingresos/99999999/procesar").status_code == 404
    assert client.post("/ingresos/99999999/terminar").status_code == 404
    assert client.get("/ingresos", params={"estado": "inventado"}).status_code == 400


def test_transferencia_mueve_stock_del_deposito_a_la_sala(client, fabrica, datos):
    v = fabrica.vino()
    fabrica.stock_deposito(v["cod_vino"], 100)
    t = transferencia(client, datos["sala2"], (v["cod_vino"], 30)).json()
    nro = t["nro_transferencia"]
    assert t["estado"] == "en_confeccion"
    from datetime import date
    assert t["fecha_confeccion"] == date.today().isoformat()                 # la fija la base (RN-11)
    client.post(f"/transferencias/{nro}/terminar")
    r = client.post(f"/transferencias/{nro}/procesar")
    assert r.status_code == 200 and r.json()["estado"] == "procesado"
    assert stock_deposito(client, v["cod_vino"]) == 70
    assert stock_sala(client, datos["sala2"], v["cod_vino"]) == 30
    assert client.post(f"/transferencias/{nro}/procesar").status_code == 409


def test_transferencia_sin_stock_suficiente_es_atomica(client, fabrica, datos):
    a, b = fabrica.vino(), fabrica.vino()
    fabrica.stock_deposito(a["cod_vino"], 50)
    fabrica.stock_deposito(b["cod_vino"], 5)
    nro = transferencia(client, datos["sala1"], (a["cod_vino"], 20), (b["cod_vino"], 6)).json()["nro_transferencia"]
    client.post(f"/transferencias/{nro}/terminar")
    r = client.post(f"/transferencias/{nro}/procesar")
    assert r.status_code == 409 and r.json()["error"]["sqlstate"] == "RN011"
    assert stock_deposito(client, a["cod_vino"]) == 50 and stock_deposito(client, b["cod_vino"]) == 5
    assert stock_sala(client, datos["sala1"], a["cod_vino"]) == 0
    assert client.get(f"/transferencias/{nro}").json()["estado"] == "terminado"
    # y el pedido no admite cambios (RN-12)
    assert client.delete(f"/transferencias/{nro}/renglones/{b['cod_vino']}").status_code == 409


def test_la_fecha_de_la_transferencia_no_se_puede_informar(client, fabrica, datos):
    v = fabrica.vino()
    r = client.post("/transferencias", json={"id_sala": datos["sala1"], "fecha_confeccion": "2000-01-01",
                                             "renglones": [{"cod_vino": v["cod_vino"], "cantidad": 1}]})
    assert r.status_code == 400
    assert client.post("/transferencias", json={"id_sala": 999999, "renglones": [{"cod_vino": v["cod_vino"], "cantidad": 1}]}).status_code == 422


def test_listados_de_documentos(client, fabrica, datos):
    v = fabrica.vino()
    for _ in range(3):
        transferencia(client, datos["sala2"], (v["cod_vino"], 1))
    p = client.get("/transferencias", params={"id_sala": datos["sala2"], "estado": "en_confeccion", "page_size": 2}).json()
    assert p["total"] >= 3 and len(p["items"]) == 2 and p["pages"] >= 2
    assert all(t["estado"] == "en_confeccion" for t in p["items"])
    assert client.get("/ingresos", params={"page_size": 5}).status_code == 200

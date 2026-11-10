def test_reportes_sobre_la_vista_materializada(client, fabrica, datos):
    v = fabrica.vino(precio="1000.00")
    fabrica.stock_sala(datos["sala2"], v["cod_vino"], 100)
    cli = fabrica.cliente()          # socio 10 %
    assert fabrica.venta(cli["id_cliente"], datos["sala2"], (v["cod_vino"], 10)).status_code == 201

    r = client.post("/reportes/refrescar")
    assert r.status_code == 200 and r.json()["estado"] == "ok"
    p = client.get("/reportes/ventas-mensuales", params={"id_sala": datos["sala2"]}).json()
    assert p["total"] >= 1
    mes = p["items"][0]
    assert mes["unidades"] >= 10 and mes["total_vendido"] >= 9000.0

    top = client.get("/reportes/top-vinos", params={"limite": 3, "id_sala": datos["sala2"]}).json()
    assert 1 <= len(top) <= 3 and top == sorted(top, key=lambda t: (-t["unidades"], t["cod_vino"]))
    assert client.get("/reportes/top-vinos", params={"limite": 0}).status_code == 400
    assert client.get("/reportes/top-vinos", params={"limite": 51}).status_code == 400


def test_stock_critico(client, fabrica, datos):
    escaso, abundante = fabrica.vino(), fabrica.vino()
    fabrica.stock_deposito(escaso["cod_vino"], 3)
    fabrica.stock_deposito(abundante["cod_vino"], 5000)
    ids = {i["cod_vino"] for i in client.get("/reportes/stock-critico", params={"umbral": 10, "page_size": 100}).json()["items"]}
    assert escaso["cod_vino"] in ids and abundante["cod_vino"] not in ids
    assert client.get("/reportes/stock-critico", params={"umbral": -1}).status_code == 400

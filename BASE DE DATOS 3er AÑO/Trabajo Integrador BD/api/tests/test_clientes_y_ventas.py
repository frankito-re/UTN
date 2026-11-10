from tests.conftest import unico


def test_el_descuento_lo_fija_la_base_segun_el_tipo(fabrica):
    assert fabrica.cliente("socio")["descuento"] == 10.0
    assert fabrica.cliente("distribuidor")["descuento"] == 20.0
    e = fabrica.cliente("exportador")
    assert e["descuento"] == 30.0 and e["pais_destino"] == "Brasil"


def test_subtipo_incompleto_es_422(client):
    r = client.post("/clientes", json={"nombre_razon_social": unico("X"), "tipo_doc": "CUIT", "nro_doc": unico("D"),
                                       "direccion": "Dir", "cod_postal": "5600", "tipo_cliente": "exportador"})
    assert r.status_code == 422 and r.json()["error"]["sqlstate"] == "23502"
    assert client.get("/clientes", params={"q": r.request.content.decode()[:0] or "zzzzzz"}).json()["total"] == 0


def test_documento_repetido_409_y_localidad_inexistente_422(client, fabrica):
    c = fabrica.cliente(nro_doc="DOC-REPETIDO-1")
    r = client.post("/clientes", json={"nombre_razon_social": "Otro", "tipo_doc": "DNI", "nro_doc": "DOC-REPETIDO-1",
                                       "direccion": "Dir", "cod_postal": "5600", "tipo_cliente": "socio"})
    assert r.status_code == 409
    r = client.post("/clientes", json={"nombre_razon_social": "Otro", "tipo_doc": "DNI", "nro_doc": unico("D"),
                                       "direccion": "Dir", "cod_postal": "0000", "tipo_cliente": "socio"})
    assert r.status_code == 422
    r = client.post("/clientes", json={"nombre_razon_social": "Otro", "tipo_doc": "LIBRETA", "nro_doc": unico("D"),
                                       "direccion": "Dir", "cod_postal": "5600", "tipo_cliente": "socio"})
    assert r.status_code == 422 and r.json()["error"]["restriccion"] == "ck_cliente_tipo_doc"
    assert c["tipo_cliente"] == "socio"


def test_busqueda_por_prefijo_sin_distinguir_mayusculas(client, fabrica):
    marca = unico("Zeta").lower()
    fabrica.cliente(nombre_razon_social=f"{marca.upper()} Uno")
    fabrica.cliente("distribuidor", nombre_razon_social=f"{marca} dos")
    assert client.get("/clientes", params={"q": marca[:8]}).json()["total"] == 2
    assert client.get("/clientes", params={"q": marca, "tipo": "distribuidor"}).json()["total"] == 1
    assert client.get("/clientes", params={"q": "uno"}).json()["total"] == 0        # solo prefijo


def test_venta_la_base_calcula_todo_y_descuenta_stock(client, fabrica, datos):
    a = fabrica.vino(precio="1000.00")
    b = fabrica.vino(precio="2000.00")
    fabrica.stock_sala(datos["sala1"], a["cod_vino"], 10)
    fabrica.stock_sala(datos["sala1"], b["cod_vino"], 10)
    exportador = fabrica.cliente("exportador")           # 30 %
    r = fabrica.venta(exportador["id_cliente"], datos["sala1"], (a["cod_vino"], 3), (b["cod_vino"], 1))
    assert r.status_code == 201, r.text
    v = r.json()
    assert r.headers["Location"] == f"/comprobantes/{v['nro_comprobante']}"
    assert (v["subtotal"], v["descuento"], v["total"]) == (5000.0, 1500.0, 3500.0)
    por_vino = {d["cod_vino"]: d for d in v["detalle"]}
    assert por_vino[a["cod_vino"]]["precio_unitario"] == 1000.0 and por_vino[a["cod_vino"]]["descuento_pct"] == 30.0
    assert por_vino[a["cod_vino"]]["subtotal"] == 2100.0
    assert v["renglones"] == 2 and v["unidades"] == 4
    stock = {s["cod_vino"]: s["cantidad"] for s in client.get(f"/salas/{datos['sala1']}/stock", params={"page_size": 100}).json()["items"]}
    assert stock[a["cod_vino"]] == 7 and stock[b["cod_vino"]] == 9
    assert client.get(f"/comprobantes/{v['nro_comprobante']}").json()["total"] == 3500.0


def test_venta_sin_stock_es_409_y_no_deja_nada_a_medias(client, fabrica, datos):
    a = fabrica.vino()
    b = fabrica.vino()
    fabrica.stock_sala(datos["sala1"], a["cod_vino"], 10)
    fabrica.stock_sala(datos["sala1"], b["cod_vino"], 1)
    cli = fabrica.cliente()
    antes = client.get("/comprobantes", params={"id_cliente": cli["id_cliente"]}).json()["total"]
    r = fabrica.venta(cli["id_cliente"], datos["sala1"], (a["cod_vino"], 4), (b["cod_vino"], 2))
    assert r.status_code == 409
    e = r.json()["error"]
    assert e["sqlstate"] == "RN009" and e["regla"] == "RN-09" and "Stock insuficiente" in e["mensaje"]
    assert client.get("/comprobantes", params={"id_cliente": cli["id_cliente"]}).json()["total"] == antes
    stock = {s["cod_vino"]: s["cantidad"] for s in client.get(f"/salas/{datos['sala1']}/stock", params={"page_size": 100}).json()["items"]}
    assert stock[a["cod_vino"]] == 10          # el primer renglon (valido) tambien se revirtio


def test_venta_con_datos_invalidos(client, fabrica, datos):
    v = fabrica.vino()
    fabrica.stock_sala(datos["sala1"], v["cod_vino"], 10)
    cli = fabrica.cliente()
    assert fabrica.venta(cli["id_cliente"], datos["sala1"], (999999, 1)).status_code == 422          # vino inexistente
    assert fabrica.venta(999999, datos["sala1"], (v["cod_vino"], 1)).status_code == 422               # cliente inexistente
    r = fabrica.venta(cli["id_cliente"], datos["sala1"], (v["cod_vino"], 0))
    assert r.status_code == 422 and r.json()["error"]["restriccion"] == "ck_renglon_cantidad_pos"
    assert client.post("/comprobantes", json={"id_cliente": cli["id_cliente"], "id_sala": datos["sala1"], "renglones": []}).status_code == 400
    r = client.post("/comprobantes", json={"id_cliente": cli["id_cliente"], "id_sala": datos["sala1"],
                                           "renglones": [{"cod_vino": v["cod_vino"], "cantidad": 1}] * 2})
    assert r.status_code == 400
    r = client.post("/comprobantes", json={"id_cliente": cli["id_cliente"], "id_sala": datos["sala1"], "total": 1,
                                           "renglones": [{"cod_vino": v["cod_vino"], "cantidad": 1}]})
    assert r.status_code == 400                      # el cliente no puede informar el total
    assert client.get("/comprobantes/999999999").status_code == 404


def test_listado_de_comprobantes_filtros(client, fabrica, datos):
    v = fabrica.vino()
    fabrica.stock_sala(datos["sala2"], v["cod_vino"], 50)
    cli = fabrica.cliente()
    for _ in range(3):
        assert fabrica.venta(cli["id_cliente"], datos["sala2"], (v["cod_vino"], 1)).status_code == 201
    p = client.get("/comprobantes", params={"id_cliente": cli["id_cliente"], "page_size": 2}).json()
    assert (p["total"], p["pages"], len(p["items"])) == (3, 2, 2)
    assert client.get("/comprobantes", params={"id_cliente": cli["id_cliente"], "id_sala": datos["sala1"]}).json()["total"] == 0
    assert client.get("/comprobantes", params={"id_cliente": cli["id_cliente"], "desde": "2999-01-01"}).json()["total"] == 0
    assert client.get("/comprobantes", params={"desde": "ayer"}).status_code == 400
    ficha = client.get(f"/clientes/{cli['id_cliente']}").json()
    assert len(ficha["ultimas_compras"]) == 3

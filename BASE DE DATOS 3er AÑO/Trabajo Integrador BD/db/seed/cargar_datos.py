#!/usr/bin/env python3
"""Carga masiva reproducible de «Bodegas del Atuel» (Etapa 3).

    .venv/bin/python db/seed/cargar_datos.py --limpiar            # escala 1.0
    .venv/bin/python db/seed/cargar_datos.py --limpiar --escala 0.02   # prueba rapida

* Reproducible: todo sale de random.Random(semilla) y Faker.seed(semilla); la
  fecha de referencia es fija (no usa "hoy"). Misma semilla y escala -> mismos datos.
* Eficiente: genera todo en memoria y carga con COPY (una transaccion).
* Coherente: el stock final de salas y depósito sale de las cantidades
  transferidas, ingresadas y vendidas, y se verifica al terminar.
* Triggers: durante la carga se desactivan SOLO los que recalculan o rechazan
  datos históricos (ventas, estados). Los diferidos (corte = 100 %, subtipos de
  cliente) quedan activos y validan lo cargado al COMMIT. Todos se reactivan
  antes del COMMIT: si el script falla, la transaccion revierte todo.
* Conexion: usa el propietario (POSTGRES_USER de .env) porque trunca y desactiva
  triggers. Las aplicaciones nunca deben usar este rol.
"""
import argparse
import bisect
import datetime as dt
import os
import random
import sys
import time
from pathlib import Path

import psycopg
from faker import Faker

RAIZ = Path(__file__).resolve().parents[2]
FECHA_REF = dt.date(2026, 11, 1)         # "hoy" de los datos; fijo por defecto (--fecha-ref hoy para usar la fecha real)
MIN_FECHA = dt.date(2019, 6, 1)          # ninguna fecha generada es anterior

COLS = {
    "localidad": "cod_postal,nombre,provincia,encargado_regional",
    "sala_venta": "id_sala,calle,numero,dia_cierre,cod_postal",
    "empleado": "cuit,nombre,fecha_ingreso,salario,id_sala",
    "finca": "id_finca,nombre,superficie_ha,departamento,provincia",
    "cepa": "id_cepa,nombre,tipo",
    "bodega": "cuit,razon_social,domicilio",
    "parcela": "id_finca,nro_parcela,superficie_ha,anio_plantacion,id_cepa",
    "lote_uva": "nro_lote,id_finca,nro_parcela,campania,fecha_cosecha,kg,cuit_bodega",
    "analisis_calidad": "id_analisis,nro_lote,fecha,brix,ph,acidez_total",
    "vino": "cod_vino,nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega",
    "composicion": "cod_vino,id_cepa,porcentaje",
    "maridaje": "id_maridaje,nombre,temperatura_servicio",
    "vino_maridaje": "cod_vino,id_maridaje",
    "cliente": "id_cliente,nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,fecha_alta,tipo_cliente,descuento",
    "socio": "id_cliente",
    "distribuidor": "id_cliente,zona_cobertura,nro_habilitacion",
    "exportador": "id_cliente,pais_destino",
    "permiso_exportacion": "cod_permiso,id_cliente,fecha_emision,fecha_vencimiento",
    "transportista": "cod_transportista,razon_social,cuit,email,telefono,domicilio",
    "cobertura_transportista": "cod_transportista,cod_postal",
    "comprobante": "nro_comprobante,fecha,id_cliente,id_sala,subtotal,descuento,total",
    "renglon_comprobante": "nro_comprobante,cod_vino,cantidad,precio_unitario,descuento_pct,subtotal",
    "ingreso": "cod_ingreso,fecha,estado,cod_transportista,cuit_bodega",
    "renglon_ingreso": "cod_ingreso,cod_vino,cantidad",
    "transferencia": "nro_transferencia,id_sala,fecha_confeccion,estado",
    "renglon_transferencia": "nro_transferencia,cod_vino,cantidad",
    "stock_sala": "id_sala,cod_vino,cantidad",
    "stock_deposito": "cod_vino,cantidad",
}
ORDEN_CARGA = list(COLS)          # ya esta en orden de dependencias (padres primero)
TODAS = ORDEN_CARGA + ["auditoria_precio"]
IDENTITY = {"sala_venta": "id_sala", "finca": "id_finca", "cepa": "id_cepa", "lote_uva": "nro_lote",
            "analisis_calidad": "id_analisis", "vino": "cod_vino", "maridaje": "id_maridaje",
            "cliente": "id_cliente", "comprobante": "nro_comprobante", "transportista": "cod_transportista",
            "ingreso": "cod_ingreso", "transferencia": "nro_transferencia"}
# Triggers que recalculan o rechazan datos historicos: se apagan solo durante la carga.
TRIGGERS_APAGADOS = {
    "comprobante": ["trg_comprobante_importes"],
    "renglon_comprobante": ["trg_renglon_calcula", "trg_renglon_valida_stock",
                            "trg_renglon_descuenta_stock", "trg_renglon_recalcula_comprobante"],
    "ingreso": ["trg_ingreso_estado"],
    "transferencia": ["trg_transferencia_estado"],
    "renglon_ingreso": ["trg_renglon_ingreso_edicion"],
    "renglon_transferencia": ["trg_renglon_transf_edicion"],
}

# --------------------------------------------------------------------------- catalogos
LOCALIDADES = [  # (nombre, provincia, codigo postal)
    ("San Rafael", "Mendoza", "5600"), ("General Alvear", "Mendoza", "5620"),
    ("Malargüe", "Mendoza", "5613"), ("Mendoza", "Mendoza", "5500"), ("Godoy Cruz", "Mendoza", "5501"),
    ("Guaymallén", "Mendoza", "5521"), ("Las Heras", "Mendoza", "5539"), ("Maipú", "Mendoza", "5515"),
    ("Luján de Cuyo", "Mendoza", "5507"), ("Tunuyán", "Mendoza", "5560"), ("Tupungato", "Mendoza", "5561"),
    ("San Martín", "Mendoza", "5570"), ("Rivadavia", "Mendoza", "5577"), ("Junín", "Mendoza", "5573"),
    ("San Carlos", "Mendoza", "5569"), ("Santa Rosa", "Mendoza", "5598"), ("La Paz", "Mendoza", "5590"),
    ("Lavalle", "Mendoza", "5533"),
    ("San Luis", "San Luis", "5700"), ("Villa Mercedes", "San Luis", "5730"), ("San Juan", "San Juan", "5400"),
    ("Córdoba", "Córdoba", "5000"), ("Río Cuarto", "Córdoba", "5800"), ("Rosario", "Santa Fe", "2000"),
    ("Santa Fe", "Santa Fe", "3000"), ("Buenos Aires", "Buenos Aires", "1000"), ("La Plata", "Buenos Aires", "1900"),
    ("Mar del Plata", "Buenos Aires", "7600"), ("Bahía Blanca", "Buenos Aires", "8000"),
    ("Neuquén", "Neuquén", "8300"), ("San Carlos de Bariloche", "Río Negro", "8400"),
    ("Salta", "Salta", "4400"), ("San Miguel de Tucumán", "Tucumán", "4000"), ("Posadas", "Misiones", "3300"),
    ("Resistencia", "Chaco", "3500"), ("Paraná", "Entre Ríos", "3100"), ("Santa Rosa", "La Pampa", "6300"),
    ("Comodoro Rivadavia", "Chubut", "9000"), ("Ushuaia", "Tierra del Fuego", "9410"),
]
N_MENDOZA = 18
CALLES = ["San Martín", "Belgrano", "Mitre", "Sarmiento", "Rivadavia", "Alem", "Lamadrid", "Godoy Cruz",
          "Las Heras", "Emilio Civit", "Yrigoyen", "Moreno", "Colón", "Urquiza", "25 de Mayo", "9 de Julio",
          "Pellegrini", "Bernardo de Irigoyen", "Corrientes", "Salta", "Libertad", "Independencia"]
DIAS = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
DEPTOS_MZA = ["San Rafael", "General Alvear", "Malargüe", "Luján de Cuyo", "Maipú", "Tupungato", "Tunuyán",
              "San Carlos", "Lavalle", "Rivadavia", "Junín", "San Martín", "Santa Rosa", "La Paz",
              "Godoy Cruz", "Guaymallén", "Las Heras"]
DEPTOS_SJ = ["Pocito", "Caucete", "Albardón", "Zonda", "Sarmiento"]
CEPAS = [("Malbec", "tinta", 30), ("Cabernet Sauvignon", "tinta", 14), ("Merlot", "tinta", 8),
         ("Syrah", "tinta", 9), ("Bonarda", "tinta", 9), ("Tempranillo", "tinta", 5), ("Pinot Noir", "tinta", 4),
         ("Chardonnay", "blanca", 9), ("Sauvignon Blanc", "blanca", 5), ("Torrontés", "blanca", 4),
         ("Chenin Blanc", "blanca", 2), ("Semillón", "blanca", 1)]
MARIDAJES = [("Carnes rojas", 17), ("Quesos duros", 16), ("Pastas salsa roja", 16), ("Carnes blancas", 12),
             ("Quesos blandos", 10), ("Pescados y mariscos", 8), ("Entradas", 10), ("Postres", 8)]
MARIDAJE_POR_TIPO = {"tinto": ["Carnes rojas", "Quesos duros", "Pastas salsa roja"],
                     "blanco": ["Carnes blancas", "Pescados y mariscos", "Quesos blandos", "Entradas"],
                     "rosado": ["Entradas", "Carnes blancas", "Pescados y mariscos"],
                     "espumante": ["Entradas", "Postres", "Quesos blandos"]}
LINEAS = ["Reserva", "Gran Reserva", "Clásico", "Terroir", "Roble", "Joven", "Premium", "Edición Limitada",
          "Tradición", "Selección", "Altos del Atuel", "Cañón del Atuel", "Single Vineyard", "Fundador"]
PREF_BODEGA = ["Bodega", "Bodegas", "Viñedos", "Finca", "Cavas de"]
ZONAS = ["Cuyo", "NOA", "NEA", "Patagonia", "Centro", "Buenos Aires y GBA", "Litoral", "Sur Mendocino",
         "Valle de Uco"]
PAISES = ["Brasil", "Estados Unidos", "China", "Reino Unido", "Alemania", "Canadá", "Paraguay", "Chile",
          "México", "Países Bajos", "Japón", "Uruguay"]
TRANSPORTES = ["Andesmar", "Expreso Cuyano", "Logística del Sur", "Transportes Atuel", "Vía Cargo", "Cruz del Sur",
               "Expreso Malargüe", "Flete Rápido", "Transportes Pehuenche", "Del Plata Logística", "Ruta 40 Cargas",
               "Cargas Alvear", "Distribuciones Cordillera", "Mendoza Express", "TransCuyo"]


# --------------------------------------------------------------------------- utilidades
def centavos(c):
    return f"{c // 100}.{c % 100:02d}"


def cuit_valido(prefijo, dni):
    base = f"{prefijo}{dni:08d}"
    s = sum(int(d) * m for d, m in zip(base, (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)))
    r = 11 - s % 11
    if r == 10:
        return None
    return base + str(0 if r == 11 else r)


def cuit_unico(rng, usados, prefijos):
    while True:
        c = cuit_valido(rng.choice(prefijos), rng.randint(10_000_000, 49_999_999))
        if c and c not in usados:
            usados.add(c)
            return c


def fecha_azar(rng, desde, hasta):
    return desde + dt.timedelta(days=rng.randint(0, (hasta - desde).days))


def acotar(f):
    return max(MIN_FECHA, min(f, FECHA_REF))


def acum(pesos):
    t, out = 0.0, []
    for p in pesos:
        t += p
        out.append(t)
    return out


def elegir(rng, cum):
    return bisect.bisect_left(cum, rng.random() * cum[-1])


# --------------------------------------------------------------------------- generacion
def generar(esc, semilla):
    rng = random.Random(semilla)
    Faker.seed(semilla)
    fake = Faker("es_AR")
    T = {t: [] for t in COLS}

    def n(base, minimo):
        return max(minimo, round(base * esc))

    # --- localidades, salas, empleados
    for nombre, prov, cp in LOCALIDADES:
        T["localidad"].append((cp, nombre, prov, f"{fake.first_name()} {fake.last_name()}"))
    cps_mza = [l[2] for l in LOCALIDADES[:N_MENDOZA]]
    cps_todos = [l[2] for l in LOCALIDADES]
    ns = n(40, 4)
    pool = cps_mza[:]
    rng.shuffle(pool)
    cps_sala = pool[:ns] + [rng.choice(cps_todos) for _ in range(max(0, ns - len(pool)))]
    vistas = set()
    for i, cp in enumerate(cps_sala, 1):
        while True:
            calle, num = rng.choice(CALLES), rng.randint(10, 3500)
            if (calle, num, cp) not in vistas:
                vistas.add((calle, num, cp))
                break
        T["sala_venta"].append((i, calle, num, DIAS[(i - 1) % 7], cp))

    cuits = set()
    for _ in range(max(ns * 3, n(400, 12))):
        sala = rng.randint(1, ns) if len(T["empleado"]) >= ns else len(T["empleado"]) + 1
        T["empleado"].append((cuit_unico(rng, cuits, ["20", "23", "24", "27"]),
                              f"{fake.first_name()} {fake.last_name()}",
                              fecha_azar(rng, dt.date(2004, 1, 1), FECHA_REF - dt.timedelta(days=32)),
                              centavos(rng.randint(650, 2200) * 1000 * 100), sala))

    # --- produccion: fincas, cepas, parcelas
    for i, (nombre, tipo, _) in enumerate(CEPAS, 1):
        T["cepa"].append((i, nombre, tipo))
    peso_cepa = acum([c[2] for c in CEPAS])
    nf = n(100, 3)
    PARC_X_FINCA = 14
    for f in range(1, nf + 1):
        sj = rng.random() < 0.08
        sup_total = 0.0
        for p in range(1, PARC_X_FINCA + 1):
            sup = round(rng.uniform(2, 15), 1)
            sup_total += sup
            T["parcela"].append((f, p, f"{sup:.2f}", rng.randint(1975, 2018), elegir(rng, peso_cepa) + 1))
        T["finca"].append((f, f"Finca {fake.last_name()} {f}", f"{sup_total * rng.uniform(1.0, 1.25):.2f}",
                           rng.choice(DEPTOS_SJ if sj else DEPTOS_MZA), "San Juan" if sj else "Mendoza"))

    # --- bodegas
    nb = n(25, 3)
    bodegas, marcas, usados_b = [], {}, set()
    while len(bodegas) < nb:
        marca = fake.last_name()
        razon = f"{rng.choice(PREF_BODEGA)} {marca}"
        if razon in usados_b:
            continue
        usados_b.add(razon)
        cuit = cuit_unico(rng, cuits, ["30", "33"])
        bodegas.append(cuit)
        marcas[cuit] = marca
        T["bodega"].append((cuit, razon, f"{fake.street_address()}, {rng.choice(DEPTOS_MZA)}, Mendoza"))

    # --- lotes de uva y analisis de calidad
    nro_lote, id_an = 0, 0
    for (f, p, sup, anio, _) in T["parcela"]:
        for camp in range(2015, 2026):
            if camp < anio + 3 or rng.random() > 0.93:
                continue
            nro_lote += 1
            fecha = dt.date(camp, 2, 10) + dt.timedelta(days=rng.randint(0, 80))
            T["lote_uva"].append((nro_lote, f, p, camp, fecha, f"{float(sup) * rng.uniform(4000, 12000):.2f}",
                                  rng.choice(bodegas)))
            for _ in range(rng.randint(1, 3)):
                id_an += 1
                T["analisis_calidad"].append((id_an, nro_lote, fecha - dt.timedelta(days=rng.randint(0, 10)),
                                              f"{rng.uniform(19, 26.5):.1f}", f"{rng.uniform(3.1, 3.9):.2f}",
                                              f"{rng.uniform(4, 8.5):.2f}"))

    # --- vinos, cortes y maridajes
    tintas = [i for i, c in enumerate(CEPAS, 1) if c[1] == "tinta"]
    blancas = [i for i, c in enumerate(CEPAS, 1) if c[1] == "blanca"]
    espum = [i for i, c in enumerate(CEPAS, 1) if c[0] in ("Chardonnay", "Pinot Noir", "Chenin Blanc", "Sauvignon Blanc")]
    peso_t = acum([CEPAS[i - 1][2] for i in tintas])
    peso_b = acum([CEPAS[i - 1][2] for i in blancas])
    patrones = [[100], [100], [60, 40], [70, 30], [85, 15], [50, 30, 20], [40, 40, 20]]
    for i, (nombre, temp) in enumerate(MARIDAJES, 1):
        T["maridaje"].append((i, nombre, f"{temp:.1f}"))
    id_mar = {m[0]: i for i, m in enumerate(MARIDAJES, 1)}
    nv = n(600, 20)
    precio_c, vistos = {}, set()
    while len(T["vino"]) < nv:
        cuit = rng.choice(bodegas)
        r = rng.random()
        base = "tinta" if rng.random() < 0.72 else "blanca"
        if base == "tinta":
            tipo = "tinto" if r < 0.86 else ("rosado" if r < 0.94 else "espumante")
        else:
            tipo = "blanco" if r < 0.9 else "espumante"
        fam = {"tinto": tintas, "rosado": tintas, "blanco": blancas, "espumante": espum}[tipo]
        peso = peso_t if tipo in ("tinto", "rosado") else (peso_b if tipo == "blanco" else None)
        pat = rng.choice(patrones)
        cepas_v = []
        while len(cepas_v) < len(pat):
            c = fam[elegir(rng, peso)] if peso else rng.choice(fam)
            if c not in cepas_v:
                cepas_v.append(c)
            if len(fam) < len(pat):
                break
        pat = pat[:len(cepas_v)]
        if sum(pat) != 100:          # no alcanzaron cepas distintas para el corte: varietal
            pat, cepas_v = [100], cepas_v[:1]
        anada = rng.randint(2018 if tipo == "espumante" else 2015, 2025)
        vol = rng.choices([750, 375, 1500], [85, 8, 7])[0]
        linea = rng.choice(LINEAS)
        nombre = f"{marcas[cuit]} {linea} {CEPAS[cepas_v[0] - 1][0] if len(cepas_v) == 1 else 'Blend'}"
        clave = (nombre, anada, vol)
        if clave in vistos:
            continue
        vistos.add(clave)
        cod = len(T["vino"]) + 1
        rango = {"tinto": (13.0, 15.0), "blanco": (11.5, 13.5), "rosado": (12.0, 13.5), "espumante": (11.0, 12.5)}[tipo]
        factor = {750: 1.0, 375: 0.6, 1500: 1.9}[vol] * (1.5 if linea in ("Reserva", "Gran Reserva", "Single Vineyard") else 1.0)
        precio = max(100, round(rng.randint(70, 450) * 100 * factor / 100) * 100)
        precio_c[cod] = precio * 100
        T["vino"].append((cod, nombre, tipo, anada, vol, f"{rng.uniform(*rango):.1f}", centavos(precio * 100), cuit))
        for c, pct in zip(cepas_v, pat):
            T["composicion"].append((cod, c, f"{pct:.2f}"))
        for m in rng.sample(MARIDAJE_POR_TIPO[tipo], rng.randint(1, min(3, len(MARIDAJE_POR_TIPO[tipo])))):
            T["vino_maridaje"].append((cod, id_mar[m]))

    # --- transportistas y cobertura
    nt = n(15, 3)
    cuit_t = {}
    for i in range(1, nt + 1):
        razon = TRANSPORTES[(i - 1) % len(TRANSPORTES)] + ("" if i <= len(TRANSPORTES) else f" {i}")
        cuit = cuit_unico(rng, cuits, ["30", "33"])
        cuit_t[i] = cuit
        slug = razon.lower().replace(" ", "").replace("ñ", "n").replace("ü", "u")
        T["transportista"].append((i, razon, cuit, f"contacto@{slug}.com.ar",
                                   f"0260-4{rng.randint(100000, 999999)}", f"{fake.street_address()}, Mendoza"))
        zonas = set(rng.sample(cps_todos, rng.randint(4, 14)))
        if i <= 3 or rng.random() < 0.4:
            zonas.add("5620")   # General Alvear
        T["cobertura_transportista"].extend((i, z) for z in sorted(zonas))

    # --- clientes
    ncli = n(20000, 30)
    nd, ne = max(3, round(ncli * 0.05)), max(3, round(ncli * 0.05))
    tipos = ["socio"] * (ncli - nd - ne) + ["distribuidor"] * nd + ["exportador"] * ne
    rng.shuffle(tipos)
    dnis = rng.sample(range(10_000_000, 60_000_000), ncli)
    cp_pesos = acum([5.0 if i < N_MENDOZA else 0.7 for i in range(len(LOCALIDADES))])
    clientes = {"socio": [], "distribuidor": [], "exportador": []}
    nhab, npe = 0, 0
    DESC = {"socio": 10, "distribuidor": 20, "exportador": 30}
    for cid, tipo in enumerate(tipos, 1):
        alta = fecha_azar(rng, dt.date(2012, 1, 1), FECHA_REF - dt.timedelta(days=17))
        if tipo == "socio":
            nombre, tdoc, ndoc = f"{fake.last_name()}, {fake.first_name()}", "DNI", str(dnis[cid - 1])
        else:
            nombre, tdoc = fake.company(), "CUIT"
            ndoc = cuit_unico(rng, cuits, ["30", "33"])
        T["cliente"].append((cid, nombre, tdoc, ndoc, fake.street_address(), LOCALIDADES[elegir(rng, cp_pesos)][2],
                             alta, tipo, f"{DESC[tipo]:.2f}"))
        clientes[tipo].append((alta, cid, DESC[tipo]))
        if tipo == "socio":
            T["socio"].append((cid,))
        elif tipo == "distribuidor":
            nhab += 1
            T["distribuidor"].append((cid, rng.choice(ZONAS), f"HAB-{nhab:05d}"))
        else:
            T["exportador"].append((cid, rng.choice(PAISES)))
            for _ in range(rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 6])):
                npe += 1
                emi = fecha_azar(rng, dt.date(2018, 1, 1), FECHA_REF - dt.timedelta(days=61))
                T["permiso_exportacion"].append((f"PE-{emi.year}-{npe:06d}", cid, emi,
                                                 emi + dt.timedelta(days=rng.randint(365, 730))))

    # --- ventas
    ncomp = n(160000, 50)
    inicio, fin = dt.date(2020, 1, 1), FECHA_REF - dt.timedelta(days=1)
    span = (fin - inicio).days
    acts = {}
    for tipo, lst in clientes.items():
        frac = 0.8 if tipo == "exportador" else 0.62
        sel = sorted(c for c in lst if rng.random() < frac) or [min(lst)]
        acts[tipo] = (sel, [c[0] for c in sel])
    cum_sala = acum([rng.uniform(0.5, 2.0) for _ in range(ns)])
    orden = list(range(1, nv + 1))
    rng.shuffle(orden)
    pesos_vino = [0.0] * nv
    for rank, v in enumerate(orden):
        pesos_vino[v - 1] = 1 / (rank + 1) ** 0.7
    cum_vino = acum(pesos_vino)
    # Cada sala trabaja un surtido: los 40 vinos mas vendidos estan en todas; el resto, segun su cobertura.
    top = set(orden[:40])
    catalogo_sala = {}
    for s_ in range(1, ns + 1):
        cob = rng.uniform(0.55, 0.95)
        catalogo_sala[s_] = top | {v for v in range(1, nv + 1) if rng.random() < cob}
    cum_tipo = acum([92, 6, 2])
    nombres_tipo = ["socio", "distribuidor", "exportador"]
    cum_nr = acum([14, 22, 24, 20, 13, 7])
    vendido, primera_venta = {}, {}
    ventas = []
    for _ in range(ncomp):
        d = inicio + dt.timedelta(days=int(span * rng.random() ** 0.85))
        tipo = nombres_tipo[elegir(rng, cum_tipo)]
        sel, altas = acts[tipo]
        k = bisect.bisect_right(altas, d)
        if k == 0:
            d, k = altas[0], 1
        cli = sel[rng.randrange(k)]
        sala = elegir(rng, cum_sala) + 1
        nr = elegir(rng, cum_nr) + 1
        vs = set()
        surtido = catalogo_sala[sala]
        while len(vs) < min(nr, len(surtido)):
            v = elegir(rng, cum_vino) + 1
            if v in surtido:
                vs.add(v)
        reng, bruto, total = [], 0, 0
        for v in sorted(vs):
            q = rng.randint(1, 12) if tipo == "socio" else (rng.randint(6, 48) if tipo == "distribuidor" else rng.randint(24, 240))
            p, pct = precio_c[v], cli[2]
            sub = (q * p * (100 - pct) + 50) // 100
            reng.append((v, q, p, pct, sub))
            bruto += q * p
            total += sub
            vendido[(sala, v)] = vendido.get((sala, v), 0) + q
            if (sala, v) not in primera_venta or d < primera_venta[(sala, v)]:
                primera_venta[(sala, v)] = d
        ventas.append((d, cli[1], sala, reng, bruto, total))
    ventas.sort(key=lambda x: x[0])
    for nro, (d, cid, sala, reng, bruto, total) in enumerate(ventas, 1):
        T["comprobante"].append((nro, d, cid, sala, centavos(bruto), centavos(bruto - total), centavos(total)))
        for (v, q, p, pct, sub) in reng:
            T["renglon_comprobante"].append((nro, v, q, centavos(p), f"{pct:.2f}", centavos(sub)))
    del ventas

    # --- stock final por (sala, vino) -> transferencias procesadas
    piezas_sala = {s: [] for s in range(1, ns + 1)}      # (fecha, vino, cantidad)
    stock_sala = {}
    pares = set(vendido)
    for s in range(1, ns + 1):
        for v in range(1, nv + 1):
            if (s, v) not in vendido and rng.random() < 0.25 * 0.7:
                pares.add((s, v))
    for (s, v) in sorted(pares):
        vend = vendido.get((s, v), 0)
        resto = 0 if rng.random() < 0.22 else rng.randint(1, 80)
        stock_sala[(s, v)] = resto
        pv = primera_venta.get((s, v))
        if vend:
            piezas_sala[s].append((acotar(pv - dt.timedelta(days=rng.randint(2, 25))), v, vend))
        if resto:
            if pv:
                f = FECHA_REF - dt.timedelta(days=rng.randint(1, 120)) if rng.random() < 0.65 else fecha_azar(rng, pv, FECHA_REF)
            else:
                f = FECHA_REF - dt.timedelta(days=rng.randint(1, 200))
            piezas_sala[s].append((acotar(f), v, resto))
    transf = []                                           # (fecha, sala, estado, {vino: cant})
    salida_vino = {}
    primer_transf = {}
    for s, piezas in piezas_sala.items():
        piezas.sort()
        i = 0
        while i < len(piezas):
            tam = rng.randint(3, 10)
            grupo = piezas[i:i + tam]
            i += tam
            reng = {}
            for (_, v, q) in grupo:
                reng[v] = reng.get(v, 0) + q
            transf.append((grupo[0][0], s, "procesado", reng))
            for v, q in reng.items():
                salida_vino[v] = salida_vino.get(v, 0) + q
                if v not in primer_transf or grupo[0][0] < primer_transf[v]:
                    primer_transf[v] = grupo[0][0]
    for _ in range(max(2, round(len(transf) * 0.03))):    # pendientes (no tocan stock)
        reng = {}
        for _ in range(rng.randint(1, 4)):
            reng[rng.randint(1, nv)] = rng.randint(1, 24)
        transf.append((FECHA_REF - dt.timedelta(days=rng.randint(0, 40)), rng.randint(1, ns),
                       rng.choice(["en_confeccion", "terminado"]), reng))
    transf.sort(key=lambda x: x[0])
    for nro, (f, s, est, reng) in enumerate(transf, 1):
        T["transferencia"].append((nro, s, f, est))
        T["renglon_transferencia"].extend((nro, v, q) for v, q in sorted(reng.items()))
    for (s, v), c in sorted(stock_sala.items()):
        T["stock_sala"].append((s, v, c))

    # --- deposito final por vino -> ingresos procesados
    piezas_bod = {b: [] for b in bodegas}
    cuit_vino = {r[0]: r[7] for r in T["vino"]}
    for v in range(1, nv + 1):
        resto = 0 if rng.random() < 0.05 else rng.randint(1, 400)
        T["stock_deposito"].append((v, resto))
        necesidad = salida_vino.get(v, 0) + resto
        if necesidad <= 0:
            continue
        partes = rng.randint(1, min(4, necesidad))
        cortes = sorted(rng.sample(range(1, necesidad), partes - 1)) if partes > 1 else []
        cants = [b - a for a, b in zip([0] + cortes, cortes + [necesidad])]
        ft = primer_transf.get(v, FECHA_REF - dt.timedelta(days=rng.randint(30, 400)))
        for j, q in enumerate(cants):
            if j == len(cants) - 1 and rng.random() < 0.5:
                f = FECHA_REF - dt.timedelta(days=rng.randint(1, 100))
            else:
                f = ft - dt.timedelta(days=rng.randint(5, 150))
            piezas_bod[cuit_vino[v]].append((acotar(f), v, q))
    ingresos = []                                         # (fecha, estado, transportista, bodega, {vino: cant})
    for b, piezas in piezas_bod.items():
        piezas.sort()
        i = 0
        while i < len(piezas):
            grupo = piezas[i:i + rng.randint(3, 8)]
            i += len(grupo)
            reng = {}
            for (_, v, q) in grupo:
                reng[v] = reng.get(v, 0) + q
            ingresos.append((grupo[0][0], "procesado", rng.randint(1, nt), b, reng))
    for _ in range(max(2, round(len(ingresos) * 0.03))):
        b = rng.choice(bodegas)
        propios = [v for v in range(1, nv + 1) if cuit_vino[v] == b] or [1]
        reng = {v: rng.randint(10, 120) for v in rng.sample(propios, min(len(propios), rng.randint(1, 4)))}
        ingresos.append((FECHA_REF - dt.timedelta(days=rng.randint(0, 40)),
                         rng.choice(["en_confeccion", "terminado"]), rng.randint(1, nt), b, reng))
    ingresos.sort(key=lambda x: x[0])
    for cod, (f, est, tr, b, reng) in enumerate(ingresos, 1):
        T["ingreso"].append((cod, f, est, tr, b))
        T["renglon_ingreso"].extend((cod, v, q) for v, q in sorted(reng.items()))
    return T


# --------------------------------------------------------------------------- base de datos
def leer_env():
    env = {}
    ruta = RAIZ / ".env"
    if ruta.exists():
        for linea in ruta.read_text().splitlines():
            if "=" in linea and not linea.lstrip().startswith("#"):
                k, v = linea.split("=", 1)
                env[k.strip()] = v.strip()
    env.update({k: v for k, v in os.environ.items() if k.startswith("POSTGRES_")})
    return env


VERIFICACIONES = [
    ("Comprobantes cuyo total no coincide con la suma de sus renglones", """
        SELECT count(*) FROM comprobante c
        LEFT JOIN (SELECT nro_comprobante, SUM(cantidad*precio_unitario) bruto, SUM(subtotal) neto
                     FROM renglon_comprobante GROUP BY 1) r USING (nro_comprobante)
        WHERE c.subtotal IS DISTINCT FROM COALESCE(r.bruto,0)
           OR c.total IS DISTINCT FROM COALESCE(r.neto,0)
           OR c.descuento IS DISTINCT FROM COALESCE(r.bruto,0) - COALESCE(r.neto,0)"""),
    ("Renglones cuyo subtotal no coincide con fn_subtotal_renglon", """
        SELECT count(*) FROM renglon_comprobante
        WHERE subtotal <> fn_subtotal_renglon(cantidad, precio_unitario, descuento_pct)"""),
    ("Comprobantes con distinto resultado que fn_calcular_comprobante (muestra de 3000)", """
        SELECT count(*) FROM (SELECT nro_comprobante FROM comprobante ORDER BY nro_comprobante LIMIT 3000) m
        JOIN comprobante c USING (nro_comprobante),
        LATERAL fn_calcular_comprobante(m.nro_comprobante) f
        WHERE (c.subtotal, c.descuento, c.total) IS DISTINCT FROM (f.subtotal_bruto, f.monto_descuento, f.total)"""),
    ("Stock de sala distinto de transferido - vendido", """
        WITH ent AS (SELECT t.id_sala, rt.cod_vino, SUM(rt.cantidad) q FROM transferencia t
                       JOIN renglon_transferencia rt USING (nro_transferencia)
                      WHERE t.estado = 'procesado' GROUP BY 1,2),
             sal AS (SELECT c.id_sala, r.cod_vino, SUM(r.cantidad) q FROM comprobante c
                       JOIN renglon_comprobante r USING (nro_comprobante) GROUP BY 1,2),
             esp AS (SELECT COALESCE(e.id_sala, s.id_sala) id_sala, COALESCE(e.cod_vino, s.cod_vino) cod_vino,
                            COALESCE(e.q,0) - COALESCE(s.q,0) q
                       FROM ent e FULL JOIN sal s ON e.id_sala = s.id_sala AND e.cod_vino = s.cod_vino)
        SELECT count(*) FROM esp FULL JOIN stock_sala ss USING (id_sala, cod_vino)
        WHERE COALESCE(esp.q,0) <> COALESCE(ss.cantidad,0)"""),
    ("Stock de deposito distinto de ingresado - transferido", """
        WITH ent AS (SELECT cod_vino, SUM(ri.cantidad) q FROM ingreso i JOIN renglon_ingreso ri USING (cod_ingreso)
                      WHERE i.estado = 'procesado' GROUP BY 1),
             sal AS (SELECT cod_vino, SUM(rt.cantidad) q FROM transferencia t JOIN renglon_transferencia rt USING (nro_transferencia)
                      WHERE t.estado = 'procesado' GROUP BY 1),
             esp AS (SELECT COALESCE(e.cod_vino, s.cod_vino) cod_vino, COALESCE(e.q,0) - COALESCE(s.q,0) q
                       FROM ent e FULL JOIN sal s ON e.cod_vino = s.cod_vino)
        SELECT count(*) FROM esp FULL JOIN stock_deposito d USING (cod_vino)
        WHERE COALESCE(esp.q,0) <> COALESCE(d.cantidad,0)"""),
    ("Vinos cuyo corte no suma 100", "SELECT count(*) FROM vino WHERE fn_suma_composicion(cod_vino) <> 100"),
    ("Clientes sin fila en su subtipo", """
        SELECT count(*) FROM cliente c WHERE NOT EXISTS (
          SELECT 1 FROM socio s WHERE c.tipo_cliente='socio' AND s.id_cliente=c.id_cliente
          UNION ALL SELECT 1 FROM distribuidor d WHERE c.tipo_cliente='distribuidor' AND d.id_cliente=c.id_cliente
          UNION ALL SELECT 1 FROM exportador e WHERE c.tipo_cliente='exportador' AND e.id_cliente=c.id_cliente)"""),
    ("Triggers que quedaron desactivados", "SELECT count(*) FROM pg_trigger WHERE NOT tgisinternal AND tgenabled = 'D'"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escala", type=float, default=1.0, help="1.0 = volumen completo (~500.000 renglones de venta)")
    ap.add_argument("--semilla", type=int, default=42)
    ap.add_argument("--fecha-ref", default="2026-11-01",
                    help="fecha 'de hoy' de los datos (AAAA-MM-DD) o 'hoy'; fija por defecto para que sea reproducible")
    ap.add_argument("--limpiar", action="store_true", help="vacia las tablas antes de cargar (obligatorio si ya hay datos)")
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--reporte", default=str(RAIZ / "docs" / "reporte_carga.md"), help="ruta del reporte ('' = no escribir)")
    a = ap.parse_args()

    global FECHA_REF
    FECHA_REF = dt.date.today() if a.fecha_ref == "hoy" else dt.date.fromisoformat(a.fecha_ref)
    env = leer_env()
    try:
        con = psycopg.connect(host=a.host, port=int(env.get("POSTGRES_PORT", 5435)), user=env["POSTGRES_USER"],
                              password=env["POSTGRES_PASSWORD"], dbname=env["POSTGRES_DB"])
    except KeyError as e:
        sys.exit(f"Falta {e} en .env")
    tiempos = []

    def marca(nombre, t0):
        tiempos.append((nombre, time.perf_counter() - t0))
        print(f"  {nombre:<44}{tiempos[-1][1]:8.2f} s", flush=True)

    t_total = time.perf_counter()
    print(f"Generando datos en memoria (escala {a.escala}, semilla {a.semilla})...")
    t0 = time.perf_counter()
    T = generar(a.escala, a.semilla)
    marca("Generacion en memoria", t0)

    cur = con.cursor()
    cur.execute("SELECT (SELECT count(*) FROM localidad) + (SELECT count(*) FROM vino) + (SELECT count(*) FROM comprobante)")
    if cur.fetchone()[0] and not a.limpiar:
        sys.exit("La base ya tiene datos. Usa --limpiar para vaciarla y recargar.")

    print("Cargando (una sola transaccion)...")
    t0 = time.perf_counter()
    cur.execute("TRUNCATE " + ", ".join(TODAS) + " RESTART IDENTITY CASCADE")
    for tabla, trgs in TRIGGERS_APAGADOS.items():
        for trg in trgs:
            cur.execute(f"ALTER TABLE {tabla} DISABLE TRIGGER {trg}")
    marca("Truncate y triggers de carga apagados", t0)
    filas = {}
    for tabla in ORDEN_CARGA:
        t0 = time.perf_counter()
        with cur.copy(f"COPY {tabla} ({COLS[tabla]}) FROM STDIN") as cp:
            for fila in T[tabla]:
                cp.write_row(fila)
        filas[tabla] = len(T[tabla])
        marca(f"COPY {tabla} ({len(T[tabla]):,} filas)", t0)
    del T
    t0 = time.perf_counter()
    for tabla, trgs in TRIGGERS_APAGADOS.items():
        for trg in trgs:
            cur.execute(f"ALTER TABLE {tabla} ENABLE TRIGGER {trg}")
    for tabla, col in IDENTITY.items():
        cur.execute(f"SELECT setval(pg_get_serial_sequence('{tabla}', '{col}'), (SELECT MAX({col}) FROM {tabla}))")
    marca("Triggers reactivados y secuencias ajustadas", t0)
    t0 = time.perf_counter()
    con.commit()          # aca corren los triggers diferidos: corte = 100 % y subtipos de cliente
    marca("COMMIT (validacion de triggers diferidos)", t0)

    con.autocommit = True
    t0 = time.perf_counter()
    cur.execute("ANALYZE")
    marca("ANALYZE", t0)

    t0 = time.perf_counter()
    for n_ronda, cond, factor in ((1, "TRUE", "1.08"), (2, "cod_vino % 2 = 0", "1.05"), (3, "cod_vino % 5 = 0", "1.10")):
        cur.execute(f"UPDATE vino SET precio = ROUND(precio * {factor}, -2) WHERE {cond}")
    marca("Ajustes de precio (generan auditoria por trigger)", t0)
    t0 = time.perf_counter()
    cur.execute("REFRESH MATERIALIZED VIEW mv_ventas_mensuales_sala")
    marca("REFRESH de la vista materializada", t0)

    print("Verificando coherencia...")
    resultados = []
    for desc, sql in VERIFICACIONES:
        t0 = time.perf_counter()
        cur.execute(sql)
        n_mal = cur.fetchone()[0]
        resultados.append((desc, n_mal))
        marca(f"{'OK ' if n_mal == 0 else 'MAL'} {desc[:40]}", t0)

    conteos = []
    for tabla in TODAS:
        cur.execute(f"SELECT count(*) FROM {tabla}")
        conteos.append((tabla, cur.fetchone()[0]))
    cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
    tamano = cur.fetchone()[0]
    total = time.perf_counter() - t_total
    print(f"\nTotal: {total:.1f} s · base: {tamano}")
    for t, c in conteos:
        print(f"  {t:<26}{c:>10,}")

    if a.reporte:
        escribir_reporte(Path(a.reporte), a, tiempos, resultados, conteos, tamano, total)
        print(f"Reporte: {a.reporte}")
    con.close()
    if any(n_mal for _, n_mal in resultados):
        sys.exit("HAY INCONSISTENCIAS: revisar las verificaciones marcadas MAL")


def escribir_reporte(ruta, a, tiempos, resultados, conteos, tamano, total):
    L = ["# Reporte de carga masiva · Bodegas del Atuel", "",
         f"Generado el {dt.date.today().isoformat()} con `db/seed/cargar_datos.py` "
         f"(escala **{a.escala}**, semilla **{a.semilla}**, fecha de referencia {FECHA_REF.isoformat()}; "
         "con `--fecha-ref hoy` las ventanas «última semana/mes» quedan relativas al día de la ejecución). "
         "Misma semilla y escala producen los mismos datos.", "",
         f"Reproducir exactamente esta carga: `.venv/bin/python db/seed/cargar_datos.py --limpiar --escala {a.escala} "
         f"--semilla {a.semilla} --fecha-ref {FECHA_REF.isoformat()}` (requiere el contenedor levantado y "
         "`pip install -r db/seed/requirements.txt` en un entorno virtual).", "",
         f"**Tiempo total:** {total:.1f} s · **Tamaño de la base:** {tamano}", "",
         "## Conteos por tabla", "", "| Tabla | Filas |", "| :-- | --: |"]
    L += [f"| `{t}` | {c:,} |" for t, c in conteos]
    L += ["", "Cumple el requisito del TP: al menos una tabla con más de 100.000 filas "
          f"(`renglon_comprobante`: {dict(conteos)['renglon_comprobante']:,}) y tres o más con más de 10.000 "
          f"({', '.join(f'`{t}`' for t, c in conteos if c > 10000)}).",
          "", "## Tiempos por fase", "", "| Fase | Segundos |", "| :-- | --: |"]
    L += [f"| {n} | {s:.2f} |" for n, s in tiempos]
    L += ["", "## Verificaciones de coherencia", "", "| Verificación | Inconsistencias |", "| :-- | --: |"]
    L += [f"| {d} | {n} |" for d, n in resultados]
    L += ["", "La auditoría de precios (`auditoria_precio`) no se carga: la generan los triggers al aplicar tres "
          "rondas de ajuste de precios después de la carga.", ""]
    ruta.write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()

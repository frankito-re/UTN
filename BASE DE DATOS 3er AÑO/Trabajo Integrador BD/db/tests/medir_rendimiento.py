#!/usr/bin/env python3
"""Mide las consultas de rendimiento con EXPLAIN (ANALYZE, BUFFERS) (Etapa 4).

    .venv/bin/python db/tests/medir_rendimiento.py antes      # guarda docs/rendimiento/antes.json
    .venv/bin/python db/tests/medir_rendimiento.py despues    # guarda docs/rendimiento/despues.json
    .venv/bin/python db/tests/medir_rendimiento.py comparar   # genera docs/rendimiento/resultados.md

Metodologia: VACUUM (ANALYZE) previo; por consulta se descarta la primera
ejecucion (cache) y se informa la MEDIANA de 7 ejecuciones. Los datos caben en
shared_buffers, por eso la comparacion es "con cache caliente"; el numero de
bloques tocados (Buffers) es independiente del cache y muestra el trabajo real.
"""
import json
import statistics
import sys
from pathlib import Path

import psycopg

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "docs" / "rendimiento"
REPETICIONES = 7

CONSULTAS = [
    ("Q1", "Ventas por sala del último trimestre (S8)", """
        SELECT s.id_sala, s.calle || ' ' || s.numero AS sala, SUM(c.total) AS total_vendido
          FROM comprobante c JOIN sala_venta s USING (id_sala)
         WHERE c.fecha >= CURRENT_DATE - 90
         GROUP BY s.id_sala, s.calle, s.numero
         ORDER BY total_vendido DESC"""),
    ("Q2", "Últimas 20 compras de un cliente (ficha de cliente)", """
        SELECT nro_comprobante, fecha, total FROM comprobante
         WHERE id_cliente = {cliente}
         ORDER BY fecha DESC LIMIT 20"""),
    ("Q3", "Unidades vendidas de un vino por mes", """
        SELECT date_trunc('month', c.fecha)::date AS mes, SUM(r.cantidad) AS unidades
          FROM renglon_comprobante r JOIN comprobante c USING (nro_comprobante)
         WHERE r.cod_vino = 50
         GROUP BY 1 ORDER BY 1"""),
    ("Q4", "Top 10 vinos más vendidos de la red (S1)", """
        SELECT v.cod_vino, v.nombre, SUM(r.cantidad) AS unidades
          FROM renglon_comprobante r JOIN vino v USING (cod_vino)
         GROUP BY v.cod_vino, v.nombre
         ORDER BY unidades DESC LIMIT 10"""),
    ("Q5", "Clientes por tipo que compraron en una sala en la última semana (S3)", """
        SELECT cl.tipo_cliente, COUNT(DISTINCT c.id_cliente) AS clientes
          FROM comprobante c JOIN cliente cl USING (id_cliente)
         WHERE c.id_sala = 7 AND c.fecha >= CURRENT_DATE - 7
         GROUP BY cl.tipo_cliente"""),
    ("Q6", "Transferencias pendientes por sala (S5)", """
        SELECT id_sala, COUNT(*) AS pendientes FROM transferencia
         WHERE estado <> 'procesado'
         GROUP BY id_sala ORDER BY pendientes"""),
    ("Q7", "Búsqueda de clientes por nombre (autocompletado)", """
        SELECT id_cliente, nombre_razon_social FROM cliente
         WHERE lower(nombre_razon_social) LIKE 'gonz%'
         ORDER BY nombre_razon_social LIMIT 50"""),
    ("Q8", "Salas con más pedidos de un vino en los últimos 15 días (S4)", """
        SELECT t.id_sala, SUM(rt.cantidad) AS unidades
          FROM transferencia t JOIN renglon_transferencia rt USING (nro_transferencia)
         WHERE rt.cod_vino = 50 AND t.fecha_confeccion >= CURRENT_DATE - 15
         GROUP BY t.id_sala ORDER BY unidades DESC LIMIT 5"""),
]
CONSULTAS.append(("Q10", "Ventas de toda la red en el último trimestre (tablero)", """
        SELECT SUM(total) AS total_vendido, COUNT(*) AS comprobantes
          FROM comprobante WHERE fecha >= CURRENT_DATE - 90"""))
# Q9 es especial: borrar un vino sin movimientos obliga a la base a verificar la FK
# (RN-14) contra cada tabla que lo referencia. Se corre dentro de una transaccion
# que se revierte.
Q9 = ("Q9", "Borrar un vino sin movimientos (verificación de FK, RN-14)")


def conectar():
    env = {}
    for linea in (RAIZ / ".env").read_text().splitlines():
        if "=" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip()
    return psycopg.connect(host="localhost", port=int(env["POSTGRES_PORT"]), user=env["POSTGRES_USER"],
                           password=env["POSTGRES_PASSWORD"], dbname=env["POSTGRES_DB"], autocommit=True)


def nodos(plan):
    yield plan
    for h in plan.get("Plans", []):
        yield from nodos(h)


def resumen(doc):
    raiz = doc[0]["Plan"]
    scans = []
    for n in nodos(raiz):
        if "Scan" in n["Node Type"]:
            scans.append(f'{n["Node Type"]}' + (f' ({n["Index Name"]})' if "Index Name" in n else "")
                         + f' en {n.get("Relation Name", "?")}')
    trig = sum(t.get("Time", 0) for t in doc[0].get("Triggers", []))
    return {"ms": doc[0]["Execution Time"], "plan_ms": doc[0]["Planning Time"], "trigger_ms": trig,
            "hit": raiz.get("Shared Hit Blocks", 0), "read": raiz.get("Shared Read Blocks", 0),
            "scans": scans}


def medir(cur, sql):
    cur.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + sql)
    cur.fetchall()                       # primera corrida: calienta el cache, se descarta
    corridas = []
    for _ in range(REPETICIONES):
        cur.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + sql)
        corridas.append(resumen(cur.fetchone()[0]))
    mediana = sorted(corridas, key=lambda c: c["ms"])[len(corridas) // 2]
    cur.execute("EXPLAIN (ANALYZE, BUFFERS) " + sql)
    texto = "\n".join(r[0] for r in cur.fetchall())
    return {**mediana, "ms": statistics.median(c["ms"] for c in corridas), "plan_texto": texto}


def medir_q9(con):
    cur = con.cursor()
    ejecuciones = []
    for i in range(REPETICIONES + 1):
        cur.execute("BEGIN")
        cur.execute("""INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
                       SELECT 'Vino de prueba Q9', 'tinto', 2024, 750, 13, 1000, cuit FROM bodega LIMIT 1
                       RETURNING cod_vino""")
        cod = cur.fetchone()[0]
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) DELETE FROM vino WHERE cod_vino = {cod}")
        doc = cur.fetchone()[0]
        cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) DELETE FROM vino WHERE cod_vino = {cod}")  # (fila ya borrada: solo para el texto)
        cur.execute("ROLLBACK")
        if i:
            r = resumen(doc)
            r["detalle_triggers"] = [f'{t["Trigger Name"]}: {t["Time"]:.3f} ms' for t in doc[0].get("Triggers", [])
                                     if "RI_ConstraintTrigger" in t["Trigger Name"] or "fkey" in t["Constraint Name"]
                                     if t.get("Time", 0) > 0.05]
            ejecuciones.append(r)
    cur.execute("BEGIN")
    cur.execute("""INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
                   SELECT 'Vino de prueba Q9', 'tinto', 2024, 750, 13, 1000, cuit FROM bodega LIMIT 1 RETURNING cod_vino""")
    cod = cur.fetchone()[0]
    cur.execute(f"EXPLAIN (ANALYZE, BUFFERS) DELETE FROM vino WHERE cod_vino = {cod}")
    texto = "\n".join(r[0] for r in cur.fetchall())
    cur.execute("ROLLBACK")
    mediana = sorted(ejecuciones, key=lambda c: c["ms"])[len(ejecuciones) // 2]
    return {**mediana, "ms": statistics.median(c["ms"] for c in ejecuciones), "plan_texto": texto}


def medir_escritura(con, ventas=2000):
    """Costo de registrar ventas (comprobante + 3 renglones, con todos los triggers) en ms por venta."""
    cur = con.cursor()
    tiempos = []
    for _ in range(5):
        cur.execute("BEGIN")
        cur.execute("UPDATE stock_sala SET cantidad = 1000000 WHERE id_sala = 1")
        cur.execute("""
            DO $$
            DECLARE vs INTEGER[]; c INTEGER; t0 TIMESTAMPTZ := clock_timestamp();
            BEGIN
                SELECT array_agg(cod_vino) INTO vs FROM (SELECT cod_vino FROM stock_sala WHERE id_sala = 1 ORDER BY cod_vino LIMIT 3) x;
                FOR i IN 1..%d LOOP
                    INSERT INTO comprobante (id_cliente, id_sala) VALUES (1 + i %% 15000, 1) RETURNING nro_comprobante INTO c;
                    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) SELECT c, unnest(vs), 1;
                END LOOP;
                PERFORM set_config('atuel.t_ms', (extract(epoch FROM clock_timestamp() - t0) * 1000)::TEXT, true);
            END $$""" % ventas)
        cur.execute("SELECT current_setting('atuel.t_ms')")
        tiempos.append(float(cur.fetchone()[0]) / ventas)
        cur.execute("ROLLBACK")
    return {"ms_por_venta": statistics.median(tiempos), "ventas": ventas}


def comparar():
    a = json.loads((SALIDA / "antes.json").read_text())
    d = json.loads((SALIDA / "despues.json").read_text())
    i_ = SALIDA / "despues_indices.json"
    s = json.loads(i_.read_text()) if i_.exists() else None
    L = ["# Resultados de rendimiento (generado)", "",
         f"Mediana de {REPETICIONES} ejecuciones con `EXPLAIN (ANALYZE, BUFFERS)`, cache caliente. "
         "«Bloques» = buffers compartidos tocados (hit + read) por la consulta. "
         "«Solo índices» = índices de 008 con la configuración por defecto del planificador; "
         "«Después» = índices + `random_page_cost = 1.1`.", ""]
    if s:
        L += ["| Consulta | Antes (ms) | Solo índices (ms) | Después (ms) | Mejora total | Bloques antes → después |",
              "| :-- | --: | --: | --: | --: | --: |"]
    else:
        L += ["| Consulta | Antes (ms) | Después (ms) | Mejora | Bloques antes → después |", "| :-- | --: | --: | --: | --: |"]
    for q in a["consultas"]:
        x, y = a["consultas"][q], d["consultas"][q]
        mejora = x["ms"] / y["ms"] if y["ms"] else float("inf")
        blo = f'{x["hit"] + x["read"]:,} → {y["hit"] + y["read"]:,}'
        if s:
            L.append(f'| **{q}** {x["titulo"]} | {x["ms"]:.2f} | {s["consultas"][q]["ms"]:.2f} | {y["ms"]:.2f} | {mejora:.1f}× | {blo} |')
        else:
            L.append(f'| **{q}** {x["titulo"]} | {x["ms"]:.2f} | {y["ms"]:.2f} | {mejora:.1f}× | {blo} |')
    L += ["", "## Costo de escritura", "",
          "| | Sin índices | Con índices de 008 | Sobrecosto |", "| :-- | --: | --: | --: |"]
    ea, ed = a["escritura"]["ms_por_venta"], d["escritura"]["ms_por_venta"]
    L.append(f"| Registrar una venta (comprobante + 3 renglones, con triggers), ms | {ea:.3f} | {ed:.3f} | {(ed / ea - 1) * 100:+.0f} % |")
    L.append(f'| Tamaño de la base | {a["tamano_bd"] / 2**20:.1f} MB | {d["tamano_bd"] / 2**20:.1f} MB | '
             f'{(d["tamano_bd"] - a["tamano_bd"]) / 2**20:+.1f} MB |')
    L += ["", "## Tamaño de los índices de 008", "", "| Índice | Tamaño |", "| :-- | --: |"]
    nuevos = {k: v for k, v in d["indices"].items() if k not in a["indices"]}
    for k, v in sorted(nuevos.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {v / 1024:,.0f} kB |")
    L.append(f'| **Total** | **{sum(nuevos.values()) / 1024:,.0f} kB** |')
    L += ["", "## Planes", ""]
    for q in a["consultas"]:
        x, y = a["consultas"][q], d["consultas"][q]
        L += [f'### {q} · {x["titulo"]}', "", "**Antes:** " + "; ".join(x["scans"]), "",
              "**Después:** " + "; ".join(y["scans"]), "",
              "<details><summary>Plan antes</summary>\n\n```\n" + x["plan_texto"] + "\n```\n</details>", "",
              "<details><summary>Plan después</summary>\n\n```\n" + y["plan_texto"] + "\n```\n</details>", ""]
    (SALIDA / "resultados.md").write_text("\n".join(L), encoding="utf-8")
    print("Escrito", SALIDA / "resultados.md")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("antes", "despues", "comparar"):
        sys.exit(__doc__)
    if sys.argv[1] == "comparar":
        return comparar()
    con = conectar()
    cur = con.cursor()
    cur.execute("VACUUM (ANALYZE)")
    cur.execute("""SELECT id_cliente FROM comprobante GROUP BY id_cliente
                   ORDER BY count(*) DESC, id_cliente OFFSET 200 LIMIT 1""")
    cliente = cur.fetchone()[0]
    out = {"etiqueta": sys.argv[1], "consultas": {}}
    for q, titulo, sql in CONSULTAS:
        r = medir(cur, sql.format(cliente=cliente))
        r["titulo"] = titulo
        out["consultas"][q] = r
        print(f'{q} {r["ms"]:9.2f} ms  bloques {r["hit"] + r["read"]:>8,}  {"; ".join(r["scans"])[:90]}', flush=True)
    r = medir_q9(con)
    r["titulo"] = Q9[1]
    out["consultas"][Q9[0]] = r
    print(f'{Q9[0]} {r["ms"]:9.2f} ms  bloques {r["hit"] + r["read"]:>8,}  triggers {r["trigger_ms"]:.2f} ms', flush=True)
    out["escritura"] = medir_escritura(con)
    print(f'Escritura: {out["escritura"]["ms_por_venta"]:.3f} ms por venta (comprobante + 3 renglones, con triggers)')
    cur.execute("""SELECT relname, pg_relation_size(oid) FROM pg_class
                   WHERE relkind = 'i' AND relnamespace = 'public'::regnamespace ORDER BY 1""")
    out["indices"] = dict(cur.fetchall())
    cur.execute("SELECT pg_database_size(current_database())")
    out["tamano_bd"] = cur.fetchone()[0]
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / f"{sys.argv[1]}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print("Guardado", SALIDA / f"{sys.argv[1]}.json")


if __name__ == "__main__":
    main()

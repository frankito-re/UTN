#!/usr/bin/env python3
"""Instala «Bodegas del Atuel» en Supabase (sirve para cualquier Postgres gestionado).

    .venv/bin/python scripts/supabase_instalar.py --cargar          # migraciones + roles + endurecimiento + datos
    .venv/bin/python scripts/supabase_instalar.py --solo-verificar  # solo los controles

Lee .env.supabase (fuera de git, permisos 600). Unica variable obligatoria:
    SUPABASE_DB_URL=postgresql://postgres.<ref>:<CLAVE>@<host-del-pooler>:5432/postgres
(Supabase -> Connect -> «Session pooler», puerto 5432; es la unica conexion con IPv4 en el plan gratuito).
Si faltan API_DB_PASSWORD / RO_DB_PASSWORD se generan al azar y se guardan en ese mismo archivo.
Escribe ademas .env.supabase.render con el DATABASE_URL completo del rol de la API (para pegar en la plataforma).
Ninguna clave se imprime.
"""
import argparse
import secrets
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

RAIZ = Path(__file__).resolve().parents[1]
MIGRACIONES = sorted((RAIZ / "db" / "migrations").glob("*.sql"))
ENDURECER = RAIZ / "deploy" / "supabase" / "endurecer.sql"


def leer_env(ruta: Path) -> dict:
    env = {}
    for linea in ruta.read_text().splitlines():
        if "=" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def agregar_env(ruta: Path, k: str, v: str) -> None:
    with ruta.open("a") as f:
        f.write(f"\n{k}={v}\n")


def paso(msg: str) -> None:
    print(f"\n== {msg}", flush=True)


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", default=str(RAIZ / ".env.supabase"))
    ap.add_argument("--cargar", action="store_true", help="carga los datos de prueba (~100 MB; el plan gratuito tiene 500 MB)")
    ap.add_argument("--escala", type=float, default=1.0, help="escala de la carga (1.0 = completa)")
    ap.add_argument("--solo-verificar", action="store_true")
    a = ap.parse_args()

    ruta_env = Path(a.env)
    if not ruta_env.exists():
        sys.exit(f"Falta {ruta_env}. Crealo con una linea:  SUPABASE_DB_URL=postgresql://postgres.<ref>:<CLAVE>@<host>:5432/postgres")
    env = leer_env(ruta_env)
    if "SUPABASE_DB_URL" not in env:
        sys.exit("Falta SUPABASE_DB_URL en el archivo de entorno.")
    for var in ("API_DB_PASSWORD", "RO_DB_PASSWORD"):
        if not env.get(var):
            env[var] = secrets.token_urlsafe(24)
            agregar_env(ruta_env, var, env[var])
            print(f"Se genero {var} y se guardo en {ruta_env.name}")
    ruta_env.chmod(0o600)

    dueno = conninfo_to_dict(env["SUPABASE_DB_URL"])
    if dueno.get("host") not in ("localhost", "127.0.0.1") and "sslmode" not in dueno:
        dueno["sslmode"] = "require"              # conexion siempre cifrada hacia el servicio gestionado
    url_dueno = make_conninfo(**dueno)

    paso("Conexion del propietario")
    con = psycopg.connect(url_dueno, autocommit=True, connect_timeout=20)
    con.add_notice_handler(lambda d: print(f"  aviso {d.message_primary}") if "omite" in (d.message_primary or "") else None)
    usuario, version = con.execute("SELECT current_user, split_part(version(), ' ', 2)").fetchone()
    super_, crea_roles = con.execute("SELECT rolsuper, rolcreaterole FROM pg_roles WHERE rolname = current_user").fetchone()
    ok(f"conectado como {usuario} a {dueno.get('host')} (PostgreSQL {version}); superusuario={super_}, crea roles={crea_roles}")
    if not (super_ or crea_roles):
        sys.exit("El usuario de la conexion no puede crear roles: use el usuario `postgres` del proyecto.")

    if not a.solo_verificar:
        instalado = con.execute("SELECT to_regclass('public.vino') IS NOT NULL").fetchone()[0]
        paso("Migraciones 001..008")
        if instalado:
            print("  Las tablas ya existen: se saltean las migraciones (para rehacer, vaciar el esquema desde el panel de Supabase).")
        else:
            for m in MIGRACIONES:
                con.execute(m.read_text())
                ok(m.name)

        paso("Claves de los roles de la aplicacion")
        for rol, var in (("bodegas_api", "API_DB_PASSWORD"), ("bodegas_ro", "RO_DB_PASSWORD")):
            con.execute(sql.SQL("ALTER ROLE {} PASSWORD {}").format(sql.Identifier(rol), sql.Literal(env[var])))
            ok(f"{rol}: clave asignada desde {var}")

        paso("Endurecimiento (la API REST automatica de Supabase no debe ver nada)")
        con.execute(ENDURECER.read_text())
        ok(ENDURECER.name)

        if a.cargar:
            paso("Carga masiva de datos (un rato, segun la conexion)")
            r = subprocess.run([sys.executable, str(RAIZ / "db" / "seed" / "cargar_datos.py"), "--limpiar", "--fecha-ref", "hoy",
                                "--escala", str(a.escala), "--url", url_dueno, "--reporte", ""])
            if r.returncode != 0:
                sys.exit("La carga fallo (ver arriba).")

    paso("Verificacion")
    n_tablas = con.execute("SELECT count(*) FROM pg_tables WHERE schemaname='public'").fetchone()[0]
    assert n_tablas == 29, f"se esperaban 29 tablas y hay {n_tablas}"
    ok(f"{n_tablas} tablas, {con.execute('SELECT count(*) FROM pg_indexes WHERE schemaname=%s', ('public',)).fetchone()[0]} indices, "
       f"{con.execute('SELECT count(*) FROM pg_trigger WHERE NOT tgisinternal').fetchone()[0]} triggers")
    for rol in ("anon", "authenticated", "service_role"):
        if con.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (rol,)).fetchone():
            sin = con.execute("SELECT NOT (has_table_privilege(%s,'public.vino','SELECT') OR has_table_privilege(%s,'public.cliente','SELECT') "
                              "OR has_table_privilege(%s,'public.vino','INSERT'))", (rol, rol, rol)).fetchone()[0]
            assert sin, f"el rol {rol} (API REST automatica de Supabase) todavia puede acceder a las tablas"
            ok(f"el rol {rol} (API REST automatica) no tiene acceso a las tablas")

    api = dict(dueno)
    api["user"] = ("bodegas_api." + dueno["user"].split(".", 1)[1]) if "." in dueno["user"] else "bodegas_api"
    api["password"] = env["API_DB_PASSWORD"]
    url_api = make_conninfo(**api)
    with psycopg.connect(url_api, connect_timeout=20) as c:
        quien, es_super = c.execute("SELECT current_user, (SELECT rolsuper FROM pg_roles WHERE rolname = current_user)").fetchone()
        ok(f"el rol de la API entra por el pooler ({api['user']} -> {quien}), superusuario={es_super}")
        try:
            c.execute("UPDATE stock_sala SET cantidad = cantidad WHERE false")
            sys.exit("FALLO: el rol de la API puede escribir stock_sala")
        except psycopg.errors.InsufficientPrivilege:
            c.rollback()
            ok("el rol de la API NO puede escribir el stock directamente (solo por procedimientos y triggers)")
        n_vinos = c.execute("SELECT count(*) FROM vino").fetchone()[0]
        ok(f"el rol de la API lee la base: {n_vinos} vinos")
        c.execute("SELECT fn_total_comprobante(0)")
        c.execute("SELECT count(*) FROM v_catalogo_vino").fetchone()
        ok("funciones y vistas accesibles para la API")

    uri = (f"postgresql://{quote(api['user'], safe='.')}:{quote(env['API_DB_PASSWORD'], safe='')}@{api['host']}:{api.get('port', '5432')}"
           f"/{api.get('dbname', 'postgres')}" + ("?sslmode=" + api["sslmode"] if "sslmode" in api else ""))
    salida = RAIZ / ".env.supabase.render"
    salida.write_text(f"DATABASE_URL={uri}\n")
    salida.chmod(0o600)
    print(f"\nListo. Para la plataforma de hosting (variable DATABASE_URL), copiar la linea de {salida.name} (no se versiona).")
    con.close()


if __name__ == "__main__":
    main()

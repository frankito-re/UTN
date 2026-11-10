-- =============================================================================
-- Endurecimiento para Supabase. Se ejecuta DESPUES de las migraciones 001..008.
--
-- Supabase expone el esquema `public` por una API REST automatica (PostgREST) a los roles `anon` y
-- `authenticated`, y les da privilegios por defecto sobre toda tabla nueva. Nuestro acceso a datos es
-- SOLO por la API propia con el rol bodegas_api, asi que se quita todo a los roles de la API automatica:
-- sin esto, cualquiera con la clave publica `anon` podria leer (o escribir) las tablas.
-- (Ademas conviene desactivar "Data API" en Project Settings; este script lo hace innecesario.)
-- Es idempotente y no falla si esos roles no existen (Postgres comun).
-- =============================================================================
DO $$
DECLARE
    r TEXT;
BEGIN
    FOREACH r IN ARRAY ARRAY['anon', 'authenticated', 'service_role'] LOOP
        IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = r) THEN
            EXECUTE format('REVOKE ALL ON ALL TABLES    IN SCHEMA public FROM %I', r);
            EXECUTE format('REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM %I', r);
            EXECUTE format('REVOKE ALL ON ALL ROUTINES  IN SCHEMA public FROM %I', r);
            EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES    FROM %I', r);
            EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON SEQUENCES FROM %I', r);
            EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON ROUTINES  FROM %I', r);
            BEGIN
                EXECUTE format('REVOKE ALL ON SCHEMA public FROM %I', r);
            EXCEPTION WHEN insufficient_privilege THEN
                RAISE NOTICE 'No se pudo quitar USAGE del esquema public a % (sin tablas accesibles igual no ve nada).', r;
            END;
        END IF;
    END LOOP;

    -- Algunos proyectos activan RLS automaticamente en tablas nuevas ("Enable automatic RLS"). Con RLS activo y sin
    -- politicas, el rol de la API no veria filas. Como ningun rol de la API automatica tiene privilegios, se desactiva.
    FOR r IN SELECT format('%I.%I', schemaname, tablename) FROM pg_tables WHERE schemaname = 'public' LOOP
        EXECUTE format('ALTER TABLE %s DISABLE ROW LEVEL SECURITY', r);
    END LOOP;
END;
$$;

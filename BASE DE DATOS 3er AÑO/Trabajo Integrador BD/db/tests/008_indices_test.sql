-- =============================================================================
-- Pruebas de 008_indices.sql: existen, son validos y cubren los tipos pedidos.
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/008_indices_test.sql
-- =============================================================================
DO $$
DECLARE
    v_n INTEGER;
    v_esperados TEXT[] := ARRAY[
        'idx_comprobante_cliente_fecha', 'idx_comprobante_sala_fecha', 'idx_renglon_transferencia_vino',
        'idx_renglon_comprobante_vino', 'brin_comprobante_fecha', 'idx_transferencia_pendientes',
        'idx_cliente_nombre_lower', 'idx_renglon_ingreso_vino', 'idx_stock_sala_vino',
        'idx_auditoria_precio_vino', 'idx_ingreso_transportista_fecha', 'idx_ingreso_bodega',
        'idx_vino_bodega', 'idx_lote_uva_bodega', 'idx_empleado_sala'];
    v_faltan TEXT;
BEGIN
    SELECT string_agg(e, ', ') INTO v_faltan
      FROM unnest(v_esperados) e
     WHERE NOT EXISTS (SELECT 1 FROM pg_class c JOIN pg_index i ON i.indexrelid = c.oid
                        WHERE c.relname = e AND c.relnamespace = 'public'::regnamespace
                          AND i.indisvalid AND i.indisready);
    ASSERT v_faltan IS NULL, 'Faltan indices validos: ' || COALESCE(v_faltan, '');

    -- Variedad pedida por el TP: compuesto, parcial, de expresion, INCLUDE y BRIN.
    SELECT count(*) INTO v_n FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
     WHERE c.relname = ANY (v_esperados) AND i.indnkeyatts > 1;
    ASSERT v_n >= 1, 'debe haber al menos un indice compuesto';
    SELECT count(*) INTO v_n FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
     WHERE c.relname = ANY (v_esperados) AND i.indpred IS NOT NULL;
    ASSERT v_n >= 1, 'debe haber al menos un indice parcial';
    SELECT count(*) INTO v_n FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
     WHERE c.relname = ANY (v_esperados) AND i.indexprs IS NOT NULL;
    ASSERT v_n >= 1, 'debe haber al menos un indice de expresion';
    SELECT count(*) INTO v_n FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
     WHERE c.relname = ANY (v_esperados) AND i.indnatts > i.indnkeyatts;
    ASSERT v_n >= 1, 'debe haber al menos un indice con INCLUDE';
    SELECT count(*) INTO v_n FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
      JOIN pg_am a ON a.oid = c.relam WHERE c.relname = ANY (v_esperados) AND a.amname = 'brin';
    ASSERT v_n >= 1, 'debe haber al menos un indice BRIN';

    -- Cada FK que ON DELETE RESTRICT obliga a verificar al borrar un vino tiene un indice
    -- cuya primera columna es cod_vino (o es la PK compuesta que ya la tiene primera).
    SELECT string_agg(c.conrelid::regclass::text, ', ') INTO v_faltan
      FROM pg_constraint c
     WHERE c.contype = 'f' AND c.confrelid = 'vino'::regclass
       AND NOT EXISTS (SELECT 1 FROM pg_index i
                        WHERE i.indrelid = c.conrelid AND i.indkey[0] = c.conkey[1]);
    ASSERT v_faltan IS NULL, 'FK hacia vino sin indice de apoyo en: ' || COALESCE(v_faltan, '');

    -- random_page_cost fijado a nivel base
    ASSERT EXISTS (SELECT 1 FROM pg_db_role_setting s JOIN pg_database d ON d.oid = s.setdatabase
                    WHERE d.datname = current_database() AND s.setrole = 0
                      AND 'random_page_cost=1.1' = ANY (s.setconfig)),
        'random_page_cost debe estar fijado en 1.1 para la base';

    RAISE NOTICE 'OK: todas las pruebas de 008_indices pasaron';
END;
$$;

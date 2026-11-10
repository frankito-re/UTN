-- =============================================================================
-- Pruebas de 007_roles.sql: privilegios minimos de bodegas_api y bodegas_ro.
-- El propietario asume cada rol con SET ROLE dentro de una transaccion que
-- termina en ROLLBACK. Las pruebas negativas verifican el SQLSTATE exacto
-- (42501 = insufficient_privilege).
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/007_roles_test.sql
-- =============================================================================
BEGIN;

CREATE FUNCTION pg_temp.expect_error(p_sql TEXT, p_sqlstate TEXT, p_desc TEXT)
RETURNS VOID LANGUAGE plpgsql AS $f$
BEGIN
    BEGIN
        EXECUTE p_sql;
    EXCEPTION WHEN OTHERS THEN
        IF SQLSTATE = p_sqlstate THEN
            RETURN;
        END IF;
        RAISE EXCEPTION 'FALLO [%]: se esperaba SQLSTATE % pero llego % (%)',
            p_desc, p_sqlstate, SQLSTATE, SQLERRM;
    END;
    RAISE EXCEPTION 'FALLO [%]: se esperaba el error % pero la sentencia se ejecuto', p_desc, p_sqlstate;
END;
$f$;

DO $$
DECLARE
    v_sala1 INTEGER; v_sala2 INTEGER; v_trans INTEGER; v_cepa INTEGER;
    vA INTEGER; v_socio INTEGER;
    c1 INTEGER; i1 INTEGER; t1 INTEGER; n INTEGER;
    v_estado estado_documento;
BEGIN
    -- ----------------------------------------------- atributos de los roles
    ASSERT NOT (SELECT rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication
                  FROM pg_roles WHERE rolname = 'bodegas_api'), 'bodegas_api no tiene atributos de administrador';
    ASSERT NOT (SELECT rolsuper OR rolcreatedb OR rolcreaterole OR rolreplication
                  FROM pg_roles WHERE rolname = 'bodegas_ro'), 'bodegas_ro no tiene atributos de administrador';

    -- ------------------------------------------- datos preparados (propietario)
    INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Enc');
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Calle A', 1, 'lunes', '5600') RETURNING id_sala INTO v_sala1;
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Calle B', 2, 'martes', '5600') RETURNING id_sala INTO v_sala2;
    INSERT INTO bodega VALUES ('30111111119', 'Bodega Test', 'Dom');
    INSERT INTO transportista (razon_social, cuit, email, telefono, domicilio)
        VALUES ('Trans', '30222222223', 't@t.com', '1', 'Ruta') RETURNING cod_transportista INTO v_trans;
    INSERT INTO cepa (nombre, tipo) VALUES ('Malbec', 'tinta') RETURNING id_cepa INTO v_cepa;
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('A','tinto',2022,750,13,1000,'30111111119') RETURNING cod_vino INTO vA;
    INSERT INTO composicion VALUES (vA, v_cepa, 100);
    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente)
        VALUES ('Socio','DNI','1','Dir','5600','socio') RETURNING id_cliente INTO v_socio;
    INSERT INTO socio VALUES (v_socio);
    INSERT INTO stock_sala VALUES (v_sala1, vA, 10);

    -- ============================================================ bodegas_api
    SET LOCAL ROLE bodegas_api;

    -- Lo que NO puede hacer
    PERFORM pg_temp.expect_error(format('INSERT INTO stock_sala VALUES (%s, %s, 99)', v_sala2, vA), '42501', 'api: no escribe stock_sala');
    PERFORM pg_temp.expect_error(format('UPDATE stock_sala SET cantidad = 999 WHERE id_sala = %s', v_sala1), '42501', 'api: no modifica stock_sala');
    PERFORM pg_temp.expect_error(format('INSERT INTO stock_deposito VALUES (%s, 99)', vA), '42501', 'api: no escribe stock_deposito');
    PERFORM pg_temp.expect_error(format('INSERT INTO auditoria_precio (cod_vino, precio_anterior, precio_nuevo) VALUES (%s, 1, 2)', vA), '42501', 'api: no escribe la auditoria');
    PERFORM pg_temp.expect_error('DELETE FROM auditoria_precio', '42501', 'api: no borra la auditoria');
    PERFORM pg_temp.expect_error('CREATE TABLE intruso (id INT)', '42501', 'api: no hace DDL');
    PERFORM pg_temp.expect_error('TRUNCATE vino CASCADE', '42501', 'api: no hace TRUNCATE');
    PERFORM pg_temp.expect_error('CREATE ROLE intruso', '42501', 'api: no crea roles');
    PERFORM pg_temp.expect_error('SELECT fn_trg_cliente_descuento()', '42501', 'api: no invoca funciones de trigger a mano');

    -- Lo que SI puede hacer: la venta descuenta stock aunque la API no lo escriba
    INSERT INTO comprobante (id_cliente, id_sala) VALUES (v_socio, v_sala1) RETURNING nro_comprobante INTO c1;
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c1, vA, 3);
    ASSERT fn_stock_sala(v_sala1, vA) = 7, 'api: la venta descuenta stock por trigger (SECURITY DEFINER)';
    PERFORM pg_temp.expect_error(format('INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (%s, %s, 99)', c1, vA),
        'RN009', 'api: sigue rigiendo RN-09');

    -- El cambio de precio se audita aunque la API no pueda escribir la auditoria
    UPDATE vino SET precio = 1100 WHERE cod_vino = vA;
    SELECT count(*) INTO n FROM auditoria_precio WHERE cod_vino = vA;
    ASSERT n = 1, 'api: el cambio de precio queda auditado';
    ASSERT (SELECT usuario FROM auditoria_precio WHERE cod_vino = vA) = session_user::TEXT, 'la auditoria registra al usuario de la sesion';

    -- Ingreso y transferencia de punta a punta con los procedimientos
    INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (v_trans, '30111111119') RETURNING cod_ingreso INTO i1;
    INSERT INTO renglon_ingreso VALUES (i1, vA, 50);
    UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = i1;
    PERFORM pg_temp.expect_error(format($q$UPDATE ingreso SET estado = 'procesado' WHERE cod_ingreso = %s$q$, i1),
        'RN010', 'api: no puede saltear el procedimiento');
    CALL sp_procesar_ingreso(i1);
    ASSERT fn_stock_deposito(vA) = 50, 'api: sp_procesar_ingreso suma al deposito aunque la API no lo escriba';

    INSERT INTO transferencia (id_sala) VALUES (v_sala2) RETURNING nro_transferencia INTO t1;
    INSERT INTO renglon_transferencia VALUES (t1, vA, 20);
    UPDATE transferencia SET estado = 'terminado' WHERE nro_transferencia = t1;
    CALL sp_procesar_transferencia(t1);
    ASSERT fn_stock_deposito(vA) = 30 AND fn_stock_sala(v_sala2, vA) = 20, 'api: sp_procesar_transferencia mueve el stock';

    -- Vistas, funciones y refresco de la materializada
    ASSERT (SELECT stock_total FROM v_catalogo_vino WHERE cod_vino = vA) = 7 + 20 + 30, 'api: lee el catalogo';
    CALL sp_refrescar_reportes();
    ASSERT (SELECT count(*) FROM mv_ventas_mensuales_sala) = 1, 'api: refresca la materializada con el procedimiento';
    PERFORM pg_temp.expect_error('REFRESH MATERIALIZED VIEW mv_ventas_mensuales_sala', '42501', 'api: no refresca directamente');
    ASSERT fn_total_comprobante(c1) = 2700, 'api: ejecuta funciones de calculo';

    RESET ROLE;

    -- ============================================================= bodegas_ro
    SET LOCAL ROLE bodegas_ro;

    ASSERT (SELECT count(*) FROM cliente) = 1, 'ro: lee tablas';
    ASSERT (SELECT count(*) FROM v_catalogo_vino) = 1, 'ro: lee vistas';
    ASSERT (SELECT count(*) FROM mv_ventas_mensuales_sala) = 1, 'ro: lee la materializada';
    ASSERT fn_stock_sala(v_sala1, vA) = 7, 'ro: ejecuta funciones de consulta';

    PERFORM pg_temp.expect_error(format('UPDATE vino SET precio = 1 WHERE cod_vino = %s', vA), '42501', 'ro: no modifica');
    PERFORM pg_temp.expect_error('DELETE FROM cliente', '42501', 'ro: no borra');
    PERFORM pg_temp.expect_error(format('INSERT INTO localidad VALUES (%L, %L, %L, %L)', '9999', 'X', 'Y', 'Z'), '42501', 'ro: no inserta');
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_ingreso(%s)', i1), '42501', 'ro: no ejecuta procedimientos');
    PERFORM pg_temp.expect_error('CALL sp_refrescar_reportes()', '42501', 'ro: no refresca reportes');
    PERFORM pg_temp.expect_error('CREATE TABLE intruso (id INT)', '42501', 'ro: no hace DDL');

    RESET ROLE;

    RAISE NOTICE 'OK: todas las pruebas de 007_roles pasaron';
END;
$$;

ROLLBACK;

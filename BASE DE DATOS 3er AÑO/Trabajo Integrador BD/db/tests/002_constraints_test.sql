-- =============================================================================
-- Pruebas de 001_esquema.sql y 002_constraints.sql: cada regla de integridad declarativa
-- (RN-01, 02, 03, 04, 07, 14, 15, jerarquia de clientes, DEFAULT) rechaza lo invalido con el SQLSTATE exacto.
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/002_constraints_test.sql
-- Dentro de una transaccion con ROLLBACK. Requiere la base vacia.
-- =============================================================================
BEGIN;

CREATE FUNCTION pg_temp.expect_error(p_sql TEXT, p_sqlstate TEXT, p_desc TEXT)
RETURNS VOID LANGUAGE plpgsql AS $f$
BEGIN
    BEGIN
        EXECUTE p_sql;
    EXCEPTION WHEN OTHERS THEN
        IF SQLSTATE = p_sqlstate THEN RETURN; END IF;
        RAISE EXCEPTION 'FALLO [%]: se esperaba % pero llego % (%)', p_desc, p_sqlstate, SQLSTATE, SQLERRM;
    END;
    RAISE EXCEPTION 'FALLO [%]: se esperaba el error % pero la sentencia se ejecuto', p_desc, p_sqlstate;
END;
$f$;

DO $$
DECLARE
    v_sala INTEGER; v_finca INTEGER; v_cepa INTEGER; v_vino INTEGER; v_cli INTEGER; v_trans INTEGER;
    v_ing INTEGER; v_estado estado_documento; v_fecha DATE;
BEGIN
    INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Encargado');
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Calle', 1, 'lunes', '5600') RETURNING id_sala INTO v_sala;
    INSERT INTO bodega VALUES ('30111111119', 'Bodega', 'Dom');
    INSERT INTO finca (nombre, superficie_ha, departamento, provincia) VALUES ('F', 10, 'San Rafael', 'Mendoza') RETURNING id_finca INTO v_finca;
    INSERT INTO cepa (nombre, tipo) VALUES ('Malbec', 'tinta') RETURNING id_cepa INTO v_cepa;
    INSERT INTO parcela VALUES (v_finca, 1, 5, 2010, v_cepa);
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega) VALUES ('V','tinto',2022,750,13,1000,'30111111119') RETURNING cod_vino INTO v_vino;
    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente,descuento) VALUES ('C','DNI','1','D','5600','exportador',30) RETURNING id_cliente INTO v_cli;
    INSERT INTO exportador (id_cliente, pais_destino) VALUES (v_cli, 'Brasil');
    INSERT INTO transportista (razon_social, cuit, email, telefono, domicilio) VALUES ('T','30222222223','t@t.com','1','R') RETURNING cod_transportista INTO v_trans;

    -- RN-01 / RN-15: positivos y rangos
    PERFORM pg_temp.expect_error(format('UPDATE vino SET precio = 0 WHERE cod_vino = %s', v_vino), '23514', 'RN-01 precio > 0');
    PERFORM pg_temp.expect_error(format('UPDATE vino SET graduacion = 4.9 WHERE cod_vino = %s', v_vino), '23514', 'RN-15 graduacion >= 5');
    PERFORM pg_temp.expect_error(format('UPDATE vino SET graduacion = 20.1 WHERE cod_vino = %s', v_vino), '23514', 'RN-15 graduacion <= 20');
    PERFORM pg_temp.expect_error(format('UPDATE vino SET volumen_ml = 1000 WHERE cod_vino = %s', v_vino), '23514', 'presentacion 375/750/1500');
    PERFORM pg_temp.expect_error($q$INSERT INTO finca (nombre, superficie_ha, departamento, provincia) VALUES ('X', 0, 'd', 'p')$q$, '23514', 'RN-15 superficie > 0');
    PERFORM pg_temp.expect_error(format('INSERT INTO lote_uva (id_finca,nro_parcela,campania,fecha_cosecha,kg,cuit_bodega) VALUES (%s,1,2024,CURRENT_DATE,0,%L)', v_finca, '30111111119'), '23514', 'RN-15 kg > 0');
    PERFORM pg_temp.expect_error(format('INSERT INTO empleado VALUES (%L, %L, CURRENT_DATE, -5, %s)', '20123456786', 'E', v_sala), '23514', 'RN-15 salario > 0');
    PERFORM pg_temp.expect_error(format('INSERT INTO stock_sala VALUES (%s, %s, -1)', v_sala, v_vino), '23514', 'RN-09 stock >= 0');
    PERFORM pg_temp.expect_error($q$INSERT INTO bodega VALUES ('123', 'X', 'Y')$q$, '23514', 'dominio cuit_dom: 11 digitos');

    -- RN-04: una sola cosecha por parcela y campaña
    INSERT INTO lote_uva (id_finca,nro_parcela,campania,fecha_cosecha,kg,cuit_bodega) VALUES (v_finca,1,2024,CURRENT_DATE,1000,'30111111119');
    PERFORM pg_temp.expect_error(format('INSERT INTO lote_uva (id_finca,nro_parcela,campania,fecha_cosecha,kg,cuit_bodega) VALUES (%s,1,2024,CURRENT_DATE,500,%L)', v_finca, '30111111119'), '23505', 'RN-04 una cosecha por parcela y campania');
    INSERT INTO lote_uva (id_finca,nro_parcela,campania,fecha_cosecha,kg,cuit_bodega) VALUES (v_finca,1,2025,CURRENT_DATE,500,'30111111119');   -- otra campania: valido
    PERFORM pg_temp.expect_error(format('INSERT INTO parcela VALUES (%s, 2, 5, 2010, NULL)', v_finca), '23502', 'RN-04 la parcela tiene cepa (NOT NULL)');
    PERFORM pg_temp.expect_error(format('INSERT INTO parcela VALUES (%s, 1, 5, 2010, %s)', v_finca, v_cepa), '23505', 'PK de la entidad debil: (finca, nro_parcela)');

    -- RN-03 / RN-02
    PERFORM pg_temp.expect_error(format('INSERT INTO empleado VALUES (%L, %L, CURRENT_DATE, 100, NULL)', '20123456786', 'E'), '23502', 'RN-03 empleado con sala (NOT NULL)');
    PERFORM pg_temp.expect_error($q$INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Otra', 2, 'lunes', '0000')$q$, '23503', 'RN-02 la sala pertenece a una localidad existente');
    PERFORM pg_temp.expect_error($q$INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Otra', 2, 'feriado', '5600')$q$, '23514', 'dia de cierre valido');

    -- RN-07: permisos de exportacion
    INSERT INTO permiso_exportacion VALUES ('P1', v_cli, DATE '2026-01-01', DATE '2027-01-01');
    INSERT INTO permiso_exportacion VALUES ('P2', v_cli, DATE '2026-02-01', DATE '2027-02-01');          -- varios permisos: valido
    PERFORM pg_temp.expect_error(format('INSERT INTO permiso_exportacion VALUES (%L, %s, DATE %L, DATE %L)', 'P3', v_cli, '2026-05-01', '2026-05-01'), '23514', 'RN-07 vencimiento posterior a emision');

    -- Jerarquia disjunta: un cliente exportador no puede ser tambien distribuidor ni socio
    PERFORM pg_temp.expect_error(format('INSERT INTO distribuidor (id_cliente, zona_cobertura, nro_habilitacion) VALUES (%s, %L, %L)', v_cli, 'z', 'h'), '23503', 'jerarquia disjunta (distribuidor)');
    PERFORM pg_temp.expect_error(format('INSERT INTO socio (id_cliente) VALUES (%s)', v_cli), '23503', 'jerarquia disjunta (socio)');
    PERFORM pg_temp.expect_error(format($q$UPDATE cliente SET tipo_cliente = 'socio' WHERE id_cliente = %s$q$, v_cli), '23514', 'no se cambia el tipo de un cliente con subtipo');
    PERFORM pg_temp.expect_error($q$INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente,descuento) VALUES ('X','DNI','2','D','5600','mayorista',10)$q$, '23514', 'tipo de cliente valido');
    PERFORM pg_temp.expect_error($q$INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente,descuento) VALUES ('X','DNI','1','D','5600','socio',10)$q$, '23505', 'documento unico por tipo');
    PERFORM pg_temp.expect_error($q$INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente,descuento) VALUES ('X','DNI','3','D','5600','socio',101)$q$, '23514', 'RN-06 descuento entre 0 y 100');

    -- RN-14: no se borran bodega, vino ni transportista con movimientos
    INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (v_trans, '30111111119') RETURNING cod_ingreso INTO v_ing;
    INSERT INTO renglon_ingreso VALUES (v_ing, v_vino, 10);
    PERFORM pg_temp.expect_error($q$DELETE FROM bodega WHERE cuit = '30111111119'$q$, '23503', 'RN-14 bodega con vinos/ingresos');
    PERFORM pg_temp.expect_error(format('DELETE FROM transportista WHERE cod_transportista = %s', v_trans), '23503', 'RN-14 transportista con ingresos');
    PERFORM pg_temp.expect_error(format('DELETE FROM vino WHERE cod_vino = %s', v_vino), '23503', 'RN-14 vino con movimientos');
    INSERT INTO empleado VALUES ('20123456786', 'Empleado', CURRENT_DATE, 100, v_sala);
    PERFORM pg_temp.expect_error(format('DELETE FROM sala_venta WHERE id_sala = %s', v_sala), '23503', 'una sala con empleados no se borra (RN-03)');

    -- DEFAULT
    SELECT estado INTO v_estado FROM ingreso WHERE cod_ingreso = v_ing;
    ASSERT v_estado = 'en_confeccion', 'DEFAULT estado = en_confeccion';
    SELECT fecha INTO v_fecha FROM ingreso WHERE cod_ingreso = v_ing;
    ASSERT v_fecha = CURRENT_DATE, 'DEFAULT fecha = hoy';
    ASSERT (SELECT fecha_alta FROM cliente WHERE id_cliente = v_cli) = CURRENT_DATE, 'DEFAULT fecha_alta = hoy';
    INSERT INTO stock_deposito (cod_vino) VALUES (v_vino);
    ASSERT (SELECT cantidad FROM stock_deposito WHERE cod_vino = v_vino) = 0, 'DEFAULT stock = 0';

    RAISE NOTICE 'OK: todas las pruebas de 002_constraints pasaron';
END;
$$;

ROLLBACK;

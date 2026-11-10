-- =============================================================================
-- Pruebas de 004_procedimientos.sql y 005_triggers.sql (reglas RN-05 a RN-13)
-- Se ejecuta dentro de una transaccion que termina en ROLLBACK: no deja datos.
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/005_reglas_test.sql
-- Cada prueba negativa verifica el SQLSTATE exacto, no solo "que falle".
-- =============================================================================
BEGIN;

-- Ejecuta una sentencia que DEBE fallar con el SQLSTATE indicado. Corre en una
-- subtransaccion: lo que haya hecho la sentencia se revierte.
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
    v_sala1 INTEGER; v_sala2 INTEGER;
    v_trans INTEGER;
    v_cepa1 INTEGER; v_cepa2 INTEGER;
    vA INTEGER; vB INTEGER; vC INTEGER;
    v_socio INTEGER; v_expo INTEGER;
    c1 INTEGER; c2 INTEGER; c3 INTEGER;
    i1 INTEGER; i2 INTEGER; i_vacio INTEGER;
    t1 INTEGER; t2 INTEGER;
    n INTEGER;
    rc RECORD;
    v_estado estado_documento;
BEGIN
    -- ------------------------------------------------------------------ datos
    INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Encargado Test');
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal)
        VALUES ('Calle A', 1, 'lunes', '5600') RETURNING id_sala INTO v_sala1;
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal)
        VALUES ('Calle B', 2, 'martes', '5600') RETURNING id_sala INTO v_sala2;
    INSERT INTO bodega VALUES ('30111111119', 'Bodega Test', 'Domicilio');
    INSERT INTO transportista (razon_social, cuit, email, telefono, domicilio)
        VALUES ('Transporte Test', '30222222223', 'trans@test.com', '2604000000', 'Ruta 143')
        RETURNING cod_transportista INTO v_trans;
    INSERT INTO cepa (nombre, tipo) VALUES ('Malbec', 'tinta') RETURNING id_cepa INTO v_cepa1;
    INSERT INTO cepa (nombre, tipo) VALUES ('Syrah',  'tinta') RETURNING id_cepa INTO v_cepa2;

    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('A','tinto',2022,750,13,1000,'30111111119') RETURNING cod_vino INTO vA;
    INSERT INTO composicion VALUES (vA, v_cepa1, 60), (vA, v_cepa2, 40);
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('B','blanco',2023,750,12,2000,'30111111119') RETURNING cod_vino INTO vB;
    INSERT INTO composicion VALUES (vB, v_cepa1, 100);
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('C','rosado',2023,750,12,500,'30111111119') RETURNING cod_vino INTO vC;
    INSERT INTO composicion VALUES (vC, v_cepa2, 100);

    -- ------------------------------------------- RN-06 + jerarquia de clientes
    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente)
        VALUES ('Socio Test','DNI','1','Dir','5600','socio') RETURNING id_cliente INTO v_socio;
    INSERT INTO socio (id_cliente) VALUES (v_socio);
    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente)
        VALUES ('Expo Test','CUIT','2','Dir','5600','exportador') RETURNING id_cliente INTO v_expo;
    INSERT INTO exportador (id_cliente, pais_destino) VALUES (v_expo, 'Brasil');

    ASSERT fn_descuento_cliente(v_socio) = 10, 'RN-06: el socio debe quedar con 10% sin informarlo';
    ASSERT fn_descuento_cliente(v_expo)  = 30, 'RN-06: el exportador debe quedar con 30% sin informarlo';

    -- Todo lo cargado hasta aqui es valido: los triggers diferidos deben aceptarlo.
    SET CONSTRAINTS ALL IMMEDIATE;
    SET CONSTRAINTS ALL DEFERRED;

    PERFORM pg_temp.expect_error($q$
        INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente)
            VALUES ('Sin subtipo','DNI','99','Dir','5600','socio');
        SET CONSTRAINTS ALL IMMEDIATE$q$,
        'RN006', 'cliente sin fila de subtipo');
    PERFORM pg_temp.expect_error(format($q$
        INSERT INTO distribuidor (id_cliente, zona_cobertura, nro_habilitacion) VALUES (%s, 'z', 'h1')$q$, v_socio),
        '23503', 'un socio no puede cargarse como distribuidor (jerarquia disjunta)');

    -- ------------------------------------------------------------------ RN-05
    PERFORM pg_temp.expect_error($q$
        INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
            VALUES ('Z','tinto',2022,750,13,100,'30111111119');
        SET CONSTRAINTS ALL IMMEDIATE$q$,
        'RN005', 'vino sin corte');
    PERFORM pg_temp.expect_error(format($q$
        INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
            VALUES ('Z','tinto',2022,750,13,100,'30111111119');
        INSERT INTO composicion SELECT cod_vino, %s, 60 FROM vino WHERE nombre = 'Z';
        SET CONSTRAINTS ALL IMMEDIATE$q$, v_cepa1),
        'RN005', 'corte que suma 60');
    PERFORM pg_temp.expect_error(format($q$
        UPDATE composicion SET porcentaje = 50 WHERE cod_vino = %s AND id_cepa = %s;
        SET CONSTRAINTS ALL IMMEDIATE$q$, vA, v_cepa1),
        'RN005', 'modificar un porcentaje deja la suma en 90');
    PERFORM pg_temp.expect_error(format($q$
        DELETE FROM composicion WHERE cod_vino = %s AND id_cepa = %s;
        SET CONSTRAINTS ALL IMMEDIATE$q$, vA, v_cepa2),
        'RN005', 'quitar una cepa deja la suma en 60');
    -- Cambiar dos filas juntas para llegar a 100 es valido (por eso es diferido).
    UPDATE composicion SET porcentaje = 70 WHERE cod_vino = vA AND id_cepa = v_cepa1;
    UPDATE composicion SET porcentaje = 30 WHERE cod_vino = vA AND id_cepa = v_cepa2;
    SET CONSTRAINTS ALL IMMEDIATE;
    SET CONSTRAINTS ALL DEFERRED;
    -- Borrar un vino entero (cascada sobre su corte) no debe reportar error de corte.
    DELETE FROM vino WHERE cod_vino = vC;
    SET CONSTRAINTS ALL IMMEDIATE;
    SET CONSTRAINTS ALL DEFERRED;
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('C','rosado',2023,750,12,500,'30111111119') RETURNING cod_vino INTO vC;
    INSERT INTO composicion VALUES (vC, v_cepa2, 100);

    -- ------------------------------------------------------------------ RN-13
    SELECT count(*) INTO n FROM auditoria_precio;
    ASSERT n = 0, 'RN-13: no hay auditoria antes de cambiar precios';
    UPDATE vino SET precio = 1200 WHERE cod_vino = vA;
    SELECT * INTO rc FROM auditoria_precio WHERE cod_vino = vA;
    ASSERT rc.precio_anterior = 1000 AND rc.precio_nuevo = 1200, 'RN-13: auditoria con precio anterior y nuevo';
    ASSERT rc.usuario = session_user, 'RN-13: auditoria registra el usuario';
    ASSERT rc.fecha_hora IS NOT NULL, 'RN-13: auditoria registra la fecha';
    UPDATE vino SET precio = 1200 WHERE cod_vino = vA;          -- mismo precio
    UPDATE vino SET nombre = 'A2' WHERE cod_vino = vA;          -- otra columna
    UPDATE vino SET nombre = 'A' WHERE cod_vino = vA;
    SELECT count(*) INTO n FROM auditoria_precio WHERE cod_vino = vA;
    ASSERT n = 1, 'RN-13: solo los cambios reales de precio se auditan';
    UPDATE vino SET precio = 1000 WHERE cod_vino = vA;          -- vuelve a 1000 para las ventas
    SELECT count(*) INTO n FROM auditoria_precio WHERE cod_vino = vA;
    ASSERT n = 2, 'RN-13: cada cambio queda registrado';
    PERFORM pg_temp.expect_error(format(
        'UPDATE vino SET precio = 0 WHERE cod_vino = %s', vA), '23514', 'RN-01: precio > 0');

    -- ------------------------------------------------------------ RN-08 / RN-09
    INSERT INTO stock_sala VALUES (v_sala1, vA, 10);

    INSERT INTO comprobante (id_cliente, id_sala) VALUES (v_socio, v_sala1) RETURNING nro_comprobante INTO c1;
    -- Valores "tramposos" informados a mano: la base los pisa.
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad, precio_unitario, descuento_pct, subtotal)
        VALUES (c1, vA, 3, 1, 99, 1);
    SELECT * INTO rc FROM renglon_comprobante WHERE nro_comprobante = c1 AND cod_vino = vA;
    ASSERT rc.precio_unitario = 1000, 'RN-08: el renglon toma el precio vigente del vino';
    ASSERT rc.descuento_pct = 10,     'RN-06: el renglon toma el descuento del cliente (socio 10%)';
    ASSERT rc.subtotal = 2700,        'RN-08: subtotal calculado por la base';
    SELECT * INTO rc FROM comprobante WHERE nro_comprobante = c1;
    ASSERT rc.subtotal = 3000 AND rc.descuento = 300 AND rc.total = 2700, 'RN-08: importes del comprobante';
    ASSERT fn_stock_sala(v_sala1, vA) = 7, 'RN-09: la venta descuenta el stock de la sala';

    UPDATE comprobante SET total = 1, subtotal = 1, descuento = 0 WHERE nro_comprobante = c1;
    SELECT * INTO rc FROM comprobante WHERE nro_comprobante = c1;
    ASSERT rc.subtotal = 3000 AND rc.total = 2700, 'RN-08: el total no se puede cargar a mano';

    PERFORM pg_temp.expect_error(format(
        'INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (%s, %s, 1)', c1, vB),
        'RN009', 'RN-09: vender un vino sin stock');
    PERFORM pg_temp.expect_error(format(
        'INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (%s, -1, 1)', c1),
        '23502', 'un vino inexistente es error de integridad (sin precio), no de stock insuficiente RN009');

    INSERT INTO comprobante (id_cliente, id_sala) VALUES (v_expo, v_sala1) RETURNING nro_comprobante INTO c2;
    PERFORM pg_temp.expect_error(format(
        'INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (%s, %s, 8)', c2, vA),
        'RN009', 'RN-09: vender mas de lo que hay (8 > 7)');
    ASSERT fn_stock_sala(v_sala1, vA) = 7, 'RN-09: la venta rechazada no toca el stock';
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c2, vA, 7);
    ASSERT fn_stock_sala(v_sala1, vA) = 0, 'RN-09: se puede vender exactamente todo el stock';
    SELECT * INTO rc FROM comprobante WHERE nro_comprobante = c2;
    ASSERT rc.subtotal = 7000 AND rc.descuento = 2100 AND rc.total = 4900, 'RN-06/08: exportador 30% sobre 7x1000';

    UPDATE vino SET precio = 1500 WHERE cod_vino = vA;
    SELECT total INTO rc FROM comprobante WHERE nro_comprobante = c1;
    ASSERT rc.total = 2700, 'cambiar el precio no altera ventas ya hechas';
    UPDATE vino SET precio = 1000 WHERE cod_vino = vA;

    PERFORM pg_temp.expect_error(format(
        'UPDATE renglon_comprobante SET cantidad = 1 WHERE nro_comprobante = %s', c1),
        'RN008', 'un renglon de venta no cambia de cantidad');
    PERFORM pg_temp.expect_error(format(
        'UPDATE comprobante SET id_sala = %s WHERE nro_comprobante = %s', v_sala2, c1),
        'RN008', 'no se cambia la sala de un comprobante con renglones');

    -- Recalculo de descuento (consulta U1): el renglon se recalcula y arrastra al comprobante.
    UPDATE renglon_comprobante SET descuento_pct = 0 WHERE nro_comprobante = c1;
    SELECT * INTO rc FROM comprobante WHERE nro_comprobante = c1;
    ASSERT rc.subtotal = 3000 AND rc.descuento = 0 AND rc.total = 3000, 'RN-08: UPDATE de renglon recalcula el comprobante';

    -- Borrar un renglon recalcula el comprobante y NO devuelve stock.
    DELETE FROM renglon_comprobante WHERE nro_comprobante = c1;
    SELECT * INTO rc FROM comprobante WHERE nro_comprobante = c1;
    ASSERT rc.subtotal = 0 AND rc.descuento = 0 AND rc.total = 0, 'RN-08: comprobante sin renglones queda en 0';
    ASSERT fn_stock_sala(v_sala1, vA) = 0, 'borrar un renglon no regenera stock';
    -- Borrar un comprobante entero (cascada de renglones) funciona.
    DELETE FROM comprobante WHERE nro_comprobante = c2;
    SELECT count(*) INTO n FROM renglon_comprobante WHERE nro_comprobante = c2;
    ASSERT n = 0, 'borrar el comprobante borra sus renglones';

    -- ------------------------------------------------------------ RN-10 / RN-12
    INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (v_trans, '30111111119') RETURNING cod_ingreso INTO i1;
    SELECT estado INTO v_estado FROM ingreso WHERE cod_ingreso = i1;
    ASSERT v_estado = 'en_confeccion', 'RN-10: un ingreso nace en_confeccion';
    INSERT INTO renglon_ingreso VALUES (i1, vA, 100), (i1, vB, 50);

    PERFORM pg_temp.expect_error(format(
        $q$INSERT INTO ingreso (cod_transportista, cuit_bodega, estado) VALUES (%s, '30111111119', 'terminado')$q$, v_trans),
        'RN010', 'RN-10: no se crea un ingreso ya terminado');
    INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (v_trans, '30111111119') RETURNING cod_ingreso INTO i_vacio;
    PERFORM pg_temp.expect_error(format(
        $q$UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = %s$q$, i_vacio),
        'RN010', 'RN-10: no se termina un ingreso sin renglones');
    PERFORM pg_temp.expect_error(format(
        $q$UPDATE ingreso SET estado = 'procesado' WHERE cod_ingreso = %s$q$, i1),
        'RN010', 'RN-10: no se saltea la etapa terminado');
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_ingreso(%s)', i1),
        'RN010', 'RN-10: un ingreso en confeccion no se procesa');
    PERFORM pg_temp.expect_error('CALL sp_procesar_ingreso(-1)', 'P0002', 'ingreso inexistente');

    UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = i1;
    PERFORM pg_temp.expect_error(format('INSERT INTO renglon_ingreso VALUES (%s, %s, 5)', i1, vC),
        'RN012', 'RN-12: no se agregan renglones a un ingreso terminado');
    PERFORM pg_temp.expect_error(format('UPDATE renglon_ingreso SET cantidad = 1 WHERE cod_ingreso = %s', i1),
        'RN012', 'RN-12: no se modifican renglones de un ingreso terminado');
    PERFORM pg_temp.expect_error(format('DELETE FROM renglon_ingreso WHERE cod_ingreso = %s', i1),
        'RN012', 'RN-12: no se quitan renglones de un ingreso terminado');
    PERFORM pg_temp.expect_error(format('UPDATE ingreso SET cod_transportista = cod_transportista WHERE cod_ingreso = %s', i1),
        'RN010', 'RN-10: la cabecera de un ingreso terminado no se edita');
    PERFORM pg_temp.expect_error(format(
        $q$UPDATE ingreso SET estado = 'procesado' WHERE cod_ingreso = %s$q$, i1),
        'RN010', 'RN-10: terminado -> procesado solo vale a traves del procedimiento');
    ASSERT fn_stock_deposito(vA) = 0, 'los intentos rechazados no tocaron el deposito';

    CALL sp_procesar_ingreso(i1);
    SELECT estado INTO v_estado FROM ingreso WHERE cod_ingreso = i1;
    ASSERT v_estado = 'procesado', 'RN-10: el procedimiento deja el ingreso procesado';
    ASSERT fn_stock_deposito(vA) = 100 AND fn_stock_deposito(vB) = 50, 'RN-10: el ingreso suma al deposito';
    ASSERT current_setting('atuel.sp_activo') = 'off', 'el indicador del procedimiento se apaga al terminar';
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_ingreso(%s)', i1),
        'RN010', 'RN-10: un ingreso procesado no se vuelve a procesar');
    PERFORM pg_temp.expect_error(format(
        $q$UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = %s$q$, i1),
        'RN010', 'RN-10: no se retrocede de procesado');

    INSERT INTO ingreso (cod_transportista, cuit_bodega) VALUES (v_trans, '30111111119') RETURNING cod_ingreso INTO i2;
    INSERT INTO renglon_ingreso VALUES (i2, vA, 20);
    UPDATE ingreso SET estado = 'terminado' WHERE cod_ingreso = i2;
    CALL sp_procesar_ingreso(i2);
    ASSERT fn_stock_deposito(vA) = 120, 'RN-10: los ingresos se acumulan en el deposito';

    -- Borrar un ingreso procesado (consulta D5) arrastra sus renglones sin chocar con RN-12.
    DELETE FROM ingreso WHERE cod_ingreso = i1;
    SELECT count(*) INTO n FROM renglon_ingreso WHERE cod_ingreso = i1;
    ASSERT n = 0, 'borrar un ingreso procesado borra sus renglones (cascada)';
    ASSERT fn_stock_deposito(vA) = 120, 'borrar el ingreso no altera el deposito';

    -- ------------------------------------------------------------ RN-11 / RN-12
    INSERT INTO transferencia (id_sala, fecha_confeccion) VALUES (v_sala2, DATE '2000-01-01')
        RETURNING nro_transferencia INTO t1;
    SELECT fecha_confeccion INTO rc FROM transferencia WHERE nro_transferencia = t1;
    ASSERT rc.fecha_confeccion = CURRENT_DATE, 'RN-11: la fecha de confeccion es la actual, aunque se informe otra';
    PERFORM pg_temp.expect_error(format(
        $q$UPDATE transferencia SET fecha_confeccion = DATE '2001-01-01' WHERE nro_transferencia = %s$q$, t1),
        'RN011', 'RN-11: la fecha de confeccion no se modifica');
    PERFORM pg_temp.expect_error(format(
        $q$INSERT INTO transferencia (id_sala, estado) VALUES (%s, 'terminado')$q$, v_sala2),
        'RN011', 'RN-11: no se crea una transferencia ya terminada');

    -- Pedido que el deposito no puede cubrir (vB: 60 > 50)
    INSERT INTO renglon_transferencia VALUES (t1, vA, 30), (t1, vB, 60);
    UPDATE transferencia SET estado = 'terminado' WHERE nro_transferencia = t1;
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_transferencia(%s)', t1),
        'RN011', 'RN-11: sin stock suficiente en el deposito');
    ASSERT fn_stock_deposito(vA) = 120 AND fn_stock_deposito(vB) = 50,
        'RN-11: el procedimiento es atomico (el vino A tampoco se desconto)';
    ASSERT fn_stock_sala(v_sala2, vA) = 0, 'RN-11: la sala no recibio nada';
    SELECT estado INTO v_estado FROM transferencia WHERE nro_transferencia = t1;
    ASSERT v_estado = 'terminado', 'RN-11: la transferencia fallida sigue terminada';
    PERFORM pg_temp.expect_error(format('DELETE FROM renglon_transferencia WHERE nro_transferencia = %s', t1),
        'RN012', 'RN-12: no se quitan renglones de una transferencia terminada');

    INSERT INTO transferencia (id_sala) VALUES (v_sala2) RETURNING nro_transferencia INTO t2;
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_transferencia(%s)', t2),
        'RN011', 'RN-11: una transferencia en confeccion no se procesa');
    INSERT INTO renglon_transferencia VALUES (t2, vA, 30), (t2, vB, 20);
    UPDATE transferencia SET estado = 'terminado' WHERE nro_transferencia = t2;
    CALL sp_procesar_transferencia(t2);
    ASSERT fn_stock_deposito(vA) = 90 AND fn_stock_deposito(vB) = 30, 'RN-11: descuenta del deposito';
    ASSERT fn_stock_sala(v_sala2, vA) = 30 AND fn_stock_sala(v_sala2, vB) = 20, 'RN-11: suma al stock de la sala';
    SELECT estado INTO v_estado FROM transferencia WHERE nro_transferencia = t2;
    ASSERT v_estado = 'procesado', 'RN-11: queda procesada';
    PERFORM pg_temp.expect_error(format('CALL sp_procesar_transferencia(%s)', t2),
        'RN011', 'RN-11: una transferencia procesada no se vuelve a procesar');

    -- La sala ya puede vender lo transferido (integracion transferencia -> venta)
    INSERT INTO comprobante (id_cliente, id_sala) VALUES (v_socio, v_sala2) RETURNING nro_comprobante INTO c3;
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c3, vA, 5);
    ASSERT fn_stock_sala(v_sala2, vA) = 25, 'la sala vende desde el stock recibido por transferencia';

    -- Todo el estado final debe respetar los constraints diferidos.
    SET CONSTRAINTS ALL IMMEDIATE;

    RAISE NOTICE 'OK: todas las pruebas de 004_procedimientos y 005_triggers pasaron';
END;
$$;

ROLLBACK;

-- =============================================================================
-- Pruebas de 006_vistas.sql (dentro de una transacción con ROLLBACK)
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/006_vistas_test.sql
-- =============================================================================
BEGIN;

DO $$
DECLARE
    v_sala1 INTEGER; v_sala2 INTEGER; v_cepa1 INTEGER; v_cepa2 INTEGER;
    vA INTEGER; vB INTEGER; v_cli INTEGER; c1 INTEGER; c2 INTEGER;
    rc RECORD;
BEGIN
    INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Enc');
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Calle A', 10, 'lunes', '5600') RETURNING id_sala INTO v_sala1;
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal) VALUES ('Calle B', 20, 'martes', '5600') RETURNING id_sala INTO v_sala2;
    INSERT INTO bodega VALUES ('30111111119', 'Bodega Test', 'Dom');
    INSERT INTO cepa (nombre, tipo) VALUES ('Malbec', 'tinta') RETURNING id_cepa INTO v_cepa1;
    INSERT INTO cepa (nombre, tipo) VALUES ('Syrah', 'tinta') RETURNING id_cepa INTO v_cepa2;
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('A','tinto',2022,750,13,1000,'30111111119') RETURNING cod_vino INTO vA;
    INSERT INTO composicion VALUES (vA, v_cepa1, 60), (vA, v_cepa2, 40);
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('B','blanco',2023,750,12,2000,'30111111119') RETURNING cod_vino INTO vB;
    INSERT INTO composicion VALUES (vB, v_cepa1, 100);
    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente)
        VALUES ('Socio Test','DNI','1','Dir','5600','socio') RETURNING id_cliente INTO v_cli;
    INSERT INTO socio VALUES (v_cli);

    -- v_stock_vino
    INSERT INTO stock_deposito VALUES (vA, 40);
    INSERT INTO stock_sala VALUES (v_sala1, vA, 10), (v_sala2, vA, 5);
    SELECT * INTO rc FROM v_stock_vino WHERE cod_vino = vA;
    ASSERT rc.stock_deposito = 40 AND rc.stock_salas = 15 AND rc.stock_total = 55, 'v_stock_vino suma deposito y salas';
    SELECT * INTO rc FROM v_stock_vino WHERE cod_vino = vB;
    ASSERT rc.stock_deposito = 0 AND rc.stock_salas = 0 AND rc.stock_total = 0, 'v_stock_vino: vino sin stock aparece en 0';

    -- v_catalogo_vino
    SELECT * INTO rc FROM v_catalogo_vino WHERE cod_vino = vA;
    ASSERT rc.corte = 'Malbec 60%, Syrah 40%', 'v_catalogo_vino arma el corte ordenado: ' || rc.corte;
    ASSERT rc.bodega = 'Bodega Test' AND rc.stock_total = 55, 'v_catalogo_vino trae bodega y stock';
    SELECT * INTO rc FROM v_catalogo_vino WHERE cod_vino = vB;
    ASSERT rc.corte = 'Malbec 100%', 'corte de un solo varietal';

    -- v_comprobante_detalle y mv
    INSERT INTO comprobante (fecha, id_cliente, id_sala) VALUES (DATE '2026-03-10', v_cli, v_sala1) RETURNING nro_comprobante INTO c1;
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c1, vA, 3);
    INSERT INTO comprobante (fecha, id_cliente, id_sala) VALUES (DATE '2026-03-20', v_cli, v_sala1) RETURNING nro_comprobante INTO c2;
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c2, vA, 2);
    INSERT INTO comprobante (fecha, id_cliente, id_sala) VALUES (DATE '2026-03-21', v_cli, v_sala2);   -- sin renglones

    SELECT * INTO rc FROM v_comprobante_detalle WHERE nro_comprobante = c1;
    ASSERT rc.cliente = 'Socio Test' AND rc.tipo_cliente = 'socio', 'detalle: cliente';
    ASSERT rc.sala = 'Calle A 10' AND rc.localidad_sala = 'San Rafael', 'detalle: sala y localidad';
    ASSERT rc.renglones = 1 AND rc.unidades = 3 AND rc.total = 2700, 'detalle: renglones, unidades y total';
    SELECT count(*) INTO rc FROM v_comprobante_detalle WHERE renglones = 0;
    ASSERT rc.count = 1, 'detalle: el comprobante sin renglones aparece con 0';

    REFRESH MATERIALIZED VIEW mv_ventas_mensuales_sala;
    SELECT * INTO rc FROM mv_ventas_mensuales_sala WHERE id_sala = v_sala1;
    ASSERT rc.mes = DATE '2026-03-01', 'mv: agrupa por mes';
    ASSERT rc.comprobantes = 2 AND rc.unidades = 5 AND rc.total_vendido = 4500, 'mv: 2 comprobantes, 5 unidades, 4500';
    SELECT count(*) INTO rc FROM mv_ventas_mensuales_sala WHERE id_sala = v_sala2;
    ASSERT rc.count = 0, 'mv: una sala sin ventas con renglones no aparece';

    -- La materializada no se actualiza sola: conserva la foto vieja hasta el REFRESH.
    INSERT INTO stock_sala VALUES (v_sala1, vB, 5);
    INSERT INTO renglon_comprobante (nro_comprobante, cod_vino, cantidad) VALUES (c2, vB, 1);   -- 2000 - 10% = 1800
    SELECT * INTO rc FROM mv_ventas_mensuales_sala WHERE id_sala = v_sala1;
    ASSERT rc.total_vendido = 4500, 'mv: antes del REFRESH conserva el valor anterior';
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_ventas_mensuales_sala;
    SELECT * INTO rc FROM mv_ventas_mensuales_sala WHERE id_sala = v_sala1;
    ASSERT rc.total_vendido = 6300 AND rc.unidades = 6, 'mv: despues del REFRESH CONCURRENTLY refleja la venta nueva';

    RAISE NOTICE 'OK: todas las pruebas de 006_vistas pasaron';
END;
$$;

ROLLBACK;

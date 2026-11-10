-- =============================================================================
-- Pruebas de 003_funciones.sql
-- Se ejecuta dentro de una transacción que termina en ROLLBACK: no deja datos.
--   docker exec -i bodegas_atuel_postgres sh -c \
--     'psql -U $POSTGRES_USER -d $POSTGRES_DB -v ON_ERROR_STOP=1' < db/tests/003_funciones_test.sql
-- Cada ASSERT falla con un mensaje que indica qué regla se rompió.
-- =============================================================================
BEGIN;

DO $$
DECLARE
    v_sala  INTEGER;
    v_vino1 INTEGER;
    v_vino2 INTEGER;
    v_vino3 INTEGER;
    v_cepa1 INTEGER;
    v_cli   INTEGER;
    v_comp  INTEGER;
    v_calc  RECORD;
BEGIN
    -- Datos mínimos
    INSERT INTO localidad VALUES ('5600', 'San Rafael', 'Mendoza', 'Encargado Test');
    INSERT INTO sala_venta (calle, numero, dia_cierre, cod_postal)
        VALUES ('Calle', 1, 'lunes', '5600') RETURNING id_sala INTO v_sala;
    INSERT INTO bodega VALUES ('30111111119', 'Bodega Test', 'Domicilio');
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('V1','tinto',2022,750,13,1000,'30111111119') RETURNING cod_vino INTO v_vino1;
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('V2','blanco',2023,750,12,2000,'30111111119') RETURNING cod_vino INTO v_vino2;
    INSERT INTO vino (nombre,tipo,anada,volumen_ml,graduacion,precio,cuit_bodega)
        VALUES ('V3','rosado',2023,750,12,500,'30111111119') RETURNING cod_vino INTO v_vino3;
    INSERT INTO cepa (nombre,tipo) VALUES ('Malbec','tinta') RETURNING id_cepa INTO v_cepa1;

    -- RN-06: descuento por tipo
    ASSERT fn_descuento_tipo_cliente('socio')        = 10, 'RN-06 socio debe ser 10';
    ASSERT fn_descuento_tipo_cliente('distribuidor') = 20, 'RN-06 distribuidor debe ser 20';
    ASSERT fn_descuento_tipo_cliente('exportador')   = 30, 'RN-06 exportador debe ser 30';
    ASSERT fn_descuento_tipo_cliente('inexistente') IS NULL, 'RN-06 tipo desconocido debe dar NULL';

    INSERT INTO cliente (nombre_razon_social,tipo_doc,nro_doc,direccion,cod_postal,tipo_cliente,descuento)
        VALUES ('Cliente Test','CUIT','20123456786','Dir','5600','exportador',
                fn_descuento_tipo_cliente('exportador'))
        RETURNING id_cliente INTO v_cli;
    ASSERT fn_descuento_cliente(v_cli) = 30, 'fn_descuento_cliente debe leer el descuento del cliente';
    ASSERT fn_descuento_cliente(-1) IS NULL, 'cliente inexistente debe dar NULL';

    -- RN-08: renglones y comprobante
    ASSERT fn_subtotal_renglon(3, 1000, 30) = 2100.00, 'subtotal renglon 3x1000 al 30%';
    ASSERT fn_subtotal_renglon(1, 99.99, 0) = 99.99,   'subtotal sin descuento';
    ASSERT fn_subtotal_renglon(3, 0.33, 15) = 0.84,    'subtotal redondea a 2 decimales';

    INSERT INTO comprobante (id_cliente, id_sala) VALUES (v_cli, v_sala)
        RETURNING nro_comprobante INTO v_comp;

    SELECT * INTO v_calc FROM fn_calcular_comprobante(v_comp);
    ASSERT v_calc.subtotal_bruto = 0 AND v_calc.monto_descuento = 0 AND v_calc.total = 0,
        'comprobante sin renglones debe dar todo 0';
    ASSERT fn_total_comprobante(v_comp) = 0, 'total sin renglones debe ser 0';

    -- Desde 005 la venta exige stock (RN-09): se carga antes de vender.
    INSERT INTO stock_sala VALUES (v_sala, v_vino1, 100), (v_sala, v_vino2, 100);
    INSERT INTO renglon_comprobante VALUES (v_comp, v_vino1, 3, 1000, 30, fn_subtotal_renglon(3, 1000, 30));
    INSERT INTO renglon_comprobante VALUES (v_comp, v_vino2, 1, 2000, 30, fn_subtotal_renglon(1, 2000, 30));

    SELECT * INTO v_calc FROM fn_calcular_comprobante(v_comp);
    ASSERT v_calc.subtotal_bruto   = 5000.00, 'subtotal bruto = 3x1000 + 1x2000';
    ASSERT v_calc.monto_descuento  = 1500.00, 'descuento = 30% de 5000';
    ASSERT v_calc.total            = 3500.00, 'total = 2100 + 1400';
    ASSERT v_calc.total = v_calc.subtotal_bruto - v_calc.monto_descuento, 'total = subtotal - descuento';
    ASSERT fn_total_comprobante(v_comp) = 3500.00, 'fn_total_comprobante = 3500';

    -- Los valores calculados cumplen el CHECK de comprobante (RN-08)
    UPDATE comprobante SET subtotal = v_calc.subtotal_bruto,
                           descuento = v_calc.monto_descuento,
                           total = v_calc.total
     WHERE nro_comprobante = v_comp;

    -- RN-09: stock (sin fila = 0)
    ASSERT fn_stock_sala(v_sala, v_vino3) = 0, 'sin fila de stock_sala debe dar 0';
    INSERT INTO stock_sala VALUES (v_sala, v_vino3, 10);
    ASSERT fn_stock_sala(v_sala, v_vino3) = 10, 'stock_sala debe reflejar la cantidad';
    ASSERT fn_stock_sala(v_sala, v_vino1) = 97, 'stock_sala refleja lo vendido (100 - 3)';
    ASSERT fn_stock_deposito(v_vino1) = 0, 'sin fila de stock_deposito debe dar 0';
    INSERT INTO stock_deposito VALUES (v_vino1, 250);
    ASSERT fn_stock_deposito(v_vino1) = 250, 'stock_deposito debe reflejar la cantidad';

    -- RN-05: suma del corte
    ASSERT fn_suma_composicion(v_vino3) = 0, 'vino sin corte suma 0';
    INSERT INTO cepa (nombre,tipo) VALUES ('Syrah','tinta');
    INSERT INTO composicion VALUES (v_vino3, v_cepa1, 60);
    ASSERT fn_suma_composicion(v_vino3) = 60, 'suma parcial 60';
    INSERT INTO composicion SELECT v_vino3, id_cepa, 40 FROM cepa WHERE nombre = 'Syrah';
    ASSERT fn_suma_composicion(v_vino3) = 100, 'suma completa 100';

    -- RN-10 / RN-11: transiciones
    ASSERT fn_transicion_estado_valida('en_confeccion','terminado') , 'en_confeccion -> terminado';
    ASSERT fn_transicion_estado_valida('terminado','procesado')     , 'terminado -> procesado';
    ASSERT NOT fn_transicion_estado_valida('en_confeccion','procesado'), 'no se puede saltear terminado';
    ASSERT NOT fn_transicion_estado_valida('procesado','terminado')    , 'no se retrocede';
    ASSERT NOT fn_transicion_estado_valida('terminado','en_confeccion'), 'no se retrocede';
    ASSERT NOT fn_transicion_estado_valida('procesado','procesado')    , 'mismo estado no es transicion';

    RAISE NOTICE 'OK: todas las pruebas de 003_funciones pasaron';
END;
$$;

ROLLBACK;

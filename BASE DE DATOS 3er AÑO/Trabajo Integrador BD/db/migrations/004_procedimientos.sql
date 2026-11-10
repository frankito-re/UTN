-- =============================================================================
-- 004_procedimientos.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Lógica en la base)
-- Procedimientos transaccionales que impactan el stock (RN-10, RN-11).
--
-- Cada CALL corre en la transacción del llamador: si cualquier paso falla se
-- revierte TODO (stock y estado). Para evitar deadlocks y lecturas viejas:
--   1. se bloquea el documento (FOR UPDATE) -> dos procesos simultáneos sobre
--      el mismo documento se serializan y el segundo ve el estado ya cambiado;
--   2. los renglones se recorren ordenados por cod_vino, de modo que dos
--      documentos distintos toman los bloqueos de stock en el mismo orden;
--   3. cada fila de stock se bloquea (FOR UPDATE) antes de validarla.
--
-- Los triggers de estado (005) solo permiten pasar a 'procesado' mientras el
-- indicador de transacción atuel.sp_activo vale 'on', que solo estos
-- procedimientos encienden. Así un UPDATE directo no puede saltear el impacto
-- en el stock.
--
-- SECURITY DEFINER: corren con los privilegios del propietario. El rol de la API
-- no tiene permiso de escritura directa sobre stock_deposito ni stock_sala
-- (ver 007_roles.sql): el stock solo cambia a traves de estos procedimientos y
-- de los triggers de venta. search_path fijo para evitar suplantacion de objetos.
--
-- Códigos de error propios (SQLSTATE, clase 'RN'): ver cabecera de 005.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- RN-10 · Procesar un ingreso: suma al stock del depósito central
-- -----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_procesar_ingreso(p_cod_ingreso INTEGER)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
    v_estado estado_documento;
    r        RECORD;
BEGIN
    SELECT i.estado INTO v_estado
      FROM ingreso i
     WHERE i.cod_ingreso = p_cod_ingreso
       FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El ingreso % no existe', p_cod_ingreso
            USING ERRCODE = 'no_data_found';
    END IF;

    IF v_estado <> 'terminado' THEN
        RAISE EXCEPTION 'Solo un ingreso terminado puede procesarse; el ingreso % esta %',
            p_cod_ingreso, v_estado
            USING ERRCODE = 'RN010';   -- RN-10
    END IF;

    FOR r IN
        SELECT ri.cod_vino, ri.cantidad
          FROM renglon_ingreso ri
         WHERE ri.cod_ingreso = p_cod_ingreso
         ORDER BY ri.cod_vino
    LOOP
        INSERT INTO stock_deposito AS d (cod_vino, cantidad)
        VALUES (r.cod_vino, r.cantidad)
        ON CONFLICT (cod_vino)
        DO UPDATE SET cantidad = d.cantidad + EXCLUDED.cantidad;
    END LOOP;

    PERFORM set_config('atuel.sp_activo', 'on', true);
    UPDATE ingreso SET estado = 'procesado' WHERE cod_ingreso = p_cod_ingreso;
    PERFORM set_config('atuel.sp_activo', 'off', true);
END;
$$;

-- -----------------------------------------------------------------------------
-- RN-11 · Procesar una transferencia: descuenta del depósito y suma a la sala
-- Requiere stock suficiente en el depósito central para TODOS los renglones.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE sp_procesar_transferencia(p_nro_transferencia INTEGER)
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
    v_estado     estado_documento;
    v_sala       INTEGER;
    v_disponible INTEGER;
    r            RECORD;
BEGIN
    SELECT t.estado, t.id_sala INTO v_estado, v_sala
      FROM transferencia t
     WHERE t.nro_transferencia = p_nro_transferencia
       FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'La transferencia % no existe', p_nro_transferencia
            USING ERRCODE = 'no_data_found';
    END IF;

    IF v_estado <> 'terminado' THEN
        RAISE EXCEPTION 'Solo una transferencia terminada puede procesarse; la transferencia % esta %',
            p_nro_transferencia, v_estado
            USING ERRCODE = 'RN011';   -- RN-11
    END IF;

    FOR r IN
        SELECT rt.cod_vino, rt.cantidad
          FROM renglon_transferencia rt
         WHERE rt.nro_transferencia = p_nro_transferencia
         ORDER BY rt.cod_vino
    LOOP
        SELECT d.cantidad INTO v_disponible
          FROM stock_deposito d
         WHERE d.cod_vino = r.cod_vino
           FOR UPDATE;

        IF NOT FOUND OR v_disponible < r.cantidad THEN
            RAISE EXCEPTION 'Stock insuficiente en el deposito central del vino %: pedido %, disponible %',
                r.cod_vino, r.cantidad, COALESCE(v_disponible, 0)
                USING ERRCODE = 'RN011';
        END IF;

        UPDATE stock_deposito
           SET cantidad = cantidad - r.cantidad
         WHERE cod_vino = r.cod_vino;

        INSERT INTO stock_sala AS s (id_sala, cod_vino, cantidad)
        VALUES (v_sala, r.cod_vino, r.cantidad)
        ON CONFLICT (id_sala, cod_vino)
        DO UPDATE SET cantidad = s.cantidad + EXCLUDED.cantidad;
    END LOOP;

    PERFORM set_config('atuel.sp_activo', 'on', true);
    UPDATE transferencia SET estado = 'procesado' WHERE nro_transferencia = p_nro_transferencia;
    PERFORM set_config('atuel.sp_activo', 'off', true);
END;
$$;

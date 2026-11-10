-- =============================================================================
-- 005_triggers.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Lógica en la base)
-- Triggers que garantizan las reglas de negocio dentro de la base.
--
-- Códigos de error propios (SQLSTATE de clase 'RN'). La API los traduce a HTTP:
--   RN005  suma del corte != 100            -> 422
--   RN006  cliente sin fila de subtipo      -> 422
--   RN008  importe/renglon de venta no editable a mano -> 409
--   RN009  stock insuficiente en la sala    -> 409
--   RN010  transicion o edicion invalida de un ingreso -> 409
--   RN011  transicion o edicion invalida de una transferencia, o
--          stock insuficiente en el deposito central   -> 409
--   RN012  renglones de un documento que no esta en confeccion -> 409
--
-- Resumen:
--   Constraint triggers diferidos : trg_cliente_subtipo, trg_vino_corte,
--                                   trg_composicion_corte           (RN-05, subtipos)
--   BEFORE : trg_cliente_descuento, trg_comprobante_importes, trg_renglon_calcula,
--            trg_renglon_valida_stock, trg_ingreso_estado, trg_transferencia_estado,
--            trg_renglon_ingreso_edicion, trg_renglon_transf_edicion
--   AFTER  : trg_renglon_descuenta_stock, trg_renglon_recalcula_comprobante,
--            trg_vino_audita_precio
-- Los BEFORE sobre el mismo evento se ejecutan en orden alfabetico del nombre.
-- =============================================================================

-- =============================================================================
-- Clientes
-- =============================================================================

-- RN-06 · El descuento se completa a partir del tipo si no se informa.
CREATE OR REPLACE FUNCTION fn_trg_cliente_descuento() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.descuento IS NULL THEN
        NEW.descuento := fn_descuento_tipo_cliente(NEW.tipo_cliente);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_cliente_descuento
    BEFORE INSERT ON cliente
    FOR EACH ROW EXECUTE FUNCTION fn_trg_cliente_descuento();

-- Jerarquia total: todo cliente debe tener su fila en el subtipo que declara.
-- Diferido: se valida al COMMIT, para poder insertar supertipo y subtipo juntos.
CREATE OR REPLACE FUNCTION fn_trg_cliente_subtipo() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_existe BOOLEAN;
BEGIN
    SELECT CASE NEW.tipo_cliente
               WHEN 'socio'        THEN EXISTS (SELECT 1 FROM socio        WHERE id_cliente = NEW.id_cliente)
               WHEN 'distribuidor' THEN EXISTS (SELECT 1 FROM distribuidor WHERE id_cliente = NEW.id_cliente)
               WHEN 'exportador'   THEN EXISTS (SELECT 1 FROM exportador   WHERE id_cliente = NEW.id_cliente)
           END
      INTO v_existe;

    -- Si el cliente fue borrado en la misma transaccion, no hay nada que validar.
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE id_cliente = NEW.id_cliente) THEN
        RETURN NULL;
    END IF;

    IF v_existe IS NOT TRUE THEN
        RAISE EXCEPTION 'El cliente % es de tipo % pero no tiene su fila en la tabla del subtipo',
            NEW.id_cliente, NEW.tipo_cliente
            USING ERRCODE = 'RN006';
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_cliente_subtipo
    AFTER INSERT ON cliente
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION fn_trg_cliente_subtipo();

-- =============================================================================
-- Vinos
-- =============================================================================

-- RN-05 · Los porcentajes del corte suman exactamente 100.
-- Se dispara por cambios en composicion y tambien al crear un vino, para que no
-- exista un vino sin corte. Diferido: el corte se carga en varias filas.
CREATE OR REPLACE FUNCTION fn_trg_corte_100() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_vino  INTEGER;
    v_suma  NUMERIC;
BEGIN
    FOR v_vino IN
        SELECT DISTINCT x FROM (VALUES
            (CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW.cod_vino END),
            (CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN OLD.cod_vino END)
        ) AS t(x) WHERE x IS NOT NULL
    LOOP
        -- Un vino borrado en la misma transaccion (cascada) ya no se valida.
        CONTINUE WHEN NOT EXISTS (SELECT 1 FROM vino WHERE cod_vino = v_vino);

        v_suma := fn_suma_composicion(v_vino);
        IF v_suma <> 100 THEN
            RAISE EXCEPTION 'El corte del vino % suma % y debe sumar exactamente 100 (RN-05)',
                v_vino, v_suma
                USING ERRCODE = 'RN005';
        END IF;
    END LOOP;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER trg_composicion_corte
    AFTER INSERT OR UPDATE OR DELETE ON composicion
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION fn_trg_corte_100();

CREATE CONSTRAINT TRIGGER trg_vino_corte
    AFTER INSERT ON vino
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION fn_trg_corte_100();

-- RN-13 · Todo cambio de precio queda auditado (fecha, usuario, anterior, nuevo).
-- SECURITY DEFINER: quien cambia el precio no necesita (ni debe tener) permiso
-- de escritura sobre la tabla de auditoria.
CREATE OR REPLACE FUNCTION fn_trg_vino_audita_precio() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
BEGIN
    INSERT INTO auditoria_precio (cod_vino, precio_anterior, precio_nuevo, usuario)
    VALUES (NEW.cod_vino, OLD.precio, NEW.precio, session_user);
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_vino_audita_precio
    AFTER UPDATE OF precio ON vino
    FOR EACH ROW
    WHEN (OLD.precio IS DISTINCT FROM NEW.precio)
    EXECUTE FUNCTION fn_trg_vino_audita_precio();

-- =============================================================================
-- Ventas: comprobante y renglones (RN-06, RN-08, RN-09)
-- =============================================================================

-- RN-08 · Los importes del comprobante no se cargan a mano: siempre salen de
-- sus renglones (fn_calcular_comprobante).
CREATE OR REPLACE FUNCTION fn_trg_comprobante_importes() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_calc RECORD;
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.subtotal := 0; NEW.descuento := 0; NEW.total := 0;   -- sin renglones todavia
        RETURN NEW;
    END IF;

    IF NEW.id_sala <> OLD.id_sala
       AND EXISTS (SELECT 1 FROM renglon_comprobante WHERE nro_comprobante = OLD.nro_comprobante) THEN
        RAISE EXCEPTION 'No se puede cambiar la sala de un comprobante que ya tiene renglones (el stock ya se desconto)'
            USING ERRCODE = 'RN008';
    END IF;

    SELECT * INTO v_calc FROM fn_calcular_comprobante(OLD.nro_comprobante);
    NEW.subtotal  := v_calc.subtotal_bruto;
    NEW.descuento := v_calc.monto_descuento;
    NEW.total     := v_calc.total;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_comprobante_importes
    BEFORE INSERT OR UPDATE ON comprobante
    FOR EACH ROW EXECUTE FUNCTION fn_trg_comprobante_importes();

-- RN-06 / RN-08 · El renglon toma el precio vigente del vino y el descuento del
-- cliente al momento de la venta; el subtotal lo calcula la base.
-- En UPDATE no se puede cambiar el vino ni la cantidad (ya descontaron stock).
CREATE OR REPLACE FUNCTION fn_trg_renglon_calcula() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_precio    NUMERIC(10,2);
    v_id_cli    INTEGER;
BEGIN
    IF TG_OP = 'INSERT' THEN
        SELECT v.precio INTO v_precio FROM vino v WHERE v.cod_vino = NEW.cod_vino;
        SELECT c.id_cliente INTO v_id_cli FROM comprobante c WHERE c.nro_comprobante = NEW.nro_comprobante;
        -- Si el vino o el comprobante no existen, se deja pasar: la FK informa el error.
        IF v_precio IS NOT NULL AND v_id_cli IS NOT NULL THEN
            NEW.precio_unitario := v_precio;
            NEW.descuento_pct   := fn_descuento_cliente(v_id_cli);
        END IF;
    ELSE
        IF NEW.cod_vino <> OLD.cod_vino
           OR NEW.cantidad <> OLD.cantidad
           OR NEW.nro_comprobante <> OLD.nro_comprobante THEN
            RAISE EXCEPTION 'Un renglon de venta no puede cambiar de comprobante, vino ni cantidad: elimine y cargue otro'
                USING ERRCODE = 'RN008';
        END IF;
    END IF;

    NEW.subtotal := fn_subtotal_renglon(NEW.cantidad, NEW.precio_unitario, NEW.descuento_pct);
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_renglon_calcula
    BEFORE INSERT OR UPDATE ON renglon_comprobante
    FOR EACH ROW EXECUTE FUNCTION fn_trg_renglon_calcula();

-- (SECURITY DEFINER: el rol de la API no escribe stock_sala directamente; el
-- bloqueo FOR UPDATE y el descuento los hace el trigger con privilegios del propietario.)
-- RN-09 · No se vende mas de lo que hay en la sala. Se bloquea la fila de stock
-- (FOR UPDATE) antes de leerla: dos ventas simultaneas del mismo vino en la misma
-- sala se serializan y la segunda ve el stock ya descontado por la primera.
CREATE OR REPLACE FUNCTION trg_validar_stock_venta() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
DECLARE
    v_sala INTEGER;
BEGIN
    SELECT id_sala INTO v_sala FROM comprobante WHERE nro_comprobante = NEW.nro_comprobante;
    IF NOT FOUND OR NOT EXISTS (SELECT 1 FROM vino WHERE cod_vino = NEW.cod_vino) THEN
        RETURN NEW;   -- comprobante o vino inexistente: la FK informa el error (no es un problema de stock)
    END IF;

    PERFORM 1 FROM stock_sala
     WHERE id_sala = v_sala AND cod_vino = NEW.cod_vino
       FOR UPDATE;

    IF fn_stock_sala(v_sala, NEW.cod_vino) < NEW.cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente del vino % en la sala %: pedido %, disponible % (RN-09)',
            NEW.cod_vino, v_sala, NEW.cantidad, fn_stock_sala(v_sala, NEW.cod_vino)
            USING ERRCODE = 'RN009';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_renglon_valida_stock
    BEFORE INSERT ON renglon_comprobante
    FOR EACH ROW EXECUTE FUNCTION trg_validar_stock_venta();

-- La venta descuenta el stock de la sala. Borrar un renglon NO lo devuelve: la
-- baja de comprobantes viejos (consulta D1) no debe regenerar stock.
CREATE OR REPLACE FUNCTION fn_trg_renglon_descuenta_stock() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
BEGIN
    UPDATE stock_sala s
       SET cantidad = s.cantidad - NEW.cantidad
      FROM comprobante c
     WHERE c.nro_comprobante = NEW.nro_comprobante
       AND s.id_sala = c.id_sala
       AND s.cod_vino = NEW.cod_vino;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_renglon_descuenta_stock
    AFTER INSERT ON renglon_comprobante
    FOR EACH ROW EXECUTE FUNCTION fn_trg_renglon_descuenta_stock();

-- RN-08 · Cada cambio de renglones "toca" el comprobante: su trigger BEFORE
-- UPDATE recalcula subtotal, descuento y total.
CREATE OR REPLACE FUNCTION fn_trg_renglon_recalcula_comprobante() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE comprobante
       SET subtotal = subtotal
     WHERE nro_comprobante = CASE WHEN TG_OP = 'DELETE' THEN OLD.nro_comprobante
                                  ELSE NEW.nro_comprobante END;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_renglon_recalcula_comprobante
    AFTER INSERT OR UPDATE OR DELETE ON renglon_comprobante
    FOR EACH ROW EXECUTE FUNCTION fn_trg_renglon_recalcula_comprobante();

-- =============================================================================
-- Ingresos y transferencias (RN-10, RN-11, RN-12)
-- =============================================================================

-- RN-10 · Estados del ingreso:
--   * nace 'en_confeccion';
--   * fuera de confeccion la cabecera no se edita (solo cambia el estado);
--   * transiciones validas: en_confeccion -> terminado -> procesado;
--   * no se termina un ingreso sin renglones;
--   * 'procesado' solo lo fija sp_procesar_ingreso (indicador atuel.sp_activo).
CREATE OR REPLACE FUNCTION fn_trg_ingreso_estado() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'Un ingreso debe crearse en_confeccion (se intento crear %)', NEW.estado
                USING ERRCODE = 'RN010';
        END IF;
        RETURN NEW;
    END IF;

    IF NEW.estado = OLD.estado THEN
        IF OLD.estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'El ingreso % esta % y no admite modificaciones', OLD.cod_ingreso, OLD.estado
                USING ERRCODE = 'RN010';
        END IF;
        RETURN NEW;
    END IF;

    IF NOT fn_transicion_estado_valida(OLD.estado, NEW.estado) THEN
        RAISE EXCEPTION 'Transicion invalida del ingreso %: % -> %', OLD.cod_ingreso, OLD.estado, NEW.estado
            USING ERRCODE = 'RN010';
    END IF;

    IF NEW.estado = 'terminado'
       AND NOT EXISTS (SELECT 1 FROM renglon_ingreso WHERE cod_ingreso = OLD.cod_ingreso) THEN
        RAISE EXCEPTION 'No se puede terminar el ingreso % porque no tiene renglones', OLD.cod_ingreso
            USING ERRCODE = 'RN010';
    END IF;

    IF NEW.estado = 'procesado'
       AND current_setting('atuel.sp_activo', true) IS DISTINCT FROM 'on' THEN
        RAISE EXCEPTION 'Un ingreso solo se procesa con CALL sp_procesar_ingreso(%)', OLD.cod_ingreso
            USING ERRCODE = 'RN010';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_ingreso_estado
    BEFORE INSERT OR UPDATE ON ingreso
    FOR EACH ROW EXECUTE FUNCTION fn_trg_ingreso_estado();

-- RN-11 · Igual que el ingreso, mas: la fecha de confeccion es la fecha actual
-- (se ignora lo que se informe) y no se puede modificar.
CREATE OR REPLACE FUNCTION fn_trg_transferencia_estado() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'Una transferencia debe crearse en_confeccion (se intento crear %)', NEW.estado
                USING ERRCODE = 'RN011';
        END IF;
        NEW.fecha_confeccion := CURRENT_DATE;
        RETURN NEW;
    END IF;

    IF NEW.fecha_confeccion IS DISTINCT FROM OLD.fecha_confeccion THEN
        RAISE EXCEPTION 'La fecha de confeccion de la transferencia % no se puede modificar', OLD.nro_transferencia
            USING ERRCODE = 'RN011';
    END IF;

    IF NEW.estado = OLD.estado THEN
        IF OLD.estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'La transferencia % esta % y no admite modificaciones', OLD.nro_transferencia, OLD.estado
                USING ERRCODE = 'RN011';
        END IF;
        RETURN NEW;
    END IF;

    IF NOT fn_transicion_estado_valida(OLD.estado, NEW.estado) THEN
        RAISE EXCEPTION 'Transicion invalida de la transferencia %: % -> %',
            OLD.nro_transferencia, OLD.estado, NEW.estado
            USING ERRCODE = 'RN011';
    END IF;

    IF NEW.estado = 'terminado'
       AND NOT EXISTS (SELECT 1 FROM renglon_transferencia WHERE nro_transferencia = OLD.nro_transferencia) THEN
        RAISE EXCEPTION 'No se puede terminar la transferencia % porque no tiene renglones', OLD.nro_transferencia
            USING ERRCODE = 'RN011';
    END IF;

    IF NEW.estado = 'procesado'
       AND current_setting('atuel.sp_activo', true) IS DISTINCT FROM 'on' THEN
        RAISE EXCEPTION 'Una transferencia solo se procesa con CALL sp_procesar_transferencia(%)', OLD.nro_transferencia
            USING ERRCODE = 'RN011';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_transferencia_estado
    BEFORE INSERT OR UPDATE ON transferencia
    FOR EACH ROW EXECUTE FUNCTION fn_trg_transferencia_estado();

-- RN-12 · Un documento que no esta en confeccion no admite agregar, modificar
-- ni quitar renglones. FOR SHARE sobre la cabecera evita que cambie de estado
-- mientras se edita. Si la cabecera ya no existe (borrado en cascada) se permite.
CREATE OR REPLACE FUNCTION fn_trg_renglon_ingreso_edicion() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_cod    INTEGER;
    v_estado estado_documento;
BEGIN
    FOR v_cod IN
        SELECT DISTINCT x FROM (VALUES
            (CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW.cod_ingreso END),
            (CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN OLD.cod_ingreso END)
        ) AS t(x) WHERE x IS NOT NULL
    LOOP
        SELECT estado INTO v_estado FROM ingreso WHERE cod_ingreso = v_cod FOR SHARE;
        IF FOUND AND v_estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'El ingreso % esta %: no admite agregar, modificar ni quitar renglones (RN-12)',
                v_cod, v_estado
                USING ERRCODE = 'RN012';
        END IF;
    END LOOP;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER trg_renglon_ingreso_edicion
    BEFORE INSERT OR UPDATE OR DELETE ON renglon_ingreso
    FOR EACH ROW EXECUTE FUNCTION fn_trg_renglon_ingreso_edicion();

CREATE OR REPLACE FUNCTION fn_trg_renglon_transf_edicion() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE
    v_nro    INTEGER;
    v_estado estado_documento;
BEGIN
    FOR v_nro IN
        SELECT DISTINCT x FROM (VALUES
            (CASE WHEN TG_OP = 'DELETE' THEN NULL ELSE NEW.nro_transferencia END),
            (CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN OLD.nro_transferencia END)
        ) AS t(x) WHERE x IS NOT NULL
    LOOP
        SELECT estado INTO v_estado FROM transferencia WHERE nro_transferencia = v_nro FOR SHARE;
        IF FOUND AND v_estado <> 'en_confeccion' THEN
            RAISE EXCEPTION 'La transferencia % esta %: no admite agregar, modificar ni quitar renglones (RN-12)',
                v_nro, v_estado
                USING ERRCODE = 'RN012';
        END IF;
    END LOOP;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER trg_renglon_transf_edicion
    BEFORE INSERT OR UPDATE OR DELETE ON renglon_transferencia
    FOR EACH ROW EXECUTE FUNCTION fn_trg_renglon_transf_edicion();

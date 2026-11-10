-- =============================================================================
-- 006_vistas.sql  ·  Bodegas del Atuel  ·  Etapa 2 (Lógica en la base)
-- Vistas para el catálogo, el stock y los reportes. Las consume la API y el
-- tablero del front: ninguna lógica de cálculo vive en el cliente.
--   v_stock_vino              stock de depósito + salas por vino
--   v_catalogo_vino           ficha de catálogo (bodega, corte, stock)
--   v_comprobante_detalle     ventas con cliente, sala y cantidades
--   mv_ventas_mensuales_sala  MATERIALIZADA: ventas por mes y sala
--   sp_refrescar_reportes()   procedimiento para refrescar la materializada
-- =============================================================================

-- Stock por vino: depósito central, suma de todas las salas y total.
CREATE VIEW v_stock_vino AS
SELECT v.cod_vino,
       v.nombre,
       v.tipo,
       v.anada,
       v.volumen_ml,
       COALESCE(d.cantidad, 0)                              AS stock_deposito,
       COALESCE(s.total, 0)                                 AS stock_salas,
       COALESCE(d.cantidad, 0) + COALESCE(s.total, 0)       AS stock_total
  FROM vino v
  LEFT JOIN stock_deposito d ON d.cod_vino = v.cod_vino
  LEFT JOIN (SELECT cod_vino, SUM(cantidad)::BIGINT AS total
               FROM stock_sala
              GROUP BY cod_vino) s ON s.cod_vino = v.cod_vino;

-- Catálogo: lo que muestra la pantalla de vinos (con el corte ya armado).
CREATE VIEW v_catalogo_vino AS
SELECT v.cod_vino,
       v.nombre,
       v.tipo,
       v.anada,
       v.volumen_ml,
       v.graduacion,
       v.precio,
       b.razon_social AS bodega,
       (SELECT string_agg(c.nombre || ' ' || trim_scale(co.porcentaje)::TEXT || '%',
                          ', ' ORDER BY co.porcentaje DESC, c.nombre)
          FROM composicion co
          JOIN cepa c ON c.id_cepa = co.id_cepa
         WHERE co.cod_vino = v.cod_vino)                    AS corte,
       st.stock_deposito,
       st.stock_salas,
       st.stock_total
  FROM vino v
  JOIN bodega b       ON b.cuit = v.cuit_bodega
  JOIN v_stock_vino st ON st.cod_vino = v.cod_vino;

-- Comprobantes con sus datos de cliente y sala, para listados y reportes.
CREATE VIEW v_comprobante_detalle AS
SELECT c.nro_comprobante,
       c.fecha,
       cl.id_cliente,
       cl.nombre_razon_social AS cliente,
       cl.tipo_cliente,
       s.id_sala,
       s.calle || ' ' || s.numero AS sala,
       l.nombre               AS localidad_sala,
       c.subtotal,
       c.descuento,
       c.total,
       COALESCE(r.renglones, 0) AS renglones,
       COALESCE(r.unidades, 0)  AS unidades
  FROM comprobante c
  JOIN cliente cl    ON cl.id_cliente = c.id_cliente
  JOIN sala_venta s  ON s.id_sala = c.id_sala
  JOIN localidad l   ON l.cod_postal = s.cod_postal
  LEFT JOIN (SELECT nro_comprobante,
                    COUNT(*)::INTEGER       AS renglones,
                    SUM(cantidad)::BIGINT   AS unidades
               FROM renglon_comprobante
              GROUP BY nro_comprobante) r ON r.nro_comprobante = c.nro_comprobante;

-- Ventas por mes y sala. Es MATERIALIZADA porque agrega todo el historial de
-- renglones (la tabla más grande) y el tablero la consulta seguido; se actualiza
-- con REFRESH MATERIALIZED VIEW CONCURRENTLY mv_ventas_mensuales_sala
-- (CONCURRENTLY exige el índice único de abajo y no bloquea las lecturas).
CREATE MATERIALIZED VIEW mv_ventas_mensuales_sala AS
SELECT date_trunc('month', c.fecha)::DATE      AS mes,
       c.id_sala,
       COUNT(DISTINCT c.nro_comprobante)       AS comprobantes,
       SUM(r.cantidad)::BIGINT                 AS unidades,
       SUM(r.subtotal)::NUMERIC(16,2)          AS total_vendido
  FROM comprobante c
  JOIN renglon_comprobante r ON r.nro_comprobante = c.nro_comprobante
 GROUP BY date_trunc('month', c.fecha), c.id_sala
WITH DATA;

CREATE UNIQUE INDEX uq_mv_ventas_mensuales_sala ON mv_ventas_mensuales_sala (mes, id_sala);

-- Solo el propietario puede refrescar una vista materializada. Este procedimiento
-- (SECURITY DEFINER) deja que la API pida el refresco sin darle ese privilegio.
CREATE PROCEDURE sp_refrescar_reportes()
LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_ventas_mensuales_sala;
END;
$$;

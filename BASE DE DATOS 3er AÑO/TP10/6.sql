-- Implementa una vista materializada a partir de la vista vista_precios_fabricante
CREATE MATERIALIZED VIEW mv_precios_fabricante AS
SELECT *
FROM vista_precios_fabricante;
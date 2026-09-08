-- Crea una vista materializada llamada mis_productos_destacados a partir de la vista vista_productos_destacados.
CREATE MATERIALIZED VIEW mis_productos_destacados AS
SELECT *
FROM vista_productos_destacados
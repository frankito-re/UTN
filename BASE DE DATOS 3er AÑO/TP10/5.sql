-- Genera  una  vista  llamada  vista_precios_fabricante  que  muestre,  para  cada  fabricante,  el  total  y  el promedio de precio de sus productos.
CREATE OR REPLACE VIEW vista_precios_fabricante AS
SELECT
    f.nombre AS fabricante,
    SUM(p.precio) AS total_precio,
    AVG(p.precio) AS promedio_precio
FROM fabricante f
    LEFT JOIN producto p ON f.codigo = p.codigo_fabricante
GROUP BY
    f.codigo,
    f.nombre;
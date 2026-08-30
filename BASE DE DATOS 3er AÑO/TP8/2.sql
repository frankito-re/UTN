-- Obtener el precio promedio de los productos agrupados por cada código de fabricante.
SELECT
    codigo_fabricante,
    AVG(precio) AS precio_promedio
FROM producto
GROUP BY
    codigo_fabricante;
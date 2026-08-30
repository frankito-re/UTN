-- Obtener un listado con la cantidad de productos que tiene cada fabricante.
SELECT
    codigo_fabricante,
    count(nombre) AS cantidad_productos
FROM producto
GROUP BY
    codigo_fabricante
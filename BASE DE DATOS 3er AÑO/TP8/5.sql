-- Obtener el código de cada fabricante y la cantidad de productos que posee, evaluando únicamente los productos de más de $30.000 y mostrando solo los fabricantes que tengan más de 2 productos en esa categoría.
SELECT
    codigo_fabricante,
    count(nombre) AS cantidad_productos
FROM producto
WHERE
    precio >= 30000
GROUP BY
    codigo_fabricante
HAVING
    count(nombre) > 2;
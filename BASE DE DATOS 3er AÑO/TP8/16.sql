-- Obtener un listado de los fabricantes que tienen más de 2 productos asociados, junto con la cantidad de productos de cada uno.
SELECT f.nombre, count(p.nombre) AS cantidad_productos
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
GROUP BY
    f.nombre
HAVING
    count(p.nombre) >= 2

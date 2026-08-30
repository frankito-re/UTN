-- Obtener un listado con el identificador y el nombre de fabricante, solamente de aquellos fabricantes que tienen productos asociados en la base de datos.
SELECT p.codigo_fabricante, f.nombre, count(p.nombre) AS cantidad_productos
FROM
    producto as p
    JOIN fabricante f ON codigo_fabricante = f.codigo
GROUP BY
    p.codigo_fabricante,
    f.nombre
HAVING
    count(p.nombre) > 0
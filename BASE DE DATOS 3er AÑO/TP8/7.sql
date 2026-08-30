-- Obtener una lista con el nombre del producto, precio y nombre de fabricante de todos los productos de la base de datos cuyo precio supere los 70000.
SELECT p.nombre, p.precio, f.nombre AS nombre_fabricante
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
WHERE
    p.precio >= 70000
ORDER BY f.nombre;
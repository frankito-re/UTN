-- Obtener una lista de todos los productos del fabricante Acer que tengan un precio mayor que 200.000.
SELECT p.nombre, p.precio, f.nombre AS nombre_fabricante
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
WHERE
    f.nombre = 'Acer'
    AND precio >= 200000
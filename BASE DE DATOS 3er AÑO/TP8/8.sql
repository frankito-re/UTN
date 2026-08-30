-- Obtener una lista de todos los productos del fabricante Lenovo.
SELECT p.nombre, p.precio, f.nombre AS nombre_fabricante
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
WHERE
    f.nombre = 'Lenovo'
-- Obtener un listado con el nombre de producto, precio y nombre de fabricante, de todos los productos que tengan un precio mayor o igual a 180.000. Ordene el resultado en primer lugar por el precio (en orden descendente) y en segundo lugar por el nombre del fabricante (en orden ascendente)
SELECT p.nombre, p.precio, f.nombre AS nombre_fabricante
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
WHERE
    p.precio >= 180000
ORDER BY p.precio DESC, f.nombre ASC
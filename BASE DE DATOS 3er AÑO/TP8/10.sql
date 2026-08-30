-- Obtener un listado con todos los productos de los fabricantes Asus, HP y Dell. Sin utilizar el operador IN.
SELECT p.nombre, p.precio, f.nombre AS nombre_fabricante
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
WHERE
    f.nombre = 'Asus'
    OR f.nombre = 'HP'
    OR f.nombre = 'Dell'
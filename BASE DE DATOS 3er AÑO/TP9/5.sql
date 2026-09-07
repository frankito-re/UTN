-- Lista los nombres  de los productos del fabricante Asus, junto con los nombres de todos los productos con precio mayor a 300.000.
SELECT p.nombre, p.codigo_fabricante
FROM producto p
    JOIN fabricante f ON p.codigo_fabricante = f.codigo
WHERE
    f.nombre = 'Asus'
UNION
SELECT nombre, codigo_fabricante
FROM producto
WHERE
    precio >= 300000
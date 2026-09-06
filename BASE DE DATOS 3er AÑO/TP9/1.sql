-- 1. Lista el precio medio de los productos de cada fabricante,  mostrando solamente el identificador  del fabricante.
SELECT
    codigo_fabricante,
    AVG(precio) as precio_promedio
FROM producto
GROUP BY
    codigo_fabricante
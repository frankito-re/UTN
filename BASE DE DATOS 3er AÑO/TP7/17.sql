-- Lista el nombre de todos los productos del fabricante cuyo identificador de fabricante es igual a 2.
SELECT nombre, codigo_fabricante
FROM producto
WHERE
    codigo_fabricante = 2
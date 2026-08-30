-- Lista todos los productos donde el identificador de fabricante sea 1, 3 o 5. Sin utilizar el operador IN.
SELECT nombre, codigo_fabricante
FROM producto
WHERE
    codigo_fabricante = 1
    OR codigo_fabricante = 3
    OR codigo_fabricante = 5
-- Lista el nombre  del producto  más caro del fabricante Lenovo.
SELECT nombre, precio
FROM producto
WHERE
    codigo_fabricante = (
        SELECT codigo
        FROM fabricante
        WHERE
            nombre = 'Lenovo'
    )
ORDER BY precio DESC
LIMIT 1;
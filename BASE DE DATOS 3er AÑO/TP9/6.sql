-- Devuelve  todos los productos  del  fabricante Lenovo. (Sin  utilizar  JOIN).
SELECT *
FROM producto
WHERE
    codigo_fabricante IN (
        SELECT codigo
        FROM fabricante
        WHERE
            nombre = 'Lenovo'
    )
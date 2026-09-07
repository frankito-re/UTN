-- Devuelve  todos los datos de los productos que  tienen el mismo precio que  el producto más caro del fabricante Lenovo. (Sin  utilizar  JOIN).
SELECT *
FROM producto
WHERE precio = (
    SELECT MAX(precio)
    FROM producto
    WHERE codigo_fabricante IN (
        SELECT codigo
        FROM fabricante
        WHERE nombre = 'Lenovo'
    )
)
-- Devuelve  todos los productos  de la base de datos que tienen  un precio mayor o igual al del producto  más caro del fabricante Lenovo.
SELECT *
FROM producto
WHERE
    precio >= (
        SELECT precio
        FROM producto
        WHERE
            codigo_fabricante = (
                SELECT codigo
                FROM fabricante
                WHERE
                    nombre = 'Lenovo'
            )
        ORDER BY precio DESC
        LIMIT 1
    )
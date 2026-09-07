-- Lista  todos  los  productos  del  fabricante  Asus  que  tienen  un  precio  superior  al  precio  medio  de  todos  sus productos.
SELECT *
FROM producto
WHERE
    precio >= (
        SELECT AVG(precio)
        FROM producto
        WHERE
            codigo_fabricante IN (
                SELECT codigo
                FROM fabricante
                WHERE
                    nombre = 'Lenovo'
            )
    )
-- Devuelve  los nombres  de los fabricantes que  no tienen  productos  asociados. (Utilizando  ALL o ANY).
SELECT nombre
FROM fabricante
WHERE
    codigo != ALL (
        SELECT codigo_fabricante
        FROM producto
    )
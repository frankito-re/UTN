-- Devuelve  los nombres  de los fabricantes que  no tienen  productos  asociados. (Utilizando   NOT IN).
SELECT nombre
FROM fabricante
WHERE
    codigo NOT IN (
        SELECT codigo_fabricante
        FROM producto
    )
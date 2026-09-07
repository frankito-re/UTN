-- Devuelve  los nombres  de los fabricantes que  tienen  productos asociados. (Utilizando  IN).
SELECT nombre
FROM fabricante
WHERE
    codigo IN (
        SELECT codigo_fabricante
        FROM producto
    )
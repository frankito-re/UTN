-- Devuelve  los nombres  de los fabricantes que  tienen  productos asociados. (Utilizando  ALL o ANY).
SELECT nombre
FROM fabricante
WHERE
    codigo = ANY (
        SELECT codigo_fabricante
        FROM producto
    )
-- Devuelve  los nombres  de los fabricantes que  tienen  productos asociados. (Utilizando  EXISTS).
SELECT nombre
FROM fabricante f
WHERE
    EXISTS (
        SELECT 1
        FROM producto p
        WHERE
            f.codigo = p.codigo_fabricante
    )
-- Devuelve  los nombres  de los fabricantes que  no tienen  productos  asociados. (Utilizando  NOT EXISTS).
SELECT nombre
FROM fabricante f
WHERE
    NOT EXISTS (
        SELECT 1
        FROM producto p
        WHERE
            f.codigo = p.codigo_fabricante
    )
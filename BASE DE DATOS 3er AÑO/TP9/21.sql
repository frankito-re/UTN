-- Devuelve  un  listado con los nombres  de los fabricantes  que tienen  2 o más productos.
SELECT f.nombre
FROM fabricante f
    INNER JOIN producto p ON f.codigo = p.codigo_fabricante
GROUP BY
    f.codigo,
    f.nombre
HAVING
    COUNT(p.codigo) >= 2;
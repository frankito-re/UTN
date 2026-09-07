-- Devuelve  un  listado con todos los nombres  de los fabricantes que  tienen  la misma  cantidad de  productos  que el fabricante  Lenovo. (requiere  una subconsulta  dentro  del HAVING).
SELECT f.nombre, count(p.nombre) AS cantidad_productos
FROM producto p
    JOIN fabricante f ON p.codigo_fabricante = f.codigo
GROUP BY
    f.nombre,
    f.codigo
HAVING
    count(p.nombre) = (
        SELECT count(p.nombre)
        FROM producto p
            JOIN fabricante f ON p.codigo_fabricante = f.codigo
        WHERE
            f.nombre = 'Lenovo'
    )
-- Devuelve  un  listado con los nombres  de  los fabricantes  y el  número  de  productos  que  tiene  cada uno  con un precio  superior o  igual  a  220000.  No  es  necesario  mostrar  el  nombre de  los  fabricantes  que  no  tienen productos  que cumplan  la condición.
SELECT f.nombre, COUNT(p.codigo) AS total
FROM fabricante f
    INNER JOIN producto p ON f.codigo = p.codigo_fabricante
WHERE
    p.precio >= 220000
GROUP BY
    f.codigo,
    f.nombre;
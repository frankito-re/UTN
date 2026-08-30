-- Obtener  el  código  de  fabricante  y  el  precio  promedio  de  sus  productos,  mostrando  únicamente  a aquellos fabricantes cuyo precio promedio sea superior a $100.000
SELECT
    codigo_fabricante,
    AVG(precio) AS precio_promedio
FROM producto
WHERE
    precio >= 100000
GROUP BY
    codigo_fabricante;
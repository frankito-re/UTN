-- Obtener  la  cantidad  de  productos  y  el  precio  máximo  de  cada  fabricante  (codigo_fabricante), considerando únicamente aquellos productos cuyo precio sea superior a $50.000.
SELECT
    codigo_fabricante,
    COUNT(nombre) AS cantidad_productos,
    MAX(precio) AS precio_maximo
FROM producto
WHERE
    precio >= 50000
GROUP BY
    codigo_fabricante;
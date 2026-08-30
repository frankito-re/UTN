-- Lista todos los productos que tengan un precio entre 80.000 y 300.000. Sin utilizar el operador BETWEEN.
SELECT nombre, precio
FROM producto
WHERE
    precio >= 80000
    AND precio <= 300000
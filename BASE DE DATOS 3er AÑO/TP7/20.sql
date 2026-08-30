-- Lista todos los productos que tengan un precio entre 60.000 y 200.000. Utilizando el operador BETWEEN.
SELECT nombre, precio
FROM producto
WHERE
    precio >= 60000
    AND precio <= 200000
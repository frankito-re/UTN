-- Lista el nombre de los productos, el precio en pesos y el precio en dólares. Considerá una cotización de 1 USD = 1515 ARS.
SELECT nombre, precio, ROUND(precio / 1525, 2) AS precio_dolares
FROM producto
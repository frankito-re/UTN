-- Obtener el precio promedio, el precio máximo y el precio mínimo de todos los productos almacenados en la base de datos.
SELECT
    AVG(precio) AS precio_promedio,
    MAX(precio) AS precio_maximo,
    MIN(precio) AS precio_minimo
FROM producto;
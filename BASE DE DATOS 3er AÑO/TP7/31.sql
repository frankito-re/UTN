-- Indica el precio del producto más barato y el precio del producto más caro, en una misma consulta. (Utilice MIN y MAX)
SELECT
    MIN(precio) AS precio_minimo,
    MAX(precio) AS precio_maximo
FROM producto;
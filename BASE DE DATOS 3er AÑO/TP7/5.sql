-- Lista el nombre de los productos, el precio en pesos y el precio en dólares (misma cotización que el ejercicio anterior). Utiliza los siguientes alias para las columnas: nombre_producto, precio_pesos, precio_dolares.
SELECT
    nombre AS nombre_producto,
    precio AS precio_pesos,
    ROUND(precio / 1525, 2) AS precio_dolares
FROM producto
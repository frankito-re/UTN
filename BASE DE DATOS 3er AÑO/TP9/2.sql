-- Muestra el precio máximo, precio mínimo, precio medio y el número  total de productos que tiene el fabricante.
SELECT
    codigo_fabricante,
    MAX(precio) as precio_maximo,
    MIN(precio) as precio_minimo,
    AVG(precio) as precio_promedio,
    COUNT(*) as total_productos
FROM producto
GROUP BY
    codigo_fabricante
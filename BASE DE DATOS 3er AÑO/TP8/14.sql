-- Listar todos los productos junto con el nombre del fabricante, incluyendo aquellos productos que no tienen fabricante asociado (usando LEFT JOIN).
SELECT p.nombre, f.nombre AS nombre_fabricante
FROM fabricante f
    LEFT JOIN producto p ON f.codigo = p.codigo_fabricante
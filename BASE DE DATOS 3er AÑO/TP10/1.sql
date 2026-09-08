-- Genera una vista llamada vista_productos_completa que muestre una lista completa de productos con el nombre del fabricante y el stock, para evitar tener que escribir el JOIN cada vez que se necesite esta información.
CREATE OR REPLACE VIEW vista_productos_completa AS
SELECT p.codigo, p.nombre AS producto, p.precio, p.stock, f.nombre AS fabricante
FROM producto p
    JOIN fabricante f ON p.codigo_fabricante = f.codigo
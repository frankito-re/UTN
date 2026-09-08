-- Crea una vista llamada vista_productos_destacados que muestre los productos cuyo precio sea superior al precio promedio de los productos de su propio fabricante.
CREATE OR REPLACE VIEW vista_productos_destacados AS
SELECT p.codigo, p.nombre, p.precio, p.stock, p.codigo_fabricante
FROM producto p
WHERE
    p.precio > (
        SELECT AVG(p2.precio)
        FROM producto p2
        WHERE
            p2.codigo_fabricante = p.codigo_fabricante
    );
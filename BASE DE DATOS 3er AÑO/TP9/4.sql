-- Lista  un  listado  combinado  con  el  nombre,  precio  y  una  columna  categoria  que  diga  'premium' para  los productos con precio mayor  a 500.000,  y  'económico'  para  los  que  tengan  precio  menor  a  50.000.  Ordená  primero  por categoría y después  por precio descendente.
SELECT
    nombre,
    precio,
    CASE
        WHEN precio > 500000 THEN 'premium'
        WHEN precio < 50000 THEN 'económico'
    END AS categoria
FROM producto
ORDER BY categoria, precio DESC
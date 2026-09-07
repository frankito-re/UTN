-- Muestra  el nombre  de  cada fabricante, junto  con el precio máximo, precio mínimo,  precio medio  y el número  total de productos, de los fabricantes  que tienen  un  precio medio superior  a 200.000.
SELECT
    f.nombre,
    max(p.precio) as precio_maximo,
    min(p.precio) as precio_minimo,
    avg(p.precio) as precio_promedio,
    count(p.codigo) as cantidad_productos -- Es una mejor práctica contar por clave primaria
FROM producto p
    JOIN fabricante f ON p.codigo_fabricante = f.codigo
GROUP BY
    f.codigo,
    f.nombre -- Agrupar por la clave primaria y el nombre evita errores
HAVING
    avg(p.precio) > 200000;
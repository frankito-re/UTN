-- Crea una vista llamada vista_estado_fabricantes que muestre el nombre de cada fabricante junto con una columna estado, indicando 'con productos' o 'sin productos' según corresponda, combinando dos SELECT con UNION ALL.
CREATE or replace view vista_estado_fabricantes as
SELECT
    f.nombre,
    case
        when count(p.nombre) > 0 then 'Con productos'
        when count(p.nombre) = 0 then 'Sin productos'
    END AS estado
FROM producto p
    JOIN fabricante f on p.codigo_fabricante = f.codigo
GROUP BY
    f.nombre,
    f.codigo
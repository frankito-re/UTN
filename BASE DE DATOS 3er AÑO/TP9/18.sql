-- Devuelve  un  listado  con el  nombre  del  producto  más caro que  tiene  cada fabricante.  El resultado  debe  tener tres  columnas:  nombre  del  producto,  precio  y nombre  del  fabricante.  El resultado  tiene  que  estar  ordenado alfabéticamente  de menor a mayor por el nombre  del fabricante.
SELECT p1.nombre, p1.precio, f.nombre
FROM producto p1
    JOIN fabricante f ON p1.codigo_fabricante = f.codigo
WHERE
    p1.precio = (
        SELECT max(p2.precio)
        FROM producto p2
        WHERE
            p2.codigo_fabricante = p1.codigo_fabricante
    )
-- Muestra  el número  total de productos  que  tiene  cada uno  de  los fabricantes.  El listado  también  debe  incluir los  fabricantes  que  no  tienen  ningún  producto.  El  resultado  mostrará  dos  columnas,  una  con  el nombre  del fabricante y otra con el número de productos  que tiene. Ordene el resultado descendentemente  por el número  de productos.
SELECT
    f.nombre AS nombre_fabricante,
    count(p.nombre) AS cantidad_productos
FROM
    producto p
    JOIN fabricante f ON codigo_fabricante = f.codigo
GROUP BY
    f.nombre
ORDER BY count(p.nombre) DESC
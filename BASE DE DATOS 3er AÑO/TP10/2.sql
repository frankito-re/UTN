-- Crea  una  vista  llamada  vista_fabricantes_resumen  que  muestre,  para  cada  fabricante,  la  cantidad  de productos que tiene asociados — incluyendo los fabricantes que no tienen ningún producto
CREATE OR replace VIEW vista_fabricantes_resumen AS
SELECT f.nombre, count(p.nombre) AS cantidad_productos
FROM producto p
    JOIN fabricante f ON p.codigo_fabricante = f.codigo
GROUP BY
    f.nombre,
    f.codigo
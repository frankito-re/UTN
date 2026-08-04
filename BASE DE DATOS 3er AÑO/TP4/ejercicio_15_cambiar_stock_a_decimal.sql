-- EJERCICIO 15: Cambiar tipo de dato de columna "stock" en tabla "Producto"
-- Cambiar el tipo de dato de la columna "stock" en la tabla "Producto" de "entero" a "decimal".

ALTER TABLE Producto
ALTER COLUMN stock TYPE DECIMAL(10, 2);

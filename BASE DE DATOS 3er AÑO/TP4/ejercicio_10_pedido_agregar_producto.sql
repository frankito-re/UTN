-- EJERCICIO 10: Agregar columna "id_producto" a tabla "Pedido"
-- Agregar una nueva columna llamada "id_producto" (entero) a la tabla "Pedido".

ALTER TABLE Pedido
ADD COLUMN id_producto INTEGER;

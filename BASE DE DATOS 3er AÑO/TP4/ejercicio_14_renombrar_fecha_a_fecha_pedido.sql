-- EJERCICIO 14: Renombrar columna "fecha" a "fecha_pedido" en tabla "Pedido"
-- Renombrar la columna "fecha" en la tabla "Pedido" a "fecha_pedido".

ALTER TABLE Pedido
RENAME COLUMN fecha TO fecha_pedido;

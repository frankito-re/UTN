-- EJERCICIO 12: Eliminar clave foránea "id_cliente" de tabla "Pedido"
-- Eliminar la clave foránea "id_cliente" de la tabla "Pedido".

ALTER TABLE Pedido
DROP CONSTRAINT fk_pedido_cliente;

-- EJERCICIO 11: Agregar clave foránea en tabla "Pedido" que referencia "Producto"
-- Agregar una clave foránea en la tabla "Pedido" que haga referencia al "id" de la tabla "Producto"
-- utilizando la columna "id_producto".

ALTER TABLE Pedido
ADD CONSTRAINT fk_pedido_producto FOREIGN KEY (id_producto) REFERENCES Producto(id);

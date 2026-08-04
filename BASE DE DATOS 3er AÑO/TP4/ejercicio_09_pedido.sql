-- EJERCICIO 9: Crear tabla "Pedido"
-- Crear una tabla llamada "Pedido" con las siguientes columnas:
-- - "id" (entero autoincremental y clave primaria)
-- - "id_cliente" (entero, clave foránea que referencia el "id" de la tabla "Cliente")
-- - "fecha" (fecha)
-- - "total" (entero)

CREATE TABLE Pedido (
    id SERIAL PRIMARY KEY,
    id_cliente INTEGER,
    fecha DATE,
    total INTEGER,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);

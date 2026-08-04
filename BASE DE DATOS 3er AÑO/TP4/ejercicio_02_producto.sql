-- EJERCICIO 2: Crear tabla "Producto"
-- Crear una tabla llamada "Producto" con las siguientes columnas:
-- - "id" (entero autoincremental y clave primaria)
-- - "nombre" (cadena de caracteres no nula y única)
-- - "precio" (decimal)
-- - "stock" (entero no negativo)

CREATE TABLE Producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    precio DECIMAL(10, 2),
    stock INTEGER CHECK (stock >= 0)
);

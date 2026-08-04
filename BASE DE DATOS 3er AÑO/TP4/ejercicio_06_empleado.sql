-- EJERCICIO 6: Crear tabla "Empleado"
-- Crear una tabla llamada "Empleado" con las siguientes columnas:
-- - "id" (entero autoincremental y clave primaria)
-- - "nombre" (cadena de caracteres)
-- - "edad" (entero mayor que 18)
-- - "salario" (decimal mayor que 0)

CREATE TABLE Empleado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    edad INTEGER CHECK (edad > 18),
    salario DECIMAL(10, 2) CHECK (salario > 0)
);

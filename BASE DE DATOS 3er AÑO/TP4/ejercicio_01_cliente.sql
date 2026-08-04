-- EJERCICIO 1: Crear tabla "Cliente"
-- Crear una tabla llamada "Cliente" con las siguientes columnas:
-- - "id" (entero autoincremental y clave primaria)
-- - "nombre" (cadena de caracteres)
-- - "email" (cadena de caracteres)
-- - "edad" (entero)

CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    edad INTEGER
);

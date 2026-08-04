-- EJERCICIO 5: Modificar tipo de dato de columna "email" en tabla "Cliente"
-- Modificar el tipo de dato de la columna "email" de "cadena de caracteres" a "texto" en la tabla "Cliente".

ALTER TABLE Cliente
ALTER COLUMN email TYPE TEXT;

-- EJERCICIO 3: Agregar columna "telefono" a tabla "Cliente"
-- Agregar una nueva columna llamada "telefono" (cadena de caracteres) a la tabla "Cliente".

ALTER TABLE Cliente
ADD COLUMN telefono VARCHAR(20);

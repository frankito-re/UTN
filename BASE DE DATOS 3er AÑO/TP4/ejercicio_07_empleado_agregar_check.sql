-- EJERCICIO 7: Agregar restricción CHECK a tabla "Empleado"
-- Agregar una restricción de comprobación en la tabla "Empleado" para asegurar
-- que el salario no sea superior a 10000.

ALTER TABLE Empleado
ADD CONSTRAINT check_salario_maximo CHECK (salario <= 10000);

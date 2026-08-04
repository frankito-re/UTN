-- EJERCICIO 8: Eliminar restricción CHECK de tabla "Empleado"
-- Eliminar la restricción de comprobación que limita la edad en la tabla "Empleado".

ALTER TABLE Empleado
DROP CONSTRAINT empleado_edad_check;

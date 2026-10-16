-- Ejercicio 3: Análisis  del uso de índices  con EXPLAIN

-- 1) Ejecutar consultas  sobre la tabla empleados  y ventas usando  EXPLAIN para visualizar  cómo PostgreSQL utiliza  (o no utiliza)  los índices.
EXPLAIN SELECT * FROM empleados WHERE apellido = 'González';

EXPLAIN SELECT * FROM empleados WHERE LOWER(apellido) = 'gonzález';

-- 2) Identificar consultas donde  el índice es útil y aquellas donde  no es aprovechado, explicando  por qué.
EXPLAIN
SELECT *
FROM ventas
WHERE
    fecha = CURRENT_DATE - 10
    AND producto = 'Laptop';

EXPLAIN SELECT * FROM ventas WHERE fecha = CURRENT_DATE - 10;
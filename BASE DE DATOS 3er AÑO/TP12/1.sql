-- Ejercicio 1: Creación y uso básico de índices

-- 1) Crear una tabla llamada  empleados  con las columnas  id, nombre,  apellido, edad, y salario.
DROP TABLE IF EXISTS empleados;

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT,
    salario NUMERIC(10, 2)
);

-- 2) Insertar 1,000 filas de datos simulados.
INSERT INTO
    empleados (
        nombre,
        apellido,
        edad,
        salario
    )
SELECT md5(random()::text), (
        ARRAY[
            'González', 'Pérez', 'López', 'Martínez', 'Suárez'
        ]
    ) [floor(random() * 5 + 1)], (20 + random() * 40)::int, (30000 + random() * 50000)::numeric(10, 2)
FROM generate_series(1, 1000);

-- 3) Crear un índice  en la columna apellido.
EXPLAIN ANALYZE SELECT * FROM empleados WHERE apellido = 'González';

-- 4) Consultar  la tabla para encontrar  los empleados  con un  apellido específico (por  ejemplo, 'González')  y medir  el tiempo  de ejecución  con y sin el índice.
CREATE INDEX idx_empleados_apellido ON empleados (apellido);
-- Ejercicio 4: Reindexación  y limpieza
-- 1) Crear varios índices  en la tabla empleados  y luego realizar actualizaciones masivas en la tabla.

-- 1.1. Creación de la tabla empleados (si no existe previa ejecución del Ejercicio 1)
CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INT,
    salario NUMERIC(10, 2)
);

-- 1.2. Inserción masiva de 10,000 registros aleatorios para la prueba
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
FROM generate_series(1, 10000);

-- 1.3. Creación de varios índices sobre la tabla empleados CREATE INDEX idx_empleados_apellido ON empleados(apellido);
CREATE INDEX idx_empleados_salario ON empleados (salario);

CREATE INDEX idx_empleados_edad ON empleados (edad);

CREATE INDEX idx_empleados_compuesto ON empleados (apellido, salario);

-- 1.4. Ejecución de actualizaciones masivas (genera rotación de tuplas y fragmentación de índices)
UPDATE empleados SET salario = salario * 1.15 WHERE edad & gt;

30;

UPDATE empleados SET edad = edad + 1;

UPDATE empleados SET apellido = 'González' WHERE id % 4 = 0;

UPDATE empleados
SET
    salario = salario + 5000
WHERE
    apellido = 'Pérez';

-- 2) Ejecutar REINDEX para reconstruir  los índices  y observar  los cambios en el rendimiento.

-- 3) Identificar y eliminar  índices  innecesarios  que no estén siendo  utilizados  en las consultas frecuentes.
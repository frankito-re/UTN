-- Ejercicio 2: Índices compuestos

-- 1) Crear una tabla ventas  con las columnas  id, producto,  fecha, cantidad, precio.
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    producto VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    cantidad INT NOT NULL,
    precio NUMERIC(10, 2) NOT NULL
);

-- 2) Insertar 5,000 filas de datos.
INSERT INTO
    ventas (
        producto,
        fecha,
        cantidad,
        precio
    )
SELECT (
        ARRAY[
            'Laptop', 'Tablet', 'Celular', 'Monitor', 'Teclado'
        ]
    ) [floor(random() * 5 + 1)], CURRENT_DATE - (random() * 365)::int, (1 + random() * 10)::int, (100 + random() * 900)::numeric(10, 2)
FROM generate_series(1, 5000);

-- 3) Crear un índice  compuesto en las columnas  fecha y producto.
CREATE INDEX idx_ventas_fecha_producto ON ventas (fecha, producto);

-- 4) Realizar consultas que  utilicen  ambas columnas y analizar cómo el índice  afecta el rendimiento.
EXPLAIN
ANALYZE
SELECT *
FROM ventas
WHERE
    fecha = CURRENT_DATE - 10
    AND producto = 'Laptop';
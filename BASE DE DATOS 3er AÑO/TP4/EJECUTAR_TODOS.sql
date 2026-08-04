-- PRÁCTICO IV 2026: DDL (Lenguaje de Definición de Datos)
-- SCRIPT MAESTRO - Ejecuta todos los ejercicios en orden
-- Universidad Tecnológica Nacional - Facultad Regional San Rafael

-- BLOQUE 1: CREAR TABLAS BASE
-- ============================

-- Ejercicio 1: Crear tabla Cliente
CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    edad INTEGER
);

-- Ejercicio 2: Crear tabla Producto
CREATE TABLE Producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    precio DECIMAL(10, 2),
    stock INTEGER CHECK (stock >= 0)
);

-- Ejercicio 6: Crear tabla Empleado
CREATE TABLE Empleado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    edad INTEGER CHECK (edad > 18),
    salario DECIMAL(10, 2) CHECK (salario > 0)
);

-- Ejercicio 9: Crear tabla Pedido
CREATE TABLE Pedido (
    id SERIAL PRIMARY KEY,
    id_cliente INTEGER,
    fecha DATE,
    total INTEGER,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);

-- BLOQUE 2: MODIFICACIONES EN TABLA CLIENTE
-- ============================================

-- Ejercicio 3: Agregar columna telefono a Cliente
ALTER TABLE Cliente
ADD COLUMN telefono VARCHAR(20);

-- Ejercicio 4: Eliminar columna edad de Cliente
ALTER TABLE Cliente
DROP COLUMN edad;

-- Ejercicio 5: Modificar tipo de dato email en Cliente
ALTER TABLE Cliente
ALTER COLUMN email TYPE TEXT;

-- BLOQUE 3: MODIFICACIONES EN TABLA EMPLEADO
-- =============================================

-- Ejercicio 7: Agregar restricción CHECK a Empleado (salario máximo)
ALTER TABLE Empleado
ADD CONSTRAINT check_salario_maximo CHECK (salario <= 10000);

-- Ejercicio 8: Eliminar restricción CHECK de edad en Empleado
ALTER TABLE Empleado
DROP CONSTRAINT empleado_edad_check;

-- BLOQUE 4: MODIFICACIONES EN TABLA PEDIDO
-- ==========================================

-- Ejercicio 10: Agregar columna id_producto a Pedido
ALTER TABLE Pedido
ADD COLUMN id_producto INTEGER;

-- Ejercicio 11: Agregar clave foránea a Producto en Pedido
ALTER TABLE Pedido
ADD CONSTRAINT fk_pedido_producto FOREIGN KEY (id_producto) REFERENCES Producto(id);

-- Ejercicio 12: Eliminar clave foránea id_cliente de Pedido
ALTER TABLE Pedido
DROP CONSTRAINT fk_pedido_cliente;

-- BLOQUE 5: CAMBIOS DE ESTRUCTURA
-- =================================

-- Ejercicio 13: Renombrar tabla Cliente a Usuario
ALTER TABLE Cliente
RENAME TO Usuario;

-- Ejercicio 14: Renombrar columna fecha a fecha_pedido en Pedido
ALTER TABLE Pedido
RENAME COLUMN fecha TO fecha_pedido;

-- Ejercicio 15: Cambiar tipo de dato de stock en Producto
ALTER TABLE Producto
ALTER COLUMN stock TYPE DECIMAL(10, 2);

-- Ejercicio 16: Eliminar tabla Producto
DROP TABLE Producto;

-- FIN DEL SCRIPT
-- ==============

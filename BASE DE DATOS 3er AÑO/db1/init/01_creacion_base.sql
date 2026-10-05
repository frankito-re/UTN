-- ============================================================
-- Base de Datos - Ingeniería en Sistemas
-- Práctico VII - SQL: Consultas básicas (SELECT)
-- Ejercicio 1: Tienda de informática
-- Script de creación y carga de datos
-- ============================================================

DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS fabricante;

CREATE TABLE fabricante (
    codigo  INT PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL
);

CREATE TABLE producto (
    codigo             INT PRIMARY KEY,
    nombre             VARCHAR(100) NOT NULL,
    precio             NUMERIC(10,2) NOT NULL,
    stock              INT,                     -- puede quedar NULL (sin dato de stock)
    codigo_fabricante  INT NOT NULL REFERENCES fabricante(codigo)
);

-- ------------------------------------------------------------
-- Fabricantes
-- ------------------------------------------------------------
INSERT INTO fabricante (codigo, nombre) VALUES
(1,  'Samsung'),
(2,  'HP'),
(3,  'Logitech'),
(4,  'Dell'),
(5,  'Lenovo'),
(6,  'Asus'),
(7,  'sony'),
(8,  'Apple'),
(9,  'Acer'),
(10, 'Huawei');

-- ------------------------------------------------------------
-- Productos
-- ------------------------------------------------------------
INSERT INTO producto (codigo, nombre, precio, stock, codigo_fabricante) VALUES
(1,  'Notebook Portatil Gamer',          850000, 5,    1),
(2,  'Monitor LED 24 pulgadas',          180000, 12,   1),
(3,  'Mouse Inalambrico',                 25000, 40,   2),
(4,  'Teclado Mecanico RGB',              45000, 18,   2),
(5,  'Impresora Multifuncion',           220000, NULL, 2),
(6,  'Monitor Curvo 27 pulgadas',        210000, 7,    3),
(7,  'Webcam HD',                         35000, NULL, 3),
(8,  'Auriculares Gamer',                 60000, 22,   3),
(9,  'Notebook Portatil Ultraligera',    620000, 3,    4),
(10, 'Disco SSD 1TB',                     95000, 30,   4),
(11, 'Memoria RAM 16GB',                  55000, 25,   4),
(12, 'Notebook Portatil Empresarial',    540000, NULL, 5),
(13, 'Mouse Gamer',                       38000, 16,   5),
(14, 'Monitor Gamer 165Hz',              320000, 9,    6),
(15, 'Placa de Video',                   480000, 4,    6),
(16, 'Motherboard',                      150000, 11,   6),
(17, 'Auriculares Inalambricos',          90000, 14,   7),
(18, 'Parlante Bluetooth',                40000, NULL, 7),
(19, 'Tablet',                           750000, 6,    8),
(20, 'Smartwatch',                       180000, 20,   8),
(21, 'Notebook Portatil Convertible',    300000, 8,    9),
(22, 'Router WiFi',                       28000, 33,   9),
(23, 'Disco Externo 2TB',                 65000, 17,   10),
(24, 'Monitor 21 pulgadas',              130000, NULL, 10);
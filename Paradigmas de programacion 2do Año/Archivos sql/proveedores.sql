-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 15, 2025 at 02:41 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bd_empresa`
--

-- --------------------------------------------------------

--
-- Table structure for table `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(5) NOT NULL,
  `razon_social` varchar(50) DEFAULT NULL,
  `telefono` bigint(10) DEFAULT NULL,
  `domicilio` varchar(60) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `contacto` varchar(40) DEFAULT NULL,
  `activo` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `razon_social`, `telefono`, `domicilio`, `email`, `contacto`, `activo`) VALUES
(20001, 'TechGlobal SA', 1123456789, 'Av. Córdoba 1234', 'contacto@techglobal.com', 'Laura Gómez', 'S'),
(20002, 'Insumos Médicos SRL', 1123456790, 'Av. Santa Fe 456', 'info@insumed.com', 'Ricardo Pérez', 'S'),
(20003, 'Distribuidora Norte', 1123456791, 'Calle Rivadavia 789', 'ventas@norte.com', 'María Torres', 'N'),
(20004, 'Servicios Informáticos', 1123456792, 'Av. Callao 321', 'servicios@si.com', 'Jorge Díaz', 'S'),
(20005, 'Alimentos y Bebidas SRL', 1123456793, 'San Martín 456', 'contacto@ayb.com', 'Lucía Romero', 'S'),
(20006, 'Oficina Express', 1123456794, 'Belgrano 789', 'ventas@ofiexpress.com', 'Carlos Suárez', 'S'),
(20007, 'EcoLimpio', 1123456795, 'Lavalle 101', 'info@ecolimpio.com', 'Verónica López', 'N'),
(20008, 'MegaConstrucciones', 1123456796, 'Corrientes 2020', 'contacto@megacons.com', 'Tomás Herrera', 'S'),
(20009, 'Print&Go', 1123456797, 'Independencia 303', 'admin@printgo.com', 'Martina Paz', 'S'),
(20010, 'Librería Escolar', 1123456798, 'Pueyrredón 808', 'ventas@libreriaescolar.com', 'Natalia Costa', 'S');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

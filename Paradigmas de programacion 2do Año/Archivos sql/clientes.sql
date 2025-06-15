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
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(5) NOT NULL,
  `apellido` varchar(30) DEFAULT NULL,
  `nombre` varchar(30) DEFAULT NULL,
  `telefono` bigint(10) DEFAULT NULL,
  `domicilio` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `activo` char(1) DEFAULT NULL CHECK (`activo` in ('S','N'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `apellido`, `nombre`, `telefono`, `domicilio`, `email`, `activo`) VALUES
(10001, 'Gómez', 'María', 1123456789, 'Av. Libertador 1234', 'maria.gomez@gmail.com', 'S'),
(10002, 'Pérez', 'Juan', 1134567890, 'Calle Falsa 123', 'juanperez@gmail.com', 'N'),
(10003, 'Rodríguez', 'Lucía', 1145678901, 'Av. Rivadavia 4567', 'lucia.r@gmail.com', 'S'),
(10004, 'Fernández', 'Carlos', 1156789012, 'Mitre 2001', 'carlosf@hotmail.com', 'S'),
(10005, 'López', 'Ana', 1167890123, 'San Martín 300', 'analopez@yahoo.com', 'S'),
(10006, 'Martínez', 'Pedro', 1178901234, 'Belgrano 999', 'pmartinez@gmail.com', 'N'),
(10007, 'García', 'Laura', 1189012345, 'Corrientes 1500', 'laurag@gmail.com', 'S'),
(10008, 'Sánchez', 'Diego', 1190123456, 'Av. Callao 850', 'dsanchez@gmail.com', 'N'),
(10009, 'Torres', 'Valeria', 1112345678, 'Santa Fe 3700', 'valet@gmail.com', 'S'),
(10010, 'Ramírez', 'Esteban', 1129876543, 'Av. Córdoba 5050', 'estebanr@gmail.com', 'S');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

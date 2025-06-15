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
-- Table structure for table `articulos`
--

CREATE TABLE `articulos` (
  `id_articulo` int(5) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `precio_compra` decimal(10,2) DEFAULT NULL,
  `precio_venta` decimal(10,2) DEFAULT NULL,
  `stock` int(6) DEFAULT NULL,
  `id_proveedor` int(5) DEFAULT NULL,
  `activo` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `articulos`
--

INSERT INTO `articulos` (`id_articulo`, `descripcion`, `precio_compra`, `precio_venta`, `stock`, `id_proveedor`, `activo`) VALUES
(10001, 'Notebook Lenovo i5 8GB 256SSD', 380000.00, 450000.00, 15, 10001, 'S'),
(10002, 'Mouse inalámbrico Logitech', 4500.00, 6999.00, 50, 10002, 'S'),
(10003, 'Teclado mecánico Redragon', 12000.00, 14500.00, 20, 10002, 'S'),
(10004, 'Monitor Samsung 24 pulgadas', 65000.00, 82000.00, 10, 10003, 'S'),
(10005, 'Impresora HP DeskJet', 32000.00, 39000.00, 8, 10004, 'N'),
(10006, 'Pendrive Kingston 64GB', 3000.00, 4200.00, 100, 10001, 'S'),
(10007, 'Disco SSD 1TB Crucial', 42000.00, 49500.00, 12, 10003, 'S'),
(10008, 'Placa de video RTX 3060', 190000.00, 220000.00, 5, 10005, 'S'),
(10009, 'Cable HDMI 2m', 900.00, 1500.00, 80, 10002, 'S'),
(10010, 'Tablet Samsung Galaxy Tab A8', 95000.00, 115000.00, 6, 10004, 'S');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articulos`
--
ALTER TABLE `articulos`
  ADD PRIMARY KEY (`id_articulo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

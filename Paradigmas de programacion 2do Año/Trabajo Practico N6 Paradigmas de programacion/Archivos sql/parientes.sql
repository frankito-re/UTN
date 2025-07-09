-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 14, 2025 at 09:01 PM
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
-- Database: `bd_familia`
--

-- --------------------------------------------------------

--
-- Table structure for table `parientes`
--

CREATE TABLE `parientes` (
  `codigo` int(5) DEFAULT NULL,
  `nombre` varchar(30) DEFAULT NULL,
  `apellido` varchar(25) DEFAULT NULL,
  `telefono` bigint(10) DEFAULT NULL,
  `domicilio` varchar(40) DEFAULT NULL,
  `fec_nac` date DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parientes`
--

INSERT INTO `parientes` (`codigo`, `nombre`, `apellido`, `telefono`, `domicilio`, `fec_nac`, `estado`) VALUES
(1, 'Franco', 'Reyes', 412311, 'Mi casa', '2006-06-27', 1),
(2, 'Juan', 'Pérez', 2611234567, 'Calle Falsa 123', '1985-06-15', 1),
(3, 'María', 'González', 2612345678, 'Av. San Martín 1024', '1990-03-20', 1),
(4, 'Ana', 'López', 2614567890, 'Las Heras 234', '2001-01-30', 0),
(5, 'Carlos', 'Sosa', 2615678901, 'Mitre 1000', '1995-07-10', 1),
(6, 'Lucía', 'Fernández', 2616789012, 'Godoy Cruz 222', '1988-09-25', 0),
(7, 'Pedro', 'Ramírez', 2617890123, 'Chile 456', '1993-04-12', 1),
(8, 'Elena', 'Suárez', 2618901234, 'España 999', '1975-12-18', 1),
(9, 'Jorge', 'Cabrera', 2619012345, 'Catamarca 101', '1983-08-08', 0),
(10, 'Sofía', 'Vega', 2610123456, 'Patricias 300', '2002-10-21', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

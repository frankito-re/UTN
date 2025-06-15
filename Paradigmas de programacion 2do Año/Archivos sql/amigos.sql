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
-- Table structure for table `amigos`
--

CREATE TABLE `amigos` (
  `id` int(5) DEFAULT NULL,
  `nombre` varchar(30) DEFAULT NULL,
  `apellido` varchar(25) DEFAULT NULL,
  `telefono` bigint(10) DEFAULT NULL,
  `domicilio` varchar(40) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `fec_nac` date DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `amigos`
--

INSERT INTO `amigos` (`id`, `nombre`, `apellido`, `telefono`, `domicilio`, `correo`, `fec_nac`, `estado`) VALUES
(1, 'Camila', 'Rodríguez', 2611112222, 'Av. Libertador 300', 'camila@gmail.com', '1992-07-15', 1),
(2, 'Mateo', 'López', 2612223333, 'España 450', 'mateo@hotmail.com', '1987-11-02', 1),
(3, 'Valentina', 'Paz', 2613334444, 'Belgrano 150', 'valen@gmail.com', '1990-04-08', 0),
(4, 'Tomás', 'Álvarez', 2614445555, 'Mitre 789', 'tomas@gmail.com', '1995-02-20', 1),
(5, 'Martina', 'Ruiz', 2615556666, 'Rivadavia 120', 'martina@outlook.com', '1998-05-10', 1),
(6, 'Santiago', 'Fernández', 2616667777, 'Alsina 200', 'santi@gmail.com', '1984-09-12', 0),
(7, 'Luciana', 'Mendoza', 2617778888, 'Italia 310', 'lucy@gmail.com', '1991-08-21', 1),
(8, 'Benjamín', 'Castro', 2618889999, 'Tucumán 432', 'benja@live.com', '1993-12-30', 1),
(9, 'Agustina', 'Soto', 2619990000, 'Godoy Cruz 111', 'agus@gmail.com', '1996-03-03', 0),
(10, 'Nicolás', 'Moreno', 2610001111, 'Urquiza 999', 'nico@gmail.com', '1994-06-18', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
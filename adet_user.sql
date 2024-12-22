-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 22, 2024 at 02:58 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `adet`
--

-- --------------------------------------------------------

--
-- Table structure for table `adet_user`
--

CREATE TABLE `adet_user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` text NOT NULL,
  `password` varchar(64) NOT NULL,
  `role` varchar(20) NOT NULL,
  `profile_picture` varchar(255) DEFAULT 'default.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adet_user`
--

INSERT INTO `adet_user` (`id`, `first_name`, `middle_name`, `last_name`, `contact_number`, `email`, `address`, `password`, `role`, `profile_picture`) VALUES
(17, 'test', 'test', 'test', '09465191004', 'test@gmail.com', 'test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'admin', 'default.png'),
(22, 'Try', '', 'try', '09123456789', 'try@gmail.com', 'try', '1e262cd7d110812f5726055a6e672b92cde43648b76adff51a12441fbdf7e667', 'admin', 'rat.png'),
(24, 'Monica', 'L', 'Gato', '09482458474', 'monicagato@gmail.com', '123 Pangit St.', 'ff2c75986179c9eb7ac06b5482fa1f976af49ee7bb766a971981657b0b6eb968', 'user', 'pfp2.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adet_user`
--
ALTER TABLE `adet_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adet_user`
--
ALTER TABLE `adet_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

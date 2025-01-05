-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 05, 2025 at 10:35 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `manajemen_user`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `role` enum('Admin','User') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(50) NOT NULL,
  `password_hash` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `role`, `email`, `password_hash`) VALUES
(10, 'rendi', 'Admin', 'andi123@gmail.com', 'scrypt:32768:8:1$46vWbI3j7IJtsujm$2af55eb56ebcd36b0edf69df11e9f1bdb63c45bfd89a7c3b9ae9571a5d8d010036e8a74fb12f873fdeb77aed85284f077578b0d4f301deac6599f60e0a48d85f'),
(11, 'andika', 'User', 'andikasan765@gmail.com', 'scrypt:32768:8:1$S6NgSjyjo0fn4Xfg$a42096f4ee790d5aca4482547fff4f0892ae8cf1c3c5d8455ceada7bec933e606b7f5ba34eb24b686d02aa91801115c0b544850b23b81940f1788fb72c3c1dea'),
(12, 'riki', 'Admin', 'andika123@gmail.com', 'scrypt:32768:8:1$MNts2eFc5h6lbKwL$3163861488f021d4afe2fb95b1caae1c23ba2167e5de5b14111480db7df4df7cc135dfec977a86cf0da561d91ea2a536c4b12a70246e1a9a25f4476e6880f9ab');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

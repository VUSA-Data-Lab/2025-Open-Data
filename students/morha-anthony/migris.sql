-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 22, 2025 at 09:23 AM
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
-- Database: `migris`
--

-- --------------------------------------------------------

--
-- Table structure for table `trp_decisions_female`
--

CREATE TABLE `trp_decisions_female` (
  `tdf_id` int(11) NOT NULL,
  `id_1` varchar(255) NOT NULL,
  `id_2` varchar(255) NOT NULL,
  `registration_of_decision` date NOT NULL,
  `decision` text NOT NULL,
  `citizenship` varchar(100) NOT NULL,
  `age_group` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `basis_for_decision` varchar(255) NOT NULL,
  `need` text NOT NULL,
  `upload_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trp_decisions_male`
--

CREATE TABLE `trp_decisions_male` (
  `tdm_id` int(11) NOT NULL,
  `id_1` varchar(255) NOT NULL,
  `id_2` varchar(255) NOT NULL,
  `registration_of_decision` date NOT NULL,
  `decision` text NOT NULL,
  `citizenship` varchar(100) NOT NULL,
  `age_group` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `basis_for_decision` varchar(255) NOT NULL,
  `need` text NOT NULL,
  `upload_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trp_overstay_female`
--

CREATE TABLE `trp_overstay_female` (
  `tof_id` int(11) NOT NULL,
  `id_1` varchar(255) NOT NULL,
  `id_2` varchar(255) NOT NULL,
  `citizenship` varchar(100) NOT NULL,
  `registration_of_decision` date NOT NULL,
  `decision` text NOT NULL,
  `basis_for_decision` varchar(255) NOT NULL,
  `age_group` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `departure` varchar(100) NOT NULL,
  `need` text NOT NULL,
  `upload_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trp_overstay_male`
--

CREATE TABLE `trp_overstay_male` (
  `tom_id` int(11) NOT NULL,
  `id_1` varchar(255) NOT NULL,
  `id_2` varchar(255) NOT NULL,
  `citizenship` varchar(100) NOT NULL,
  `registration_of_decision` date NOT NULL,
  `decision` text NOT NULL,
  `basis_for_decision` varchar(255) NOT NULL,
  `age_group` varchar(50) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `departure` varchar(100) NOT NULL,
  `need` text NOT NULL,
  `upload_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `trp_decisions_female`
--
ALTER TABLE `trp_decisions_female`
  ADD PRIMARY KEY (`tdf_id`);

--
-- Indexes for table `trp_decisions_male`
--
ALTER TABLE `trp_decisions_male`
  ADD PRIMARY KEY (`tdm_id`);

--
-- Indexes for table `trp_overstay_female`
--
ALTER TABLE `trp_overstay_female`
  ADD PRIMARY KEY (`tof_id`);

--
-- Indexes for table `trp_overstay_male`
--
ALTER TABLE `trp_overstay_male`
  ADD PRIMARY KEY (`tom_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `trp_decisions_female`
--
ALTER TABLE `trp_decisions_female`
  MODIFY `tdf_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trp_decisions_male`
--
ALTER TABLE `trp_decisions_male`
  MODIFY `tdm_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trp_overstay_female`
--
ALTER TABLE `trp_overstay_female`
  MODIFY `tof_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trp_overstay_male`
--
ALTER TABLE `trp_overstay_male`
  MODIFY `tom_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

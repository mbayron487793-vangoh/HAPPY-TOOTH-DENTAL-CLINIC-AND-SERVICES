-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 18, 2026 at 12:40 PM
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
-- Database: `happy_tooth_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `dentist_id` int(11) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` enum('Scheduled','Completed','Cancelled','No Show') DEFAULT 'Scheduled',
  `notes` text DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_archived` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `patient_id`, `dentist_id`, `appointment_date`, `appointment_time`, `status`, `notes`, `created_by`, `date_created`, `date_updated`, `is_archived`) VALUES
(1, 1, 2, '2026-02-06', '09:00:00', 'Completed', '', NULL, '2026-02-06 19:45:37', '2026-02-08 20:40:23', 0),
(3, 3, 2, '2026-02-08', '09:00:00', 'Completed', 'n/a', 3, '2026-02-08 20:58:14', '2026-02-08 20:59:26', 0),
(4, 2, 2, '2026-02-08', '10:00:00', 'Completed', '', 3, '2026-02-08 21:00:05', '2026-02-08 21:02:25', 0),
(5, 3, 2, '2026-02-08', '22:00:00', 'Completed', '', 3, '2026-02-08 21:10:46', '2026-02-08 21:12:12', 0),
(6, 3, 2, '2026-02-10', '09:00:00', 'Completed', '', 3, '2026-02-10 20:24:43', '2026-02-18 19:33:19', 0),
(7, 1, 1, '2026-02-17', '09:00:00', 'Completed', '', 3, '2026-02-17 23:14:26', '2026-02-17 23:15:34', 0),
(8, 2, 2, '2026-02-17', '09:00:00', 'Scheduled', '', 3, '2026-02-17 23:24:00', '2026-02-17 23:24:00', 0),
(9, 1, 2, '2026-02-17', '11:00:00', 'Scheduled', '', 3, '2026-02-17 23:24:23', '2026-02-17 23:24:23', 0),
(10, 2, 1, '2026-02-17', '13:00:00', 'Completed', '', 3, '2026-02-17 23:24:40', '2026-02-17 23:25:49', 0),
(11, 3, 1, '2026-02-17', '15:00:00', 'Completed', '', 3, '2026-02-17 23:29:00', '2026-02-17 23:29:57', 0),
(12, 1, 1, '2027-02-19', '09:00:00', 'Completed', '', 3, '2026-02-17 23:52:17', '2026-02-17 23:55:25', 0),
(13, 4, 1, '2026-02-18', '09:00:00', 'Completed', '', 3, '2026-02-18 00:04:10', '2026-02-18 00:05:01', 0),
(14, 4, 2, '2026-02-19', '10:00:00', 'Scheduled', '', 3, '2026-02-18 00:10:10', '2026-02-18 00:10:10', 0),
(15, 1, 1, '2026-02-18', '13:00:00', 'Completed', '', 3, '2026-02-18 00:10:24', '2026-02-18 00:12:04', 0),
(16, 2, 1, '2026-02-21', '09:00:00', 'Completed', 'n/a', 3, '2026-02-18 19:26:32', '2026-02-18 19:27:38', 0),
(17, 5, 1, '2026-02-18', '08:00:00', 'Scheduled', '', 3, '2026-02-18 19:31:52', '2026-02-18 19:31:52', 0),
(18, 1, 2, '2026-02-18', '09:00:00', 'Scheduled', '', 3, '2026-02-18 19:37:13', '2026-02-18 19:37:13', 0);

-- --------------------------------------------------------

--
-- Table structure for table `billings`
--

CREATE TABLE `billings` (
  `id` int(11) NOT NULL,
  `appointment_id` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL DEFAULT 0.00,
  `amount_paid` decimal(10,2) NOT NULL DEFAULT 0.00,
  `balance` decimal(10,2) NOT NULL DEFAULT 0.00,
  `payment_method` enum('Cash','GCash','Card','Bank Transfer','Other') DEFAULT 'Cash',
  `payment_status` enum('Paid','Partial','Unpaid') DEFAULT 'Unpaid',
  `date_paid` datetime DEFAULT NULL,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `generated_by` int(11) DEFAULT NULL,
  `processed_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billings`
--

INSERT INTO `billings` (`id`, `appointment_id`, `total_amount`, `amount_paid`, `balance`, `payment_method`, `payment_status`, `date_paid`, `date_created`, `date_updated`, `generated_by`, `processed_by`) VALUES
(1, 1, 5000.00, 5000.00, 0.00, 'Cash', 'Paid', '2026-02-06 19:50:47', '2026-02-06 19:50:47', '2026-02-17 23:18:33', 1, NULL),
(2, 1, 1000.00, 1000.00, 0.00, 'Cash', 'Paid', '2026-02-08 20:40:33', '2026-02-08 20:39:42', '2026-02-17 23:18:33', 1, NULL),
(3, 3, 12000.00, 12000.00, 0.00, 'Cash', 'Paid', '2026-02-08 20:59:31', '2026-02-08 20:58:59', '2026-02-17 23:23:01', 3, NULL),
(4, 4, 300.00, 300.00, 0.00, 'Cash', 'Paid', '2026-02-08 21:02:25', '2026-02-08 21:01:33', '2026-02-17 23:23:01', 3, NULL),
(5, 5, 800.00, 1000.00, -200.00, 'Cash', 'Paid', '2026-02-08 21:12:12', '2026-02-08 21:11:48', '2026-02-17 23:23:01', 3, NULL),
(6, 7, 12000.00, 12000.00, 0.00, 'Cash', 'Paid', '2026-02-17 23:15:34', '2026-02-17 23:15:12', '2026-02-17 23:23:01', 3, NULL),
(7, 10, 8000.00, 8800.00, -800.00, 'Cash', 'Paid', '2026-02-17 23:25:49', '2026-02-17 23:25:20', '2026-02-17 23:27:56', 3, NULL),
(9, 12, 12000.00, 12000.00, 0.00, 'Cash', 'Paid', '2026-02-17 23:55:25', '2026-02-17 23:52:40', '2026-02-17 23:58:00', 3, NULL),
(10, 13, 8000.00, 8000.00, 0.00, 'Cash', 'Paid', '2026-02-18 00:05:01', '2026-02-18 00:04:41', '2026-02-18 00:07:19', 3, NULL),
(12, 15, 12000.00, 12000.00, 0.00, 'Cash', 'Paid', '2026-02-18 00:12:04', '2026-02-18 00:11:46', '2026-02-18 00:15:04', 3, NULL),
(13, 16, 800.00, 800.00, 0.00, 'Cash', 'Paid', '2026-02-18 19:30:05', '2026-02-18 19:27:12', '2026-02-18 19:30:05', 2, 3),
(14, 6, 12000.00, 12000.00, 0.00, 'Cash', 'Paid', '2026-02-18 19:33:19', '2026-02-18 19:32:56', '2026-02-18 19:33:19', 4, 3);

--
-- Triggers `billings`
--
DELIMITER $$
CREATE TRIGGER `trg_billing_set_generated_by` BEFORE INSERT ON `billings` FOR EACH ROW BEGIN
                        IF NEW.generated_by IS NULL THEN
                            SET NEW.generated_by = @app_user_id;
                        END IF;
                    END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `dentists`
--

CREATE TABLE `dentists` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `specialization` varchar(100) DEFAULT 'General Dentistry',
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dentists`
--

INSERT INTO `dentists` (`id`, `first_name`, `last_name`, `specialization`, `contact_number`, `email`, `user_id`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Juan', 'Dela Cruz', 'General Dentistry', '09171234567', NULL, 2, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(2, 'Mikko', 'Cuyno', 'General Dentistry', '09774234027', 'mcuyno63@gmail.com', 4, 1, '2026-02-06 19:42:41', '2026-02-06 19:49:46');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `birthdate` date NOT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `medical_history` text DEFAULT NULL,
  `date_registered` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `first_name`, `last_name`, `gender`, `birthdate`, `contact_number`, `email`, `address`, `medical_history`, `date_registered`, `date_updated`) VALUES
(1, 'haley', 'cuyno', 'Male', '2005-02-12', '0923124214', 'haley@gmail.com', 'dumalag 1, matina aplaya, davao city', 'none', '2026-02-06 19:45:24', '2026-02-06 19:45:24'),
(2, 'elah', 'menil', 'Female', '2001-02-08', '09774234027', 'menilelah@gmail.com', 'talomo,talusa', 'n/a', '2026-02-08 20:37:25', '2026-02-08 20:37:25'),
(3, 'mario', 'cuyno', 'Male', '2001-02-08', '0923125412', 'marioc@gmail.com', 'dumalag 1', 'n/a', '2026-02-08 20:57:56', '2026-02-08 20:57:56'),
(4, 'jayd', 'cuyno', 'Male', '2001-08-18', '09774234207', 'jayd@gmail.com', 'dumalag 1', 'n/a', '2026-02-18 00:03:59', '2026-02-18 00:03:59'),
(5, 'jarrel', 'cuyno', 'Male', '2001-09-13', '09111111111', 'jarrel@gmail.com', 'dumalag 1', 'n/a', '2026-02-18 19:31:10', '2026-02-18 19:31:10');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(11) NOT NULL,
  `service_name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00,
  `is_active` tinyint(1) DEFAULT 1,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `service_name`, `description`, `price`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Dental Consultation', 'Oral examination and assessment', 300.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(2, 'Tooth Cleaning (Prophylaxis)', 'Scaling and polishing of teeth', 800.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(3, 'Tooth Extraction (Simple)', 'Simple removal of a tooth', 1000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(4, 'Tooth Extraction (Surgical)', 'Complex removal requiring surgery', 3500.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(5, 'Dental Filling (Composite)', 'Tooth-colored composite filling', 1200.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(6, 'Dental Filling (Amalgam)', 'Silver amalgam filling', 800.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(7, 'Root Canal Treatment', 'Endodontic treatment for infected tooth', 5000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(8, 'Tooth Whitening / Bleaching', 'Cosmetic teeth whitening', 4000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(9, 'Dental X-Ray (Periapical)', 'Single tooth X-ray', 350.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(10, 'Panoramic X-Ray', 'Full mouth panoramic X-ray', 800.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(11, 'Dental Crown', 'Cap placed over a damaged tooth', 8000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(12, 'Dental Bridge', 'Replacement for missing teeth', 12000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(13, 'Dentures (Complete)', 'Full set of removable false teeth', 15000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(14, 'Dentures (Partial)', 'Partial removable false teeth', 8000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(15, 'Orthodontic Braces (Metal)', 'Traditional metal braces', 30000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(16, 'Retainer', 'Post-braces retainer appliance', 5000.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(17, 'Fluoride Treatment', 'Preventive fluoride application', 500.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(18, 'Pit and Fissure Sealant', 'Preventive sealant per tooth', 600.00, 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29');

-- --------------------------------------------------------

--
-- Table structure for table `treatments`
--

CREATE TABLE `treatments` (
  `id` int(11) NOT NULL,
  `appointment_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `tooth_number` varchar(10) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `date_created` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `treatments`
--

INSERT INTO `treatments` (`id`, `appointment_id`, `service_id`, `tooth_number`, `notes`, `date_created`) VALUES
(1, 1, 3, '14', 'none', '2026-02-08 20:39:42'),
(2, 3, 12, '14', 'n/a', '2026-02-08 20:58:59'),
(3, 4, 1, 'n/a', 'will be back, the patient needs time to think for the surgery', '2026-02-08 21:01:33'),
(4, 5, 2, 'all of the', 'n/a', '2026-02-08 21:11:48'),
(5, 7, 12, '14', 'nothing', '2026-02-17 23:15:12'),
(6, 10, 11, '14', 'wala', '2026-02-17 23:25:20'),
(7, 11, 18, '1', 'n/a', '2026-02-17 23:29:35'),
(8, 12, 12, '12', '1', '2026-02-17 23:52:40'),
(9, 13, 11, '1', 'n/a', '2026-02-18 00:04:41'),
(10, 15, 12, '1', '', '2026-02-18 00:11:46'),
(11, 16, 6, '1', 'n/a', '2026-02-18 19:27:12'),
(12, 6, 12, '1', 'n/a', '2026-02-18 19:32:56');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `role` enum('Admin','Dentist','Staff') NOT NULL DEFAULT 'Staff',
  `is_active` tinyint(1) DEFAULT 1,
  `date_created` datetime DEFAULT current_timestamp(),
  `date_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `first_name`, `last_name`, `role`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'admin', '$2b$12$EPaYJppt0aKixbsl1b7FZuPi.UMjc1uU1RtIX/VONpQ3FRs6R5TUK', 'System', 'Administrator', 'Admin', 1, '2026-02-06 19:41:28', '2026-02-06 19:41:28'),
(2, 'dentist', '$2b$12$mXy8Npagx2xumKrw6/BW2uOJV.fXHQ6mMFo.pkvyNGRj5MOz52PRC', 'Juan', 'Dela Cruz', 'Dentist', 1, '2026-02-06 19:41:28', '2026-02-06 19:41:28'),
(3, 'staff', '$2b$12$l8oxBGnrA5A1iLR0QVBolelWve3y8PUiqkB6uVjujeMd6KRUArxoi', 'Maria', 'Santos', 'Staff', 1, '2026-02-06 19:41:29', '2026-02-06 19:41:29'),
(4, 'mikko.cuyno', '$2b$12$HlK8UtY/bFHmkFzwXAQHLeHcy5aXkSG8lF2nPAMcKz8XLcY1/N8Ai', 'Mikko', 'Cuyno', 'Dentist', 1, '2026-02-06 19:49:46', '2026-02-08 21:19:33'),
(5, 'hale.cuyno', '$2b$12$gMCEGdx8UTfwOD24OTluguKFo5G9wApmIdTwJQY4DzmDdNvTjTb..', 'hale', 'cuyno', 'Staff', 1, '2026-02-06 21:46:53', '2026-02-06 21:46:53'),
(6, 'mikmik', '$2b$12$GC1wvxj9JBnlNPrHbf/x2.bDVYu11KmV3.c6UTckVm4/aadJ9aEU6', 'mik', 'mik', 'Staff', 1, '2026-02-10 19:59:34', '2026-02-10 19:59:34');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `dentist_id` (`dentist_id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `billings`
--
ALTER TABLE `billings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appointment_id` (`appointment_id`),
  ADD KEY `processed_by` (`processed_by`),
  ADD KEY `generated_by` (`generated_by`);

--
-- Indexes for table `dentists`
--
ALTER TABLE `dentists`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `treatments`
--
ALTER TABLE `treatments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appointment_id` (`appointment_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `billings`
--
ALTER TABLE `billings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `dentists`
--
ALTER TABLE `dentists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `treatments`
--
ALTER TABLE `treatments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`dentist_id`) REFERENCES `dentists` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `billings`
--
ALTER TABLE `billings`
  ADD CONSTRAINT `billings_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `billings_ibfk_10` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_11` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_12` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_13` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_14` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_15` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_16` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_17` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_18` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_19` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_2` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_20` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_3` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_4` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_5` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_6` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_7` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_8` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `billings_ibfk_9` FOREIGN KEY (`generated_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `dentists`
--
ALTER TABLE `dentists`
  ADD CONSTRAINT `dentists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `treatments`
--
ALTER TABLE `treatments`
  ADD CONSTRAINT `treatments_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `treatments_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

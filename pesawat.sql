-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jun 13, 2021 at 05:39 PM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 5.6.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pesawat`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_jenis_pesawat`
--

CREATE TABLE `tbl_jenis_pesawat` (
  `id_jenis_pesawat` int(11) NOT NULL,
  `nama_jenis_pesawat` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `tbl_jenis_pesawat`
--

INSERT INTO `tbl_jenis_pesawat` (`id_jenis_pesawat`, `nama_jenis_pesawat`) VALUES
(1, 'Pesawat Militer'),
(2, 'Helikopter Militer'),
(3, 'Pesawat Sipil'),
(4, 'Helikopter Sipil');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_karakteristik`
--

CREATE TABLE `tbl_karakteristik` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `tbl_karakteristik`
--

INSERT INTO `tbl_karakteristik` (`id`, `name`) VALUES
(2, 'Jenis Sayap'),
(3, 'Penempatan Sayap'),
(5, 'Arah Sayap'),
(6, 'Jenis Mesin'),
(8, 'Posisi Mesin'),
(9, 'Badan Pesawat'),
(10, 'Bentuk Ekor Pesawat'),
(13, 'Persenjataan'),
(14, 'Warna');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_pesawat`
--

CREATE TABLE `tbl_pesawat` (
  `id` int(11) NOT NULL,
  `nama_pesawat` varchar(35) CHARACTER SET utf8 DEFAULT NULL,
  `id_jenis_pesawat` int(11) DEFAULT NULL,
  `id_jenis_sayap` int(11) DEFAULT NULL,
  `id_jenis_penempatan_sayap` int(11) DEFAULT NULL,
  `id_arah_sayap` int(11) DEFAULT NULL,
  `id_jenis_mesin` int(11) DEFAULT NULL,
  `id_badan_pesawat` int(11) DEFAULT NULL,
  `id_persenjataan` int(11) DEFAULT NULL,
  `id_warna` int(11) DEFAULT NULL,
  `id_posisi_mesin` int(11) NOT NULL,
  `id_jenis_ekor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_pesawat`
--

INSERT INTO `tbl_pesawat` (`id`, `nama_pesawat`, `id_jenis_pesawat`, `id_jenis_sayap`, `id_jenis_penempatan_sayap`, `id_arah_sayap`, `id_jenis_mesin`, `id_badan_pesawat`, `id_persenjataan`, `id_warna`, `id_posisi_mesin`, `id_jenis_ekor`) VALUES
(1, 'Chengdu J-7', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(2, 'Chengdu J-10', 1, 3, 6, 15, 21, 37, 58, 60, 30, 44),
(3, 'Chengdu J-20', 1, 3, 4, 15, 21, 38, 58, 60, 30, 45),
(4, 'Shenyang J-8', 1, 3, 5, 15, 21, 38, 58, 60, 30, 44),
(5, 'Shenyang J-11', 1, 3, 4, 13, 21, 38, 58, 60, 30, 45),
(6, 'Shenyang J-16', 1, 3, 4, 13, 21, 38, 58, 60, 30, 45),
(7, 'F-16 Fighting Falcon', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(8, 'F-15E Strike Eagle', 1, 3, 4, 13, 21, 38, 58, 60, 30, 45),
(9, 'F-35 Lightning II', 1, 3, 5, 13, 21, 37, 58, 60, 30, 45),
(10, 'F-22 Raptor', 1, 3, 4, 15, 21, 37, 58, 60, 30, 45),
(11, 'F-5 Freedom Fighter', 1, 3, 6, 13, 21, 38, 58, 60, 30, 44),
(12, 'F-4 Phantom II', 1, 3, 6, 13, 21, 37, 58, 60, 30, 44),
(13, 'Mikoyan MiG-29', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(14, 'Mikoyan MiG-35', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(15, 'Sukhoi Su-27', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(16, 'Sukhoi Su-35', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(17, 'Typhoon Fighter FGR-4', 1, 3, 6, 15, 21, 37, 58, 60, 30, 44),
(18, 'Dassault Rafale', 1, 3, 6, 15, 21, 37, 58, 60, 30, 44),
(19, 'Dassault Mirage 2000', 1, 3, 6, 15, 21, 37, 58, 60, 30, 44),
(20, 'JF-17 Thunder', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(21, 'Tu-160M Blackjack', 1, 3, 6, 13, 21, 37, 59, 60, 29, 44),
(22, 'Sukhoi Su-57', 1, 3, 4, 15, 21, 38, 58, 60, 30, 45),
(23, 'F-15C Eagle', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(24, 'L-39 Albatros', 1, 3, 6, 12, 21, 37, 59, 60, 30, 44),
(25, 'Tupolev Tu-22m', 1, 3, 6, 13, 21, 38, 58, 60, 30, 44),
(26, 'Yakovlev Yak-130', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(27, 'Shenyang J-31', 1, 3, 4, 13, 21, 38, 58, 60, 30, 45),
(28, 'Shenyang J-15', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(29, 'Xi''an H-20', 1, 3, 5, 15, 21, 42, 58, 60, 30, 52),
(30, 'Xi''an H-6K', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(31, 'Xi''an JH-7', 1, 3, 4, 13, 21, 37, 58, 60, 30, 44),
(32, 'Hongdu JL-15', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44),
(33, 'BAE System Hawk', 1, 3, 6, 13, 21, 37, 59, 60, 30, 44),
(34, 'Dassault', 1, 3, 4, 13, 21, 37, 59, 60, 36, 44),
(35, 'Jaguar', 1, 3, 4, 13, 21, 37, 58, 60, 36, 44),
(36, 'Panavia Tornado', 1, 3, 4, 13, 21, 37, 58, 60, 30, 44),
(37, 'T-38B Talon', 1, 3, 6, 13, 21, 38, 59, 60, 30, 44),
(38, 'T-37C Tweet', 1, 3, 5, 12, 19, 38, 59, 60, 30, 44),
(39, 'McDonnell Douglas F/A-18D Hornet', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45),
(40, 'Boeing C-17 Globemaster III', 1, 3, 4, 13, 21, 41, 59, 60, 29, 46),
(41, 'V-22 Osprey', 1, 2, 4, 12, 20, 41, 58, 60, 29, 48),
(42, 'Northrop Grumman B-2 Spirit', 1, 3, 6, 13, 21, 42, 58, 61, 36, 50),
(43, 'F-117', 1, 3, 6, 13, 21, 42, 58, 61, 36, 49),
(44, 'F-18', 1, 3, 5, 13, 21, 37, 58, 60, 30, 45),
(45, 'EMB 314/A-29 Super Tucano', 1, 3, 6, 12, 20, 37, 58, 60, 35, 44),
(46, 'Antonov An-124', 3, 3, 4, 13, 21, 41, 59, 61, 29, 44),
(47, 'Antonov An-225', 3, 3, 4, 13, 21, 41, 59, 61, 29, 44),
(48, 'Airbus A300', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(49, 'ATR-72', 3, 3, 4, 12, 20, 41, 59, 61, 29, 46),
(50, 'CN-235', 3, 3, 4, 13, 20, 41, 59, 61, 29, 44),
(51, 'CASA C-212', 3, 3, 4, 12, 20, 41, 59, 61, 29, 44),
(52, 'N-219', 3, 3, 4, 12, 20, 41, 59, 61, 29, 44),
(53, 'N-250', 3, 3, 4, 12, 20, 41, 59, 61, 29, 44),
(54, 'N-245', 3, 3, 4, 13, 20, 41, 59, 61, 29, 44),
(55, 'Airbus A380', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(56, 'Airbus A340 600', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(57, 'Boeing 747 400', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(58, 'Embraer 190', 3, 3, 6, 13, 20, 41, 59, 61, 29, 44),
(59, 'Tupolev Tu-204', 3, 3, 6, 13, 20, 41, 59, 61, 29, 44),
(60, 'NAMC YS-11', 3, 3, 6, 12, 20, 41, 59, 61, 29, 44),
(61, 'DC-10', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(62, 'DC-93', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46),
(63, 'MD-11', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(64, 'MD-82', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46),
(65, 'Fokker F28', 3, 3, 6, 13, 20, 41, 59, 61, 35, 46),
(66, 'Fokker F50', 3, 3, 6, 12, 20, 41, 59, 61, 29, 44),
(67, 'Hawker Siddley HS 748', 3, 3, 6, 12, 20, 41, 59, 61, 29, 44),
(68, 'Hawker 400', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46),
(69, 'Gulfstream G200', 3, 3, 6, 13, 21, 41, 59, 61, 35, 47),
(70, 'Gulfstream 3', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46),
(71, 'Vickers VC-10', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46),
(72, 'Dassault Falcon 900', 3, 3, 6, 13, 21, 41, 59, 61, 35, 47),
(73, 'Falcon 2000', 3, 3, 6, 13, 21, 41, 59, 61, 35, 47),
(74, 'DHC-8', 3, 3, 4, 12, 20, 41, 59, 61, 29, 46),
(75, 'Boeing 707', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(76, 'Boeing 737 Classic', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(77, 'DHC-6', 3, 3, 4, 12, 20, 41, 59, 61, 29, 46),
(78, 'Douglas DC-3', 3, 3, 6, 12, 20, 41, 59, 61, 29, 44),
(79, 'McDonnell Douglas DC-10', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(80, 'McDonnell Douglas MD-82', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44),
(81, 'AH-64 Apache Longbow', 2, 2, 7, 16, 22, 43, 58, 60, 32, 51),
(82, 'AS32 Super Puma', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(83, 'AW101 Merlin', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(84, 'AW109 Power', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(85, 'A129 Mangusta', 2, 2, 7, 16, 22, 43, 58, 60, 32, 51),
(86, 'Chinook CH-47F', 2, 2, 7, 16, 22, 43, 59, 60, 31, 52),
(87, 'Sikorsky S-70A', 2, 2, 7, 16, 22, 43, 58, 60, 33, 51),
(88, 'Kamov KA-50 Black Shark', 2, 2, 7, 16, 22, 43, 58, 60, 32, 44),
(89, 'Kamov KA-52 Alligator', 2, 2, 7, 16, 22, 43, 58, 60, 32, 44),
(90, 'NH90', 2, 2, 7, 16, 22, 43, 59, 60, 34, 51),
(91, 'Sea King S-61', 2, 2, 7, 16, 22, 43, 59, 60, 34, 51),
(92, 'Sikorsky S-76', 2, 2, 7, 16, 22, 43, 59, 60, 34, 51),
(93, 'Bell UH-1 Iroquois', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(94, 'Bell AH-1W Super Cobra', 2, 2, 7, 16, 22, 43, 58, 60, 33, 51),
(95, 'Sikorsky HH-60P Pave Hawk', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(96, 'Sikorsky UH-60M Black Hawk', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(97, 'KA-52M', 2, 2, 7, 16, 22, 43, 58, 60, 32, 44),
(98, 'UH-72A Lakota', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(99, 'Yakovlev Yak-24U', 2, 2, 7, 16, 22, 43, 59, 60, 31, 52),
(100, 'PZL-Swidnik Mi-2', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(101, 'Bell AH-1S Cobra', 2, 2, 7, 16, 22, 43, 58, 60, 33, 51),
(102, 'Mil Mi 24P', 2, 2, 7, 16, 22, 43, 58, 60, 33, 51),
(103, 'Boeing CH-47D Chinook', 2, 2, 7, 16, 22, 43, 59, 60, 31, 52),
(104, 'Mil Mi 8MTV-2', 2, 2, 7, 16, 22, 43, 58, 60, 32, 51),
(105, 'Sikorsky UH-60A Black Hawk', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(106, 'Boeing CH-47F Chinook', 2, 2, 7, 16, 22, 43, 59, 60, 31, 52),
(107, 'Eurocopter AS-532U2 Cougar Mk2', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(108, 'Westland WS-61 Sea King Mk48', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(109, 'Westland WAH-64D Longbow Apache AH1', 2, 2, 7, 16, 22, 43, 58, 60, 32, 51),
(110, 'Sikorsky S-70C(M)-2 Thunderhawk', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(111, 'Agusta A-109CM', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(112, 'Bell UH-1H Huey II', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(113, 'Mil Mi-8MT', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(114, 'Agusta HH-3F', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(115, 'AgustaWestland HH-139A', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(116, 'Westland WG-13 Lynx AH7', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(117, 'Sikorsky CH-53E Super Stallion', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(118, 'Agusta AB-47J Ranger', 2, 2, 7, 16, 22, 43, 59, 60, 32, 51),
(119, 'Aerospatiale TP-1 Oryx M', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(120, 'Kazan Ansat-U', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51),
(121, 'Eurocopter EC-135', 4, 2, 7, 16, 22, 43, 59, 61, 34, 51),
(122, 'Bell 430', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(123, 'Agusta-Bell 412 Grifone', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(124, 'Bell 230', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(125, 'Bell JetRanger', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(126, 'Bell Supertransport', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(127, 'Robinson R44', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(128, 'Sikorsky S-76', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(129, 'Enstrom F-28', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(130, 'Eurocopter AS350', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(131, 'Eurocopter EC120 Colibri', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(132, 'NBK 117', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(133, 'Bell 212', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(134, 'Bell 407', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(135, 'Agusta A109', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(136, 'Eurocopter EC145', 4, 2, 7, 16, 22, 43, 59, 61, 33, 45),
(137, 'Eurocopter EC130', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(138, 'Hughes 369', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(139, 'Mil Mi-34 Hermit', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(140, 'MD Explorer', 4, 2, 7, 16, 22, 43, 59, 61, 33, 45),
(141, 'Ansat', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(142, 'Bell 412', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(143, 'Sikorsky S-92', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(144, 'Agusta W169', 4, 2, 7, 16, 22, 43, 59, 61, 34, 51),
(145, 'Aeropastiale AS-355', 4, 2, 7, 16, 22, 43, 59, 61, 34, 51),
(146, 'Airbus Helicopter H225', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(147, 'Airbus Helicopter EC-120 Colibri', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(148, 'Airbus Helicopter H175', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(149, 'Avicopter AC313', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51),
(150, 'Cicare CH-7', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(151, 'CH-77 Ranabot', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(152, 'Guimbal Cabri G2', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(153, 'Sikorsky S-434', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(154, 'Schweizer 330', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51),
(155, 'Airbus Helicopter H135 Helionix', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_process`
--

CREATE TABLE `tbl_process` (
  `id` int(11) NOT NULL,
  `id_pesawat` int(11) NOT NULL,
  `fusi_informasi` varchar(255) NOT NULL,
  `jumlah_fusi` int(11) NOT NULL,
  `naive_bayes` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_process`
--

INSERT INTO `tbl_process` (`id`, `id_pesawat`, `fusi_informasi`, `jumlah_fusi`, `naive_bayes`) VALUES
(1, 1, '1010000010010010', 6, 0.133333),
(2, 2, '1000100010001010', 4, 0.0888889),
(3, 3, '1000111010110010', 2, 0.0444444),
(4, 4, '1000101110001010', 1, 0.0222222),
(5, 5, '1010011010110010', 4, 0.0888889),
(6, 6, '1010011010110010', 4, 0.0888889),
(7, 7, '1010000010010010', 6, 0.133333),
(8, 8, '1010011010110010', 4, 0.0888889),
(9, 9, '1010010110100110', 2, 0.0444444),
(10, 10, '1000110110101010', 1, 0.0222222),
(11, 11, '1010001110010010', 2, 0.0444444),
(12, 12, '1010000010001010', 1, 0.0222222),
(13, 13, '1010010110101010', 7, 0.155556),
(14, 14, '1010010110101010', 7, 0.155556),
(15, 15, '1010010110101010', 7, 0.155556),
(16, 16, '1010010110101010', 7, 0.155556),
(17, 17, '1000100010001010', 4, 0.0888889),
(18, 18, '1000100010001010', 4, 0.0888889),
(19, 19, '1000100010001010', 4, 0.0888889),
(20, 20, '1010000010010010', 6, 0.133333),
(21, 21, '1001101111000110', 1, 0.0222222),
(22, 22, '1000111010110010', 2, 0.0444444),
(23, 23, '1010010110101010', 7, 0.155556),
(24, 24, '1010000001001010', 1, 0.0222222),
(25, 25, '1010001110010010', 2, 0.0444444),
(26, 26, '1010000010010010', 6, 0.133333),
(27, 27, '1010011010110010', 4, 0.0888889),
(28, 28, '1010010110101010', 7, 0.155556),
(29, 29, '0000101111110010', 1, 0.0222222),
(30, 30, '1010000010010010', 6, 0.133333),
(31, 31, '1010000010011110', 2, 0.0444444),
(32, 32, '1010000010010010', 6, 0.133333),
(33, 33, '1010110001001010', 1, 0.0222222),
(34, 34, '1011001100010110', 1, 0.0222222),
(35, 35, '1011111111010110', 1, 0.0222222),
(36, 36, '1010000010011110', 2, 0.0444444),
(37, 37, '1010111101010010', 1, 0.0222222),
(38, 38, '1000101101011110', 1, 0.0222222),
(39, 39, '1010010110101010', 7, 0.155556),
(40, 40, '1001101011010011', 1, 0.0222222),
(41, 41, '1000100010101000', 1, 0.0222222),
(42, 42, '1000001001110111', 1, 0.0222222),
(43, 43, '1001010111110110', 1, 0.0222222),
(44, 44, '1010010110100110', 2, 0.0444444),
(45, 45, '1010000010111010', 1, 0.0222222),
(46, 81, '1101011100001010', 4, 0.1),
(47, 82, '1101111001001000', 16, 0.4),
(48, 83, '1101111001001000', 16, 0.4),
(49, 84, '1101111001001000', 16, 0.4),
(50, 85, '1101011100001010', 4, 0.1),
(51, 86, '0111000000111101', 4, 0.1),
(52, 87, '1101001010001000', 4, 0.1),
(53, 88, '1111010000011010', 3, 0.075),
(54, 89, '1111010000011010', 3, 0.075),
(55, 90, '1101101011001010', 3, 0.075),
(56, 91, '1101101011001010', 3, 0.075),
(57, 92, '1101101011001010', 3, 0.075),
(58, 93, '1101111001001000', 16, 0.4),
(59, 94, '1101001010001000', 4, 0.1),
(60, 95, '1101111001001000', 16, 0.4),
(61, 96, '1101111001001000', 16, 0.4),
(62, 97, '1111010000011010', 3, 0.075),
(63, 98, '1101111001001000', 16, 0.4),
(64, 99, '0111000000111101', 4, 0.1),
(65, 100, '1101111001001000', 16, 0.4),
(66, 101, '1101001010001000', 4, 0.1),
(67, 102, '1101001010001000', 4, 0.1),
(68, 103, '0111000000111101', 4, 0.1),
(69, 104, '1101011100001010', 4, 0.1),
(70, 105, '1101101111001010', 6, 0.15),
(71, 106, '0111000000111101', 4, 0.1),
(72, 107, '1101111001001000', 16, 0.4),
(73, 108, '1101101111001010', 6, 0.15),
(74, 109, '1101011100001010', 4, 0.1),
(75, 110, '1101111001001000', 16, 0.4),
(76, 111, '1101111001001000', 16, 0.4),
(77, 112, '1101101111001010', 6, 0.15),
(78, 113, '1101111001001000', 16, 0.4),
(79, 114, '1101111001001000', 16, 0.4),
(80, 115, '1101111001001000', 16, 0.4),
(81, 116, '1101101111001010', 6, 0.15),
(82, 117, '1101101111001010', 6, 0.15),
(83, 118, '1101101111001010', 6, 0.15),
(84, 119, '1101111001001000', 16, 0.4),
(85, 120, '1101111001001000', 16, 0.4),
(86, 46, '1010000110010011', 2, 0.0571429),
(87, 47, '1010000110010011', 2, 0.0571429),
(88, 48, '1010000110000111', 10, 0.285714),
(89, 49, '1011011010111011', 3, 0.0857143),
(90, 50, '1011100110001011', 2, 0.0571429),
(91, 51, '1011010110001011', 3, 0.0857143),
(92, 52, '1011010110001011', 3, 0.0857143),
(93, 53, '1011010110001011', 3, 0.0857143),
(94, 54, '1011100110001011', 2, 0.0571429),
(95, 55, '1010000110000111', 10, 0.285714),
(96, 56, '1010000110000111', 10, 0.285714),
(97, 57, '1010000110000111', 10, 0.285714),
(98, 58, '1011100110011111', 2, 0.0571429),
(99, 59, '1011100110011111', 2, 0.0571429),
(100, 60, '1011010110011111', 4, 0.114286),
(101, 61, '1010000110000111', 10, 0.285714),
(102, 62, '1000000100010011', 5, 0.142857),
(103, 63, '1010000110000111', 10, 0.285714),
(104, 64, '1000000100010011', 5, 0.142857),
(105, 65, '1001100100001011', 1, 0.0285714),
(106, 66, '1011010110011111', 4, 0.114286),
(107, 67, '1011010110011111', 4, 0.114286),
(108, 68, '1000000100010011', 5, 0.142857),
(109, 69, '1000011101110011', 3, 0.0857143),
(110, 70, '1000000100010011', 5, 0.142857),
(111, 71, '1000000100010011', 5, 0.142857),
(112, 72, '1000011101110011', 3, 0.0857143),
(113, 73, '1000011101110011', 3, 0.0857143),
(114, 74, '1011011010111011', 3, 0.0857143),
(115, 75, '1010000110000111', 10, 0.285714),
(116, 76, '1010000110000111', 10, 0.285714),
(117, 77, '1011011010111011', 3, 0.0857143),
(118, 78, '1011010110011111', 4, 0.114286),
(119, 79, '1010000110000111', 10, 0.285714),
(120, 80, '1010000110000111', 10, 0.285714),
(121, 121, '1110001010111010', 3, 0.0857143),
(122, 122, '1110011000111000', 23, 0.657143),
(123, 123, '1110011000111000', 23, 0.657143),
(124, 124, '1110011000111000', 23, 0.657143),
(125, 125, '1110011000111000', 23, 0.657143),
(126, 126, '1110011000111000', 23, 0.657143),
(127, 127, '1110011000111000', 23, 0.657143),
(128, 128, '1110011000111000', 23, 0.657143),
(129, 129, '1110001110111010', 7, 0.2),
(130, 130, '1110011000111000', 23, 0.657143),
(131, 131, '1110011000111000', 23, 0.657143),
(132, 132, '1110011000111000', 23, 0.657143),
(133, 133, '1110011000111000', 23, 0.657143),
(134, 134, '1110011000111000', 23, 0.657143),
(135, 135, '1110011000111000', 23, 0.657143),
(136, 136, '1100000000011100', 2, 0.0571429),
(137, 137, '1110011000111000', 23, 0.657143),
(138, 138, '1110011000111000', 23, 0.657143),
(139, 139, '1110001110111010', 7, 0.2),
(140, 140, '1100000000011100', 2, 0.0571429),
(141, 141, '1110011000111000', 23, 0.657143),
(142, 142, '1110011000111000', 23, 0.657143),
(143, 143, '1110011000111000', 23, 0.657143),
(144, 144, '1110001010111010', 3, 0.0857143),
(145, 145, '1110001010111010', 3, 0.0857143),
(146, 146, '1110011000111000', 23, 0.657143),
(147, 147, '1110011000111000', 23, 0.657143),
(148, 148, '1110011000111000', 23, 0.657143),
(149, 149, '1110011000111000', 23, 0.657143),
(150, 150, '1110001110111010', 7, 0.2),
(151, 151, '1110001110111010', 7, 0.2),
(152, 152, '1110001110111010', 7, 0.2),
(153, 153, '1110001110111010', 7, 0.2),
(154, 154, '1110001110111010', 7, 0.2),
(155, 155, '1110011000111000', 23, 0.657143);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_spesifik`
--

CREATE TABLE `tbl_spesifik` (
  `id_spesifik` int(11) NOT NULL,
  `id_karakteristik` int(11) DEFAULT NULL,
  `kode_spesifik` varchar(4) DEFAULT NULL,
  `spesifik` varchar(255) DEFAULT NULL,
  `bit_spesifik` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `tbl_spesifik`
--

INSERT INTO `tbl_spesifik` (`id_spesifik`, `id_karakteristik`, `kode_spesifik`, `spesifik`, `bit_spesifik`) VALUES
(2, 2, 'RW', 'Rotary Wings', '0000000000000001'),
(3, 2, 'FW', 'Fixed Wings', '0000000000000010'),
(4, 3, 'HW', 'High Wings', '0000000000000100'),
(5, 3, 'MW', 'Mid Wings', '0000000000001000'),
(6, 3, 'LW', 'Low Wings', '0000000000010000'),
(7, 3, 'NP', 'Don''t Have Wing Placement', '0000000000100000'),
(12, 5, 'SW', 'Straight Wings', '0000010000000000'),
(13, 5, 'BW', 'Sweptback Wings', '0000100000000000'),
(14, 5, 'FS', 'Forward Swept Wings', '0001000000000000'),
(15, 5, 'DW', 'Delta Wings', '0010000000000000'),
(16, 5, 'TW', 'Rotor Wings', '0100000000000000'),
(17, 5, 'ND', 'Don''t Have Wing Direction', '1000000000000000'),
(18, 6, 'PS', 'Piston', '0100000000000001'),
(19, 6, 'TJ', 'TurboJet', '0010000000000100'),
(20, 6, 'UP', 'TurboProp', '0001000000001000'),
(21, 6, 'TF', 'TurboFan', '0000100000010000'),
(22, 6, 'TS', 'TurboShaft', '0000010000100000'),
(29, 8, 'OW', 'On The Wing', '0010010010000100'),
(30, 8, 'BF', 'Behind Fuselage', '0001001100001000'),
(31, 8, 'AF', 'Above Fuselage', '0000100011010000'),
(32, 8, 'BC', 'Behind Cabin', '0000000100000011'),
(33, 8, 'AC', 'Above Cabin', '0000010010000001'),
(34, 8, 'IF', 'In Fuselage', '0000000000000011'),
(35, 8, 'FF', 'Front Fuselage', '0000011100100000'),
(36, 8, 'CF', 'Close to the Fuselage', '0000110001000000'),
(37, 9, 'SB', 'Subsonic', '0000001000010000'),
(38, 9, 'SP', 'Supersonic', '0000000100001000'),
(39, 9, 'CS', 'High-Capacity Subsonic', '0000000010000100'),
(40, 9, 'MS', 'High-maneuverability Supersonic', '0000000001000010'),
(41, 9, 'FB', 'Flying Boat', '0000000000100001'),
(42, 9, 'HP', 'Hypersonic', '0000000001000100'),
(43, 9, 'DF', 'Dragonfly', '0000000010001000'),
(44, 10, 'CL', 'Conventional Tail', '0000000100010000'),
(45, 10, 'WL', 'Twin Tail', '0000010000100100'),
(46, 10, 'TL', 'T-Tail', '0000001000100000'),
(47, 10, 'CT', 'Cruciform Tail', '0000010001000000'),
(48, 10, 'HT', 'H-Tail', '0000100010000000'),
(49, 10, 'VT', 'V-Tail', '0001000100000000'),
(50, 10, 'NT', 'No Tail (double main rotor)', '0000011010000001'),
(51, 10, 'TR', 'Rotor Tail', '0010001000000000'),
(52, 10, 'DL ', 'Don''t Have Tail', '1000000000100100'),
(58, 13, 'HE', 'Have a Weapon', '1000100010000000'),
(59, 13, 'NE', 'Don''t Have Weaponary', '1000010001000000'),
(60, 14, 'LR', 'Berloreng', '0011100000000000'),
(61, 14, 'TR', 'Tidak Berloreng', '0000000001110000');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_testing`
--

CREATE TABLE `tbl_testing` (
  `id` int(11) NOT NULL,
  `nama_pesawat` varchar(35) CHARACTER SET utf8 DEFAULT NULL,
  `id_jenis_pesawat` int(11) DEFAULT NULL,
  `id_jenis_sayap` int(11) DEFAULT NULL,
  `id_jenis_penempatan_sayap` int(11) DEFAULT NULL,
  `id_arah_sayap` int(11) DEFAULT NULL,
  `id_jenis_mesin` int(11) DEFAULT NULL,
  `id_badan_pesawat` int(11) DEFAULT NULL,
  `id_persenjataan` int(11) DEFAULT NULL,
  `id_warna` int(11) DEFAULT NULL,
  `id_posisi_mesin` int(11) NOT NULL,
  `id_jenis_ekor` int(11) NOT NULL,
  `result` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_testing`
--

INSERT INTO `tbl_testing` (`id`, `nama_pesawat`, `id_jenis_pesawat`, `id_jenis_sayap`, `id_jenis_penempatan_sayap`, `id_arah_sayap`, `id_jenis_mesin`, `id_badan_pesawat`, `id_persenjataan`, `id_warna`, `id_posisi_mesin`, `id_jenis_ekor`, `result`) VALUES
(1, '-', 1, 3, 5, 13, 21, 37, 58, 60, 30, 44, 'Pesawat Militer'),
(2, 'Airbus', 4, 3, 4, 12, 20, 41, 59, 61, 29, 44, 'Pesawat Sipil'),
(3, 'F18', 1, 3, 5, 13, 21, 37, 58, 60, 30, 45, 'Pesawat Militer'),
(4, 'Sikorsky', 2, 2, 7, 16, 22, 43, 58, 60, 34, 51, 'Objek tidak dikenal atau belum ada di dalam basis data'),
(5, 'Bell', 2, 2, 7, 16, 22, 43, 58, 60, 33, 51, 'Helikopter Militer'),
(6, 'Chengdu ', 1, 3, 4, 15, 21, 38, 58, 60, 30, 45, 'Pesawat Militer'),
(7, 'Shenyang', 1, 3, 4, 13, 21, 38, 58, 60, 30, 45, 'Pesawat Militer'),
(8, 'Sukhoi', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45, 'Pesawat Militer'),
(9, 'Sukhoi Su35', 1, 3, 4, 13, 21, 37, 58, 60, 30, 45, 'Pesawat Militer'),
(10, 'F5', 1, 3, 6, 13, 21, 38, 58, 60, 30, 44, 'Pesawat Militer'),
(11, '-', 3, 3, 6, 13, 21, 42, 58, 61, 36, 50, 'Pesawat Militer'),
(15, 'Hawker', 3, 3, 6, 13, 21, 41, 59, 61, 35, 46, 'Pesawat Sipil'),
(16, '-', 3, 3, 6, 13, 21, 41, 59, 61, 35, 47, 'Pesawat Sipil'),
(18, 'Boeing', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44, 'Pesawat Sipil'),
(19, '-', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44, 'Pesawat Sipil'),
(20, 'DC10', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44, 'Pesawat Sipil'),
(21, 'Airbus', 3, 3, 6, 13, 21, 41, 59, 61, 29, 44, 'Pesawat Sipil'),
(22, 'AW101', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51, 'Helikopter Sipil'),
(23, 'A129', 2, 2, 7, 16, 22, 43, 58, 60, 32, 51, 'Helikopter Militer'),
(24, '-', 2, 2, 7, 16, 22, 43, 58, 60, 32, 44, 'Helikopter Militer'),
(26, 'NH90', 2, 2, 7, 16, 22, 43, 59, 60, 34, 51, 'Helikopter Militer'),
(27, 'KA', 2, 2, 7, 16, 22, 43, 58, 60, 32, 44, 'Helikopter Militer'),
(28, 'YAK-24U', 2, 2, 7, 16, 22, 43, 59, 60, 31, 52, 'Helikopter Militer'),
(29, 'Agusta', 2, 2, 7, 16, 22, 43, 59, 60, 33, 51, 'Helikopter Militer'),
(30, 'Robinso', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51, 'Helikopter Sipil'),
(31, 'Enstrom F-28', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51, 'Helikopter Sipil'),
(32, 'Eurocopter', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51, 'Helikopter Sipil'),
(33, 'A109', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51, 'Helikopter Sipil'),
(34, 'Eurocopter', 4, 2, 7, 16, 22, 43, 59, 61, 33, 51, 'Helikopter Sipil'),
(35, 'Schweizer ', 4, 2, 7, 16, 22, 43, 59, 61, 32, 51, 'Helikopter Sipil'),
(36, 'F117', 3, 3, 6, 13, 21, 42, 58, 61, 36, 49, 'Pesawat Militer');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user`
--

CREATE TABLE `tbl_user` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_user`
--

INSERT INTO `tbl_user` (`id`, `name`, `username`, `password`) VALUES
(1, 'admin', 'admin', '21232f297a57a5a743894a0e4a801fc3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_jenis_pesawat`
--
ALTER TABLE `tbl_jenis_pesawat`
  ADD PRIMARY KEY (`id_jenis_pesawat`) USING BTREE;

--
-- Indexes for table `tbl_karakteristik`
--
ALTER TABLE `tbl_karakteristik`
  ADD PRIMARY KEY (`id`) USING BTREE;

--
-- Indexes for table `tbl_pesawat`
--
ALTER TABLE `tbl_pesawat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_process`
--
ALTER TABLE `tbl_process`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_spesifik`
--
ALTER TABLE `tbl_spesifik`
  ADD PRIMARY KEY (`id_spesifik`) USING BTREE;

--
-- Indexes for table `tbl_testing`
--
ALTER TABLE `tbl_testing`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_jenis_pesawat`
--
ALTER TABLE `tbl_jenis_pesawat`
  MODIFY `id_jenis_pesawat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `tbl_karakteristik`
--
ALTER TABLE `tbl_karakteristik`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `tbl_pesawat`
--
ALTER TABLE `tbl_pesawat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=156;
--
-- AUTO_INCREMENT for table `tbl_process`
--
ALTER TABLE `tbl_process`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=156;
--
-- AUTO_INCREMENT for table `tbl_spesifik`
--
ALTER TABLE `tbl_spesifik`
  MODIFY `id_spesifik` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;
--
-- AUTO_INCREMENT for table `tbl_testing`
--
ALTER TABLE `tbl_testing`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;
--
-- AUTO_INCREMENT for table `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

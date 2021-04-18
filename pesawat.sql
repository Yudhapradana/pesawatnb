-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 18, 2021 at 06:02 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
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
(1, 'Pesawat'),
(2, 'Helikopter');

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
(4, 'Jumlah Sayap'),
(5, 'Arah Sayap'),
(6, 'Jenis Mesin'),
(7, 'Jumlah Mesin'),
(8, 'Posisi Mesin'),
(9, 'Badan Pesawat'),
(10, 'Bentuk Ekor Pesawat'),
(11, 'Jenis Landing Gear'),
(12, 'Canard'),
(13, 'Persenjataan'),
(14, 'Warna');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_karakter_pesawat`
--

CREATE TABLE `tbl_karakter_pesawat` (
  `id_karakter_pesawat` int(11) NOT NULL,
  `nama_karakter_pesawat` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_karakter_pesawat`
--

INSERT INTO `tbl_karakter_pesawat` (`id_karakter_pesawat`, `nama_karakter_pesawat`) VALUES
(1, 'Sipil'),
(2, 'Militer');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_pesawat`
--

CREATE TABLE `tbl_pesawat` (
  `id` int(11) NOT NULL,
  `nama_pesawat` varchar(35) CHARACTER SET utf8 DEFAULT NULL,
  `id_jenis_pesawat` int(11) DEFAULT NULL,
  `id_karakter_pesawat` int(11) DEFAULT NULL,
  `id_jenis_sayap` int(11) DEFAULT NULL,
  `id_jenis_penempatan_sayap` int(11) DEFAULT NULL,
  `id_jumlah_sayap` int(11) DEFAULT NULL,
  `id_arah_sayap` int(11) DEFAULT NULL,
  `id_jenis_mesin` int(11) DEFAULT NULL,
  `id_jumlah_mesin` int(11) DEFAULT NULL,
  `id_posisi_mesin` int(11) DEFAULT NULL,
  `id_badan_pesawat` int(11) DEFAULT NULL,
  `id_jenis_ekor` int(11) DEFAULT NULL,
  `id_jenis_landing_gear` int(11) DEFAULT NULL,
  `id_persenjataan` int(11) DEFAULT NULL,
  `id_warna` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(7, 3, 'NP', 'Don\'t Have Wing Placement', '0000000000100000'),
(8, 4, 'MP', 'Monoplane', '0000000001000000'),
(9, 4, 'BP', 'Biplane', '0000000010000000'),
(10, 4, 'TP', 'Triplane', '0000000100000000'),
(11, 4, 'NW', 'Don\'t Have Wing', '0000001000000000'),
(12, 5, 'SW', 'Straight Wings', '0000010000000000'),
(13, 5, 'BW', 'Sweptback Wings', '0000100000000000'),
(14, 5, 'FS', 'Forward Swept Wings', '0001000000000000'),
(15, 5, 'DW', 'Delta Wings', '0010000000000000'),
(16, 5, 'TW', 'Rotor Wings', '0100000000000000'),
(17, 5, 'ND', 'Don\'t Have Wing Direction', '1000000000000000'),
(18, 6, 'PS', 'Piston', '0100000000000001'),
(19, 6, 'TJ', 'Turbo Jet', '0010000000000100'),
(20, 6, 'UP', 'Turbo Prop', '0001000000001000'),
(21, 6, 'TF', 'Turbo Fan', '0000100000010000'),
(22, 6, 'TS', 'Turbo Shaft', '0000010000100000'),
(23, 7, 'OM', '1 (One Machine)', '0000001001000000'),
(24, 7, 'TM', '2 (Two Machine)', '0000000110000000'),
(25, 7, 'RM', '3 (Three Machine)', '1000000110000000'),
(26, 7, 'FM', '4 (Four Machine)', '1000000110000010'),
(27, 7, 'VM', '5 (Five Machine)', '1000001001000010'),
(28, 7, 'SM', '6 (Six Machine)', '0100001001000010'),
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
(51, 10, 'TR', 'Tail Rotor', '0010001000000000'),
(52, 10, 'DL ', 'Don’t have Tail', '1000000000100100'),
(53, 11, 'FH', 'Folded Wheels', '0100010000000000'),
(54, 11, 'NF', 'Wheels not folded', '1000100000000000'),
(55, 11, 'SD', 'Skids', '1100010000001000'),
(56, 12, 'HC', 'Have Canard', '1010001000000100'),
(57, 12, 'NC', 'Don\'t Have Canard', '1001000100000010'),
(58, 13, 'HE', 'Have Weaponary', '1000100010000000'),
(59, 13, 'NE', 'Don\'t Have Weaponary', '1000010001000000'),
(60, 14, 'LR', 'Loreng Biru', '0011100000000000'),
(61, 14, 'TR', 'Warna Komersil', '0000000001110000'),
(62, 14, 'LB', 'Loreng Abu-abu', '0010100000000000'),
(63, 14, 'HM', 'Hitam', '0110100000000000'),
(64, 14, 'AB', 'Abu-abu', '0011010000000000'),
(65, 14, 'LH', 'Loreng Hijau', '0100110000000000'),
(66, 14, 'LC', 'Loreng Coklat', '0101010000000000');

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
-- Indexes for table `tbl_karakter_pesawat`
--
ALTER TABLE `tbl_karakter_pesawat`
  ADD PRIMARY KEY (`id_karakter_pesawat`);

--
-- Indexes for table `tbl_pesawat`
--
ALTER TABLE `tbl_pesawat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tbl_spesifik`
--
ALTER TABLE `tbl_spesifik`
  ADD PRIMARY KEY (`id_spesifik`) USING BTREE;

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
  MODIFY `id_jenis_pesawat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tbl_karakteristik`
--
ALTER TABLE `tbl_karakteristik`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `tbl_karakter_pesawat`
--
ALTER TABLE `tbl_karakter_pesawat`
  MODIFY `id_karakter_pesawat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `tbl_pesawat`
--
ALTER TABLE `tbl_pesawat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_spesifik`
--
ALTER TABLE `tbl_spesifik`
  MODIFY `id_spesifik` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

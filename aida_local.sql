-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-aida
-- Creato il: Dic 12, 2024 alle 09:37
-- Versione del server: 8.0.31
-- Versione PHP: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aida_local`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `config_files`
--

CREATE TABLE `config_files` (
  `id` int NOT NULL,
  `filename` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `filepath` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT './configs',
  `username` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `upload_date` datetime DEFAULT NULL,
  `last_update` datetime DEFAULT NULL,
  `ext` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `filetype` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `period` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `original_start_date` datetime DEFAULT NULL,
  `sampling` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nacq` int DEFAULT NULL,
  `t_sampling` float DEFAULT NULL,
  `t_acq` float DEFAULT NULL,
  `t_window` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `isrunning` tinyint DEFAULT '0',
  `iscomplete` tinyint DEFAULT '0',
  `opmode` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `history`
--

CREATE TABLE `history` (
  `id` int NOT NULL,
  `date_time` datetime DEFAULT NULL,
  `username` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `operation` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `input` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `output` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `configuration` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- --------------------------------------------------------

--
-- Struttura della tabella `hktm_efd_params`
--

CREATE TABLE `hktm_efd_params` (
  `id` int NOT NULL,
  `param` varchar(45) DEFAULT NULL,
  `units` varchar(10) DEFAULT NULL,
  `description` longtext,
  `minval` float DEFAULT '-999',
  `maxval` float DEFAULT '-999',
  `hardmin` float NOT NULL DEFAULT '-999',
  `hardmax` float NOT NULL DEFAULT '-999',
  `subsystem` varchar(45) DEFAULT NULL,
  `hascalib` tinyint NOT NULL DEFAULT '0',
  `extra` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `hktm_efd_params`
--

INSERT INTO `hktm_efd_params` (`id`, `param`, `units`, `description`, `minval`, `maxval`, `hardmin`, `hardmax`, `subsystem`, `hascalib`, `extra`) VALUES
(1, 'ring0', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(2, 'ring1', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(3, 'ring10', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(4, 'ring11', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(5, 'ring2', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(6, 'ring3', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(7, 'ring4', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(8, 'ring5', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(9, 'ring6', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(10, 'ring7', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(11, 'ring8', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(12, 'ring9', 'deg_C', 'Ring temperatures: LG2-1, LG2-2, LG2-3, LG2-4, LG3-1, LG3-2, LG3-3, LG3-4, LG4-1, LG4-2, LG4-3, and LG4-4.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(13, 'intake0', 'deg_C', 'Intake temperatures: #1 and #2.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(14, 'intake1', 'deg_C', 'Intake temperatures: #1 and #2.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(15, 'exhaust0', 'deg_C', 'Exhaust temperatures: #1 and #2.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(16, 'exhaust1', 'deg_C', 'Exhaust temperatures: #1 and #2.', -999, -999, -999, -999, 'MTM2', 0, 'temperature'),
(17, 'lutGravity0', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(18, 'lutGravity1', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(19, 'lutGravity2', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(20, 'lutGravity3', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(21, 'lutGravity4', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(22, 'lutGravity5', 'N', 'Gravity component (F_e + F_0 + F_a + F_f) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(23, 'lutTemperature0', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(24, 'lutTemperature1', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(25, 'lutTemperature2', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(26, 'lutTemperature3', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(27, 'lutTemperature4', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(28, 'lutTemperature5', 'N', 'Temperature component (T_u + T_x + T_y + T_r) of look-up table (LUT) force for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(29, 'applied0', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(30, 'applied1', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(31, 'applied2', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(32, 'applied3', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(33, 'applied4', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(34, 'applied5', 'N', 'Force applied by SAL command or script for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(35, 'measured0', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(36, 'measured1', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(37, 'measured2', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(38, 'measured3', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(39, 'measured4', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(40, 'measured5', 'N', 'Force measurement by load cell for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(41, 'hardpointCorrection0', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(42, 'hardpointCorrection1', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(43, 'hardpointCorrection2', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(44, 'hardpointCorrection3', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(45, 'hardpointCorrection4', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce'),
(46, 'hardpointCorrection5', 'N', 'Hardpoint compensation force correction for each actuator in sequence.', -999, -999, -999, -999, 'MTM2', 0, 'tangentForce');

-- --------------------------------------------------------

--
-- Struttura della tabella `hktm_fake_params`
--

CREATE TABLE `hktm_fake_params` (
  `id` int NOT NULL,
  `param` varchar(45) DEFAULT NULL,
  `units` varchar(10) DEFAULT NULL,
  `description` longtext,
  `minval` float DEFAULT '-999',
  `maxval` float DEFAULT '-999',
  `hardmin` float NOT NULL DEFAULT '-999',
  `hardmax` float NOT NULL DEFAULT '-999',
  `subsystem` varchar(45) DEFAULT NULL,
  `hascalib` tinyint NOT NULL DEFAULT '0',
  `extra` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `hktm_fake_params`
--

INSERT INTO `hktm_fake_params` (`id`, `param`, `units`, `description`, `minval`, `maxval`, `hardmin`, `hardmax`, `subsystem`, `hascalib`, `extra`) VALUES
(1, 'temperature', 'degC', 'Example of Temperature parameter', -114.5, 124.5, -114.5, 124.5, 'SysA', 0, '0'),
(2, 'current', 'mA', 'Example of Current parameter', 0.15, 0.4, 0.15, 0.4, 'SysB', 0, '0'),
(3, 'voltage', 'V', 'Example of Voltage parameter', 9.2, 9.8, 9.2, 9.8, 'SysC', 0, '0');

-- --------------------------------------------------------

--
-- Struttura della tabella `local_files`
--

CREATE TABLE `local_files` (
  `id` int UNSIGNED NOT NULL,
  `filename` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `data_source` varchar(45) DEFAULT NULL,
  `subsystem` varchar(45) DEFAULT NULL,
  `date_start` int UNSIGNED DEFAULT '0',
  `date_stop` int UNSIGNED DEFAULT '0',
  `username` varchar(45) DEFAULT NULL,
  `filetype` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='	';

-- --------------------------------------------------------

--
-- Struttura della tabella `login_attempts`
--

CREATE TABLE `login_attempts` (
  `user_id` int NOT NULL,
  `time` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `login_attempts`
--

INSERT INTO `login_attempts` (`user_id`, `time`) VALUES
(1, '1671457588'),
(1, '1671457596'),
(1, '1671457618'),
(1, '1671457634'),
(1, '1671638394'),
(1, '1671638411'),
(1, '1698142880'),
(1, '1698142935'),
(1, '1698143038'),
(1, '1704898511'),
(1, '1704900286'),
(1, '1704900299'),
(1, '1704900311'),
(1, '1706803435'),
(1, '1715776428'),
(2, '1725374307');

-- --------------------------------------------------------

--
-- Struttura della tabella `members`
--

CREATE TABLE `members` (
  `id` int NOT NULL,
  `username` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` char(128) NOT NULL,
  `salt` char(128) NOT NULL,
  `role` varchar(45) NOT NULL DEFAULT 'user',
  `active` tinyint NOT NULL DEFAULT '0',
  `last_login` datetime DEFAULT NULL,
  `action_date` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `operation_modes`
--

CREATE TABLE `operation_modes` (
  `id` int NOT NULL,
  `mode` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `enable` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `operation_modes`
--

INSERT INTO `operation_modes` (`id`, `mode`, `enable`) VALUES
(1, 'debug', 0),
(2, 'debug-local', 0),
(3, 'nominal', 1),
(4, 'contingency', 0),
(5, 'commissioning', 0);

-- --------------------------------------------------------

--
-- Struttura della tabella `plots`
--

CREATE TABLE `plots` (
  `id` int NOT NULL,
  `plot_name` varchar(45) NOT NULL,
  `parameters` longtext,
  `plot_title` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `plots`
--

INSERT INTO `plots` (`id`, `plot_name`, `parameters`, `plot_title`) VALUES
(1, 'Trend', NULL, 'Trend Analysis'),
(2, 'Scatter', '{\"X\" : {\"type\":\"string\", \"origin\":\"db\"}}', 'Scatter Plot'),
(3, 'Histogram', '{\"Bin Size\" : {\"type\" : \"number\", \"min\" : 0, \"include_min\":0}, \"Number of Bins\" : {\"type\" : \"integer\", \"min\":1, \"include_min\" : 1}}', 'Histogram');

-- --------------------------------------------------------

--
-- Struttura della tabella `pwd_reset_tmp`
--

CREATE TABLE `pwd_reset_tmp` (
  `id` int NOT NULL,
  `email` varchar(250) NOT NULL,
  `k` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expdate` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `pwd_reset_tmp`
--

INSERT INTO `pwd_reset_tmp` (`id`, `email`, `k`, `expdate`) VALUES
(34, 'giuseppe.riccio08@gmail.com', 'f2f4012f777983b0fcf4c116ef52f340d466cbbc7e', '2024-04-13 11:54:48');

-- --------------------------------------------------------

--
-- Struttura della tabella `report_files`
--

CREATE TABLE `report_files` (
  `id` int NOT NULL,
  `filename` varchar(128) DEFAULT NULL,
  `filepath` varchar(45) DEFAULT 'report',
  `username` varchar(45) DEFAULT NULL,
  `upload_date` datetime DEFAULT NULL,
  `ext` varchar(45) DEFAULT 'pdf',
  `filetype` varchar(45) DEFAULT 'document',
  `period` varchar(45) DEFAULT NULL,
  `config_file` varchar(45) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `configpath` varchar(45) DEFAULT 'config'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `running_reports`
--

CREATE TABLE `running_reports` (
  `id` int NOT NULL,
  `username` varchar(45) DEFAULT 'auto',
  `config_file` varchar(45) DEFAULT NULL,
  `run_date` datetime DEFAULT NULL,
  `period` varchar(45) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `exp_status` decimal(6,1) DEFAULT '0.0',
  `pid` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `statistics`
--

CREATE TABLE `statistics` (
  `id` int NOT NULL,
  `stat_name` varchar(45) NOT NULL,
  `stat_slug` varchar(45) NOT NULL,
  `stat_function` varchar(45) NOT NULL,
  `stat_type` varchar(45) NOT NULL,
  `parameters` longtext,
  `addmore` tinyint NOT NULL DEFAULT '0',
  `tooltip` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='	';

--
-- Dump dei dati per la tabella `statistics`
--

INSERT INTO `statistics` (`id`, `stat_name`, `stat_slug`, `stat_function`, `stat_type`, `parameters`, `addmore`, `tooltip`) VALUES
(1, 'Mean', 'mean', 'dqc_mean', 'global', NULL, 0, NULL),
(2, 'Standard_Deviation', 'standard deviation', 'dqc_stdev', 'global', NULL, 0, NULL),
(3, 'Median', 'median', 'dqc_median', 'global', NULL, 0, NULL),
(4, 'Min', 'min', 'dqc_min', 'global', NULL, 0, NULL),
(5, 'Max', 'max', 'dqc_max', 'global', NULL, 0, NULL),
(6, 'RMS', 'rms', 'dqc_rms', 'global', NULL, 0, NULL),
(7, 'Variance', 'variance', 'dqc_variance', 'global', NULL, 0, NULL),
(8, 'Kurtosis', 'kurtosis', 'dqc_kurtosis', 'global', NULL, 0, NULL),
(9, 'Skewness', 'skewness', 'dqc_skewness', 'global', NULL, 0, NULL),
(10, 'MAD', 'mad', 'dqc_mad', 'global', NULL, 0, NULL),
(11, 'NMAD', 'nmad', 'dqc_nmad', 'global', NULL, 0, NULL),
(12, 'Percentile', 'percentile', 'dqc_percentile', 'special', '{\"quantile\" : {\"type\" : \"number\", \"id\" : \"quantile\", \"min\" : 0, \"max\" : 100, \"default\" : 50, \"required\" : \"True\"}, \"interpolation\" : {\"type\" : \"select\", \"id\" : \"interpolation\", \"option\" : [\"linear\", \"lower\", \"higher\", \"nearest\", \"midpoint\"], \"required\" : \"True\"}}', 1, NULL),
(13, 'Mode', 'mode', 'dqc_mode', 'special', '{\"precision\" : {\"type\": \"number\", \"id\" : \"precision\", \"min\" : 0, \"default\" : 0,  \"required\" : \"False\"}}', 1, 'If precision is greater than 0, data will be arranged into bins of width = 2*precision and the median of values in each bin will be considered for calculation. Otherwise the single values will be considered.'),
(14, 'Sigma_Clip', 'sigma clip', 'dqc_sigma_clip', 'special', '{\"sigma\" : {\"type\" : \"number\", \"id\" : \"sigma\", \"min\" : 0, \"default\" : 3, \"required\" : \"True\"}, \"function\" : {\"type\" : \"select\", \"id\" : \"function\", \"option\" : [\"mean\", \"median\", \"biweight\"], \"required\" : \"True\"}}', 1, NULL),
(15, 'Biweight_Mean', 'biweight mean', 'dqc_biweight', 'special', '{\"iterMax\" : {\"type\": \"number\", \"id\" : \"iterMax\", \"min\" : 1, \"default\" : 25, \"required\" :\" False\"}, \"epsilon\" : {\"type\" : \"number\", \"id\" : \"epsilon\", \"min\" : 0, \"default\" : 1e-20, \"required\" :\" False\"}}', 1, NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `stored_files`
--

CREATE TABLE `stored_files` (
  `id` int NOT NULL,
  `filename` varchar(128) DEFAULT NULL,
  `filepath` varchar(45) DEFAULT 'stored',
  `username` varchar(45) DEFAULT NULL,
  `date_exp` datetime DEFAULT NULL,
  `ext` varchar(45) DEFAULT NULL,
  `filetype` varchar(45) DEFAULT NULL,
  `status_exp` varchar(45) DEFAULT 'nd',
  `comment_exp` longtext,
  `parinfo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `sourcename` varchar(45) NOT NULL,
  `exp_tstart` datetime DEFAULT NULL,
  `exp_tstop` datetime DEFAULT NULL,
  `plot_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `stored_plots`
--

CREATE TABLE `stored_plots` (
  `id` int NOT NULL,
  `plot_type` varchar(45) NOT NULL,
  `usecase` varchar(45) NOT NULL,
  `plot_name` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `plot_data` longtext NOT NULL,
  `labels` longtext NOT NULL,
  `stats_enable` varchar(11) NOT NULL DEFAULT 'global',
  `stats_list` longtext,
  `tstart` varchar(25) NOT NULL,
  `tstop` varchar(25) NOT NULL,
  `tokeep` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `systems`
--

CREATE TABLE `systems` (
  `id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `origin` varchar(20) NOT NULL,
  `allowed_subs_check` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `required_filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `add_filters` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `plot_delta` float NOT NULL DEFAULT '0',
  `enabled` tinyint NOT NULL DEFAULT '0',
  `has_eas` tinyint NOT NULL DEFAULT '0' COMMENT 'Need connections settings and methods',
  `has_iws` tinyint NOT NULL DEFAULT '0' COMMENT 'Need connections settings and methods'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dump dei dati per la tabella `systems`
--

INSERT INTO `systems` (`id`, `name`, `origin`, `allowed_subs_check`, `required_filters`, `add_filters`, `plot_delta`, `enabled`, `has_eas`, `has_iws`) VALUES
(1, 'EFD', 'hktm', 'HKTM', '{\"Subsytem\": {\"col\": \"efd_system\", \"type\": \"dropdown-db\", \"set_for\": \"single\"}}', NULL, 0, 1, 1, 0),
(16, 'FAKE', 'hktm', 'HKTM', '{\"Subsytem\": {\"col\": \"fake_system\", \"type\": \"dropdown-db\", \"set_for\": \"single\"}}', NULL, 0, 1, 1, 0);

-- --------------------------------------------------------

--
-- Struttura della tabella `temp_plot`
--

CREATE TABLE `temp_plot` (
  `id` int NOT NULL,
  `plot_type` varchar(45) NOT NULL,
  `usecase` varchar(45) NOT NULL,
  `plot_name` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `plot_data` longtext NOT NULL,
  `labels` longtext NOT NULL,
  `stats_enable` varchar(11) NOT NULL DEFAULT 'global',
  `stats_list` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `user_files`
--

CREATE TABLE `user_files` (
  `id` int NOT NULL,
  `filename` varchar(128) DEFAULT NULL,
  `filepath` varchar(128) DEFAULT 'user',
  `username` varchar(45) DEFAULT NULL,
  `date_exp` datetime DEFAULT NULL,
  `ext` varchar(45) DEFAULT NULL,
  `filetype` varchar(45) DEFAULT NULL,
  `status_exp` varchar(45) DEFAULT 'nd',
  `comment_exp` longtext,
  `parinfo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `sourcename` varchar(45) NOT NULL,
  `exp_tstart` datetime DEFAULT NULL,
  `exp_tstop` datetime DEFAULT NULL,
  `plot_id` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `config_files`
--
ALTER TABLE `config_files`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `hktm_efd_params`
--
ALTER TABLE `hktm_efd_params`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indici per le tabelle `hktm_fake_params`
--
ALTER TABLE `hktm_fake_params`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indici per le tabelle `local_files`
--
ALTER TABLE `local_files`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `operation_modes`
--
ALTER TABLE `operation_modes`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `plots`
--
ALTER TABLE `plots`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indici per le tabelle `pwd_reset_tmp`
--
ALTER TABLE `pwd_reset_tmp`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `report_files`
--
ALTER TABLE `report_files`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `running_reports`
--
ALTER TABLE `running_reports`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indici per le tabelle `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indici per le tabelle `stored_files`
--
ALTER TABLE `stored_files`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`),
  ADD KEY `user_idx` (`username`);

--
-- Indici per le tabelle `stored_plots`
--
ALTER TABLE `stored_plots`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_2` (`id`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `systems`
--
ALTER TABLE `systems`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `temp_plot`
--
ALTER TABLE `temp_plot`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_2` (`id`),
  ADD KEY `id` (`id`);

--
-- Indici per le tabelle `user_files`
--
ALTER TABLE `user_files`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `config_files`
--
ALTER TABLE `config_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `history`
--
ALTER TABLE `history`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `hktm_efd_params`
--
ALTER TABLE `hktm_efd_params`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT per la tabella `hktm_fake_params`
--
ALTER TABLE `hktm_fake_params`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `local_files`
--
ALTER TABLE `local_files`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1683;

--
-- AUTO_INCREMENT per la tabella `members`
--
ALTER TABLE `members`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `operation_modes`
--
ALTER TABLE `operation_modes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT per la tabella `plots`
--
ALTER TABLE `plots`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `pwd_reset_tmp`
--
ALTER TABLE `pwd_reset_tmp`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT per la tabella `report_files`
--
ALTER TABLE `report_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `running_reports`
--
ALTER TABLE `running_reports`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13846;

--
-- AUTO_INCREMENT per la tabella `statistics`
--
ALTER TABLE `statistics`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=145;

--
-- AUTO_INCREMENT per la tabella `stored_files`
--
ALTER TABLE `stored_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `stored_plots`
--
ALTER TABLE `stored_plots`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `systems`
--
ALTER TABLE `systems`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT per la tabella `temp_plot`
--
ALTER TABLE `temp_plot`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT per la tabella `user_files`
--
ALTER TABLE `user_files`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

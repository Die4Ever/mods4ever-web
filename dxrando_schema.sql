-- MariaDB dump 10.19  Distrib 10.6.7-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: dxrando
-- ------------------------------------------------------
-- Server version	10.6.7-MariaDB-2ubuntu1.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `deaths`
--

DROP TABLE IF EXISTS `deaths`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deaths` (
  `log_id` int(10) unsigned DEFAULT NULL,
  `name` varchar(1000) DEFAULT NULL,
  `killer` varchar(1000) DEFAULT NULL,
  `killerclass` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `damagetype` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `x` float DEFAULT NULL,
  `y` float DEFAULT NULL,
  `z` float DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3794 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `map` varchar(1000) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `version` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `message` varchar(30000) CHARACTER SET latin1 DEFAULT NULL,
  `seed` int(10) unsigned DEFAULT NULL,
  `flagshash` int(10) unsigned DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `modname` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `firstword` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `playthrough_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `map` (`map`,`created`),
  KEY `modname` (`modname`,`created`),
  KEY `firstword` (`firstword`,`created`),
  KEY `modname_2` (`modname`,`seed`,`playthrough_id`,`created`),
  KEY `playthrough_id` (`playthrough_id`,`map`,`created`)
) ENGINE=InnoDB AUTO_INCREMENT=254807 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `old_logs`
--

DROP TABLE IF EXISTS `old_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `old_logs` (
  `message` varchar(30000) DEFAULT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `map` varchar(255) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `version` varchar(255) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `map` (`map`,`created`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-02 23:55:30

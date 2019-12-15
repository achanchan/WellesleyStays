-- MySQL dump 10.14  Distrib 5.5.64-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: wstays_db
-- ------------------------------------------------------
-- Server version	5.5.64-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `availability`
--

DROP TABLE IF EXISTS `availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `availability` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `start` date NOT NULL DEFAULT '0000-00-00',
  `end` date DEFAULT NULL,
  PRIMARY KEY (`aid`,`start`),
  KEY `pid` (`pid`),
  CONSTRAINT `availability_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `place` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `availability`
--

LOCK TABLES `availability` WRITE;
/*!40000 ALTER TABLE `availability` DISABLE KEYS */;
INSERT INTO `availability` VALUES (1,1,'2019-11-28','2019-12-01'),(2,1,'2019-12-18','2019-12-24'),(3,2,'2020-01-01','2020-06-01'),(15,32,'2019-12-09','2019-12-13'),(16,33,'2019-12-18','2019-12-20'),(17,34,'2019-12-12','2019-12-13');
/*!40000 ALTER TABLE `availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `place`
--

DROP TABLE IF EXISTS `place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `place` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `bnumber` char(9) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `street1` varchar(40) DEFAULT NULL,
  `street2` varchar(40) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `maxguest` int(11) DEFAULT NULL,
  `postalcode` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `bnumber` (`bnumber`),
  CONSTRAINT `place_ibfk_1` FOREIGN KEY (`bnumber`) REFERENCES `user` (`bnumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `place`
--

LOCK TABLES `place` WRITE;
/*!40000 ALTER TABLE `place` DISABLE KEYS */;
INSERT INTO `place` VALUES (1,'B20856852','Lexington','USA','49 Eldred Street','','MA',4,'02420'),(2,'B20856852','Wellesley','USA','106 Central Street','Bates 407','MA',1,'02481'),(3,'B20860410','Wellesley','USA','106 Central Street','Munger 234','MA',1,'02481'),(4,'B20860410','Elmhurst','USA','5101 Jacobus Street','','NY',1,'11373'),(5,'B20857037','Wellesley','USA','106 Central Street','McAfee 118','MA',1,'02481'),(6,'B20857037','Los Altos','USA','470 Gabilan Street','Apartment 4','CA',1,'94022'),(32,'B20856852','springfield','USA','142 evergreen terrace','','XY',2,'12345'),(33,'B20856852','Wellesley ','USA','My House Street','12','MA',4,'02481'),(34,'B20857037','Wellesley','USA','MY House Stree','','MA',1,'');
/*!40000 ALTER TABLE `place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `request` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `bnumber` char(9) DEFAULT NULL,
  `isfilled` tinyint(1) NOT NULL DEFAULT '0',
  `guestnum` int(11) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `start` date DEFAULT NULL,
  `end` date DEFAULT NULL,
  PRIMARY KEY (`rid`),
  KEY `bnumber` (`bnumber`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`bnumber`) REFERENCES `user` (`bnumber`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,'B20860410',0,2,'Montreal','CAN','2019-11-29','2019-11-30'),(2,'B20857037',1,2,'Singapore','SGP','2019-12-25','2020-01-01'),(3,'B20856852',0,3,'Seattle','USA','2019-12-04','2019-12-25');
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `bnumber` char(9) NOT NULL DEFAULT '',
  `email` varchar(30) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  `countrycode` varchar(3) DEFAULT NULL,
  `phonenum` char(10) DEFAULT NULL,
  PRIMARY KEY (`bnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('B12341234','scott@wellesley.edu','Scott',NULL,'3249'),('B12345679','apple@wellesley.edu','a',NULL,'5'),('B20856852','dhahm@wellesley.edu','Debbie Hahm','1','7813541150'),('B20857037','nli2@wellesley.edu','Nicole Li','1','6503808687'),('B20857039','sboy@wellesley.edu','Soulja Boy',NULL,'6789998212'),('B20860410','achan@wellesley.edu','Amy Chan','1','6462401065');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-11 15:20:34

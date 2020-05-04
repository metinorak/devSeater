-- MySQL dump 10.16  Distrib 10.1.37-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: devseater
-- ------------------------------------------------------
-- Server version	10.1.37-MariaDB

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
-- Table structure for table `contactMessages`
--

DROP TABLE IF EXISTS `contactMessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contactMessages` (
  `cmid` int(11) NOT NULL AUTO_INCREMENT,
  `subject` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `message` text COLLATE utf8_turkish_ci NOT NULL,
  `email` text COLLATE utf8_turkish_ci NOT NULL,
  `name` text COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`cmid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `followers` (
  `flwrid` int(11) NOT NULL,
  `flwdid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`flwrid`,`flwdid`),
  KEY `flwdid` (`flwdid`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`flwrid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`flwdid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `globalAdmins`
--

DROP TABLE IF EXISTS `globalAdmins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `globalAdmins` (
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`uid`),
  CONSTRAINT `globalAdmins_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `isRead` tinyint(1) NOT NULL DEFAULT '0',
  `message` text COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `receiver_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `isDeletedBySender` tinyint(1) DEFAULT '0',
  `isDeletedByReceiver` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`mid`),
  KEY `receiver_id` (`receiver_id`),
  KEY `sender_id` (`sender_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`uid`) ON DELETE NO ACTION,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`uid`) ON DELETE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `nfid` int(11) NOT NULL,
  `type` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `related_id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `actor_uid` int(11) NOT NULL,
  `isRead` tinyint(1) NOT NULL DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`nfid`),
  UNIQUE KEY `actor_uid` (`actor_uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`actor_uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectAdmins`
--

DROP TABLE IF EXISTS `projectAdmins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectAdmins` (
  `uid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`uid`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `projectAdmins_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `projectAdmins_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectLinks`
--

DROP TABLE IF EXISTS `projectLinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectLinks` (
  `plid` int(11) NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `link` text COLLATE utf8_turkish_ci NOT NULL,
  `pid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`plid`),
  UNIQUE KEY `plid` (`plid`,`pid`),
  KEY `pid` (`pid`),
  CONSTRAINT `projectLinks_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectPostCommentLikes`
--

DROP TABLE IF EXISTS `projectPostCommentLikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectPostCommentLikes` (
  `ppcid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`ppcid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `projectPostCommentLikes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `projectPostCommentLikes_ibfk_2` FOREIGN KEY (`ppcid`) REFERENCES `projectPostComments` (`ppcid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectPostComments`
--

DROP TABLE IF EXISTS `projectPostComments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectPostComments` (
  `ppcid` int(11) NOT NULL AUTO_INCREMENT,
  `ppid` int(11) NOT NULL,
  `comment` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ppcid`),
  KEY `ppid` (`ppid`),
  KEY `uid` (`uid`),
  CONSTRAINT `projectPostComments_ibfk_1` FOREIGN KEY (`ppid`) REFERENCES `projectPosts` (`ppid`) ON DELETE CASCADE,
  CONSTRAINT `projectPostComments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectPostLikes`
--

DROP TABLE IF EXISTS `projectPostLikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectPostLikes` (
  `ppid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`ppid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `projectPostLikes_ibfk_1` FOREIGN KEY (`ppid`) REFERENCES `projectPosts` (`ppid`) ON DELETE CASCADE,
  CONSTRAINT `projectPostLikes_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projectPosts`
--

DROP TABLE IF EXISTS `projectPosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projectPosts` (
  `ppid` int(11) NOT NULL AUTO_INCREMENT,
  `post` text COLLATE utf8_turkish_ci NOT NULL,
  `pid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ppid`),
  KEY `uid` (`uid`),
  KEY `pid` (`pid`),
  CONSTRAINT `projectPosts_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `projectPosts_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(50) COLLATE utf8_turkish_ci NOT NULL,
  `short_description` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `full_description` text COLLATE utf8_turkish_ci NOT NULL,
  `photo` tinytext COLLATE utf8_turkish_ci,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`),
  UNIQUE KEY `project_name` (`project_name`),
  UNIQUE KEY `project_name_2` (`project_name`),
  UNIQUE KEY `project_name_3` (`project_name`),
  UNIQUE KEY `project_name_4` (`project_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seaterAspirations`
--

DROP TABLE IF EXISTS `seaterAspirations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seaterAspirations` (
  `uid` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `isRejected` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`,`sid`),
  KEY `sid` (`sid`),
  CONSTRAINT `seaterAspirations_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `seaterAspirations_ibfk_2` FOREIGN KEY (`sid`) REFERENCES `seaters` (`sid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seaterSkills`
--

DROP TABLE IF EXISTS `seaterSkills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seaterSkills` (
  `sid` int(11) NOT NULL,
  `skid` int(11) NOT NULL,
  PRIMARY KEY (`sid`,`skid`),
  KEY `skid` (`skid`),
  CONSTRAINT `seaterSkills_ibfk_2` FOREIGN KEY (`skid`) REFERENCES `skills` (`skid`) ON DELETE CASCADE,
  CONSTRAINT `seaterSkills_ibfk_3` FOREIGN KEY (`sid`) REFERENCES `seaters` (`sid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seaters`
--

DROP TABLE IF EXISTS `seaters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seaters` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `short_description` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `full_description` text COLLATE utf8_turkish_ci,
  `title` varchar(48) COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sid`),
  UNIQUE KEY `sid` (`sid`,`pid`),
  KEY `uid` (`uid`),
  KEY `pid` (`pid`),
  CONSTRAINT `seaters_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE SET NULL,
  CONSTRAINT `seaters_ibfk_3` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `skills` (
  `skid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_turkish_ci NOT NULL,
  PRIMARY KEY (`skid`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userLinks`
--

DROP TABLE IF EXISTS `userLinks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userLinks` (
  `ulid` int(11) NOT NULL AUTO_INCREMENT,
  `name` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `link` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ulid`),
  UNIQUE KEY `ulid` (`ulid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `userLinks_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userPostCommentLikes`
--

DROP TABLE IF EXISTS `userPostCommentLikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userPostCommentLikes` (
  `upcid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`upcid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `userPostCommentLikes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `userPostCommentLikes_ibfk_2` FOREIGN KEY (`upcid`) REFERENCES `userPostComments` (`upcid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userPostComments`
--

DROP TABLE IF EXISTS `userPostComments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userPostComments` (
  `upcid` int(11) NOT NULL AUTO_INCREMENT,
  `upid` int(11) NOT NULL,
  `comment` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`upcid`),
  KEY `upid` (`upid`),
  KEY `uid` (`uid`),
  CONSTRAINT `userPostComments_ibfk_1` FOREIGN KEY (`upid`) REFERENCES `userPosts` (`upid`) ON DELETE CASCADE,
  CONSTRAINT `userPostComments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userPostLikes`
--

DROP TABLE IF EXISTS `userPostLikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userPostLikes` (
  `upid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  PRIMARY KEY (`upid`,`uid`),
  KEY `uid` (`uid`),
  CONSTRAINT `userPostLikes_ibfk_1` FOREIGN KEY (`upid`) REFERENCES `userPosts` (`upid`) ON DELETE CASCADE,
  CONSTRAINT `userPostLikes_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userPosts`
--

DROP TABLE IF EXISTS `userPosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userPosts` (
  `upid` int(11) NOT NULL AUTO_INCREMENT,
  `post` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`upid`),
  KEY `uid` (`uid`),
  CONSTRAINT `userPosts_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userSkills`
--

DROP TABLE IF EXISTS `userSkills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userSkills` (
  `uid` int(11) NOT NULL,
  `skid` int(11) NOT NULL,
  PRIMARY KEY (`uid`,`skid`),
  KEY `skid` (`skid`),
  CONSTRAINT `userSkills_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  CONSTRAINT `userSkills_ibfk_2` FOREIGN KEY (`skid`) REFERENCES `skills` (`skid`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(150) COLLATE utf8_turkish_ci NOT NULL,
  `username` varchar(48) COLLATE utf8_turkish_ci NOT NULL,
  `registration_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `password` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `photo` tinytext COLLATE utf8_turkish_ci,
  `bio` text COLLATE utf8_turkish_ci,
  `full_name` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `isEmailVerified` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-04  5:04:54

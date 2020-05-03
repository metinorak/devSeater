-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 03, 2020 at 07:10 PM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.1.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `devseater`
--

-- --------------------------------------------------------

--
-- Table structure for table `contactMessages`
--

CREATE TABLE `contactMessages` (
  `cmid` int(11) NOT NULL,
  `subject` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `message` text COLLATE utf8_turkish_ci NOT NULL,
  `email` text COLLATE utf8_turkish_ci NOT NULL,
  `name` text COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `followers`
--

CREATE TABLE `followers` (
  `flwrid` int(11) NOT NULL,
  `flwdid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `globalAdmins`
--

CREATE TABLE `globalAdmins` (
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `mid` int(11) NOT NULL,
  `isRead` tinyint(1) NOT NULL DEFAULT '0',
  `message` text COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `receiver_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `isDeletedBySender` tinyint(1) DEFAULT '0',
  `isDeletedByReceiver` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `nfid` int(11) NOT NULL,
  `type` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `related_id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `actor_uid` int(11) NOT NULL,
  `isRead` tinyint(1) NOT NULL DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectAdmins`
--

CREATE TABLE `projectAdmins` (
  `uid` int(11) NOT NULL,
  `pid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectLinks`
--

CREATE TABLE `projectLinks` (
  `plid` int(11) NOT NULL,
  `name` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `link` text COLLATE utf8_turkish_ci NOT NULL,
  `pid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectPostCommentLikes`
--

CREATE TABLE `projectPostCommentLikes` (
  `ppcid` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectPostComments`
--

CREATE TABLE `projectPostComments` (
  `ppcid` int(11) NOT NULL,
  `ppid` int(11) NOT NULL,
  `comment` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectPostLikes`
--

CREATE TABLE `projectPostLikes` (
  `ppid` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projectPosts`
--

CREATE TABLE `projectPosts` (
  `ppid` int(11) NOT NULL,
  `post` text COLLATE utf8_turkish_ci NOT NULL,
  `pid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `pid` int(11) NOT NULL,
  `project_name` varchar(50) COLLATE utf8_turkish_ci NOT NULL,
  `short_description` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `full_description` text COLLATE utf8_turkish_ci NOT NULL,
  `photo` tinytext COLLATE utf8_turkish_ci,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seaterAspirations`
--

CREATE TABLE `seaterAspirations` (
  `uid` int(11) NOT NULL,
  `sid` int(11) NOT NULL,
  `isRejected` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seaters`
--

CREATE TABLE `seaters` (
  `sid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `short_description` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `full_description` text COLLATE utf8_turkish_ci,
  `title` varchar(48) COLLATE utf8_turkish_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seaterSkills`
--

CREATE TABLE `seaterSkills` (
  `sid` int(11) NOT NULL,
  `skid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

CREATE TABLE `skills` (
  `skid` int(11) NOT NULL,
  `name` varchar(80) COLLATE utf8_turkish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userLinks`
--

CREATE TABLE `userLinks` (
  `ulid` int(11) NOT NULL,
  `name` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `link` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userPostCommentLikes`
--

CREATE TABLE `userPostCommentLikes` (
  `upcid` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userPostComments`
--

CREATE TABLE `userPostComments` (
  `upcid` int(11) NOT NULL,
  `upid` int(11) NOT NULL,
  `comment` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userPostLikes`
--

CREATE TABLE `userPostLikes` (
  `upid` int(11) NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userPosts`
--

CREATE TABLE `userPosts` (
  `upid` int(11) NOT NULL,
  `post` text COLLATE utf8_turkish_ci NOT NULL,
  `uid` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `uid` int(11) NOT NULL,
  `email` varchar(150) COLLATE utf8_turkish_ci NOT NULL,
  `username` varchar(48) COLLATE utf8_turkish_ci NOT NULL,
  `registration_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `password` tinytext COLLATE utf8_turkish_ci NOT NULL,
  `photo` tinytext COLLATE utf8_turkish_ci,
  `bio` text COLLATE utf8_turkish_ci,
  `full_name` varchar(100) COLLATE utf8_turkish_ci NOT NULL,
  `isEmailVerified` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `userSkills`
--

CREATE TABLE `userSkills` (
  `uid` int(11) NOT NULL,
  `skid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contactMessages`
--
ALTER TABLE `contactMessages`
  ADD PRIMARY KEY (`cmid`);

--
-- Indexes for table `followers`
--
ALTER TABLE `followers`
  ADD PRIMARY KEY (`flwrid`,`flwdid`),
  ADD KEY `flwdid` (`flwdid`);

--
-- Indexes for table `globalAdmins`
--
ALTER TABLE `globalAdmins`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`mid`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`nfid`),
  ADD UNIQUE KEY `actor_uid` (`actor_uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `projectAdmins`
--
ALTER TABLE `projectAdmins`
  ADD PRIMARY KEY (`uid`,`pid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `projectLinks`
--
ALTER TABLE `projectLinks`
  ADD PRIMARY KEY (`plid`),
  ADD UNIQUE KEY `plid` (`plid`,`pid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `projectPostCommentLikes`
--
ALTER TABLE `projectPostCommentLikes`
  ADD PRIMARY KEY (`ppcid`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `projectPostComments`
--
ALTER TABLE `projectPostComments`
  ADD PRIMARY KEY (`ppcid`),
  ADD KEY `ppid` (`ppid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `projectPostLikes`
--
ALTER TABLE `projectPostLikes`
  ADD PRIMARY KEY (`ppid`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `projectPosts`
--
ALTER TABLE `projectPosts`
  ADD PRIMARY KEY (`ppid`),
  ADD KEY `uid` (`uid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`pid`),
  ADD UNIQUE KEY `project_name` (`project_name`),
  ADD UNIQUE KEY `project_name_2` (`project_name`),
  ADD UNIQUE KEY `project_name_3` (`project_name`),
  ADD UNIQUE KEY `project_name_4` (`project_name`);

--
-- Indexes for table `seaterAspirations`
--
ALTER TABLE `seaterAspirations`
  ADD PRIMARY KEY (`uid`,`sid`),
  ADD KEY `sid` (`sid`);

--
-- Indexes for table `seaters`
--
ALTER TABLE `seaters`
  ADD PRIMARY KEY (`sid`),
  ADD UNIQUE KEY `sid` (`sid`,`pid`),
  ADD KEY `uid` (`uid`),
  ADD KEY `pid` (`pid`);

--
-- Indexes for table `seaterSkills`
--
ALTER TABLE `seaterSkills`
  ADD PRIMARY KEY (`sid`,`skid`),
  ADD KEY `skid` (`skid`);

--
-- Indexes for table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`skid`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `userLinks`
--
ALTER TABLE `userLinks`
  ADD PRIMARY KEY (`ulid`),
  ADD UNIQUE KEY `ulid` (`ulid`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `userPostCommentLikes`
--
ALTER TABLE `userPostCommentLikes`
  ADD PRIMARY KEY (`upcid`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `userPostComments`
--
ALTER TABLE `userPostComments`
  ADD PRIMARY KEY (`upcid`),
  ADD KEY `upid` (`upid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `userPostLikes`
--
ALTER TABLE `userPostLikes`
  ADD PRIMARY KEY (`upid`,`uid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `userPosts`
--
ALTER TABLE `userPosts`
  ADD PRIMARY KEY (`upid`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `userSkills`
--
ALTER TABLE `userSkills`
  ADD PRIMARY KEY (`uid`,`skid`),
  ADD KEY `skid` (`skid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contactMessages`
--
ALTER TABLE `contactMessages`
  MODIFY `cmid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `mid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projectLinks`
--
ALTER TABLE `projectLinks`
  MODIFY `plid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projectPostComments`
--
ALTER TABLE `projectPostComments`
  MODIFY `ppcid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projectPosts`
--
ALTER TABLE `projectPosts`
  MODIFY `ppid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `seaters`
--
ALTER TABLE `seaters`
  MODIFY `sid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `skills`
--
ALTER TABLE `skills`
  MODIFY `skid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userLinks`
--
ALTER TABLE `userLinks`
  MODIFY `ulid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userPostComments`
--
ALTER TABLE `userPostComments`
  MODIFY `upcid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `userPosts`
--
ALTER TABLE `userPosts`
  MODIFY `upid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `followers`
--
ALTER TABLE `followers`
  ADD CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`flwrid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`flwdid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `globalAdmins`
--
ALTER TABLE `globalAdmins`
  ADD CONSTRAINT `globalAdmins_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`uid`) ON DELETE NO ACTION,
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`uid`) ON DELETE NO ACTION;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`actor_uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `projectAdmins`
--
ALTER TABLE `projectAdmins`
  ADD CONSTRAINT `projectAdmins_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `projectAdmins_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`);

--
-- Constraints for table `projectLinks`
--
ALTER TABLE `projectLinks`
  ADD CONSTRAINT `projectLinks_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`);

--
-- Constraints for table `projectPostCommentLikes`
--
ALTER TABLE `projectPostCommentLikes`
  ADD CONSTRAINT `projectPostCommentLikes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `projectPostCommentLikes_ibfk_2` FOREIGN KEY (`ppcid`) REFERENCES `projectPostComments` (`ppcid`) ON DELETE CASCADE;

--
-- Constraints for table `projectPostComments`
--
ALTER TABLE `projectPostComments`
  ADD CONSTRAINT `projectPostComments_ibfk_1` FOREIGN KEY (`ppid`) REFERENCES `projectPosts` (`ppid`) ON DELETE CASCADE,
  ADD CONSTRAINT `projectPostComments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `projectPostLikes`
--
ALTER TABLE `projectPostLikes`
  ADD CONSTRAINT `projectPostLikes_ibfk_1` FOREIGN KEY (`ppid`) REFERENCES `projectPosts` (`ppid`) ON DELETE CASCADE,
  ADD CONSTRAINT `projectPostLikes_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `projectPosts`
--
ALTER TABLE `projectPosts`
  ADD CONSTRAINT `projectPosts_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `projectPosts_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`);

--
-- Constraints for table `seaterAspirations`
--
ALTER TABLE `seaterAspirations`
  ADD CONSTRAINT `seaterAspirations_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `seaterAspirations_ibfk_2` FOREIGN KEY (`sid`) REFERENCES `seaters` (`sid`) ON DELETE CASCADE;

--
-- Constraints for table `seaters`
--
ALTER TABLE `seaters`
  ADD CONSTRAINT `seaters_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE SET NULL,
  ADD CONSTRAINT `seaters_ibfk_3` FOREIGN KEY (`pid`) REFERENCES `projects` (`pid`);

--
-- Constraints for table `seaterSkills`
--
ALTER TABLE `seaterSkills`
  ADD CONSTRAINT `seaterSkills_ibfk_2` FOREIGN KEY (`skid`) REFERENCES `skills` (`skid`) ON DELETE CASCADE,
  ADD CONSTRAINT `seaterSkills_ibfk_3` FOREIGN KEY (`sid`) REFERENCES `seaters` (`sid`) ON DELETE CASCADE;

--
-- Constraints for table `userLinks`
--
ALTER TABLE `userLinks`
  ADD CONSTRAINT `userLinks_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `userPostCommentLikes`
--
ALTER TABLE `userPostCommentLikes`
  ADD CONSTRAINT `userPostCommentLikes_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `userPostCommentLikes_ibfk_2` FOREIGN KEY (`upcid`) REFERENCES `userPostComments` (`upcid`) ON DELETE CASCADE;

--
-- Constraints for table `userPostComments`
--
ALTER TABLE `userPostComments`
  ADD CONSTRAINT `userPostComments_ibfk_1` FOREIGN KEY (`upid`) REFERENCES `userPosts` (`upid`) ON DELETE CASCADE,
  ADD CONSTRAINT `userPostComments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `userPostLikes`
--
ALTER TABLE `userPostLikes`
  ADD CONSTRAINT `userPostLikes_ibfk_1` FOREIGN KEY (`upid`) REFERENCES `userPosts` (`upid`) ON DELETE CASCADE,
  ADD CONSTRAINT `userPostLikes_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `userPosts`
--
ALTER TABLE `userPosts`
  ADD CONSTRAINT `userPosts_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `userSkills`
--
ALTER TABLE `userSkills`
  ADD CONSTRAINT `userSkills_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`) ON DELETE CASCADE,
  ADD CONSTRAINT `userSkills_ibfk_2` FOREIGN KEY (`skid`) REFERENCES `skills` (`skid`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

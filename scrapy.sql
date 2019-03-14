/*
Navicat MySQL Data Transfer

Source Server         : 47.99.47.160
Source Server Version : 80015
Source Host           : 47.99.47.160:3306
Source Database       : scrapy

Target Server Type    : MYSQL
Target Server Version : 80015
File Encoding         : 65001

Date: 2019-03-14 23:05:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `article`
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siteid` int(11) NOT NULL,
  `sitename` varchar(50) NOT NULL,
  `articleid` varchar(100) NOT NULL,
  `articlename` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `onlyid` varchar(100) NOT NULL,
  `lastedtime` int(11) DEFAULT NULL,
  `lastedname` varchar(100) DEFAULT NULL,
  `isfull` tinyint(4) DEFAULT '0',
  `isvip` tinyint(4) DEFAULT '0',
  `votes` int(11) DEFAULT '0',
  `articleurl` varchar(500) DEFAULT NULL,
  `chaptersize` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `od` (`onlyid`)
) ENGINE=MyISAM AUTO_INCREMENT=112939 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for `site`
-- ----------------------------
DROP TABLE IF EXISTS `site`;
CREATE TABLE `site` (
  `siteid` int(11) NOT NULL AUTO_INCREMENT,
  `sitename` varchar(50) DEFAULT NULL,
  `belong` int(11) DEFAULT NULL,
  `pages` int(11) DEFAULT NULL,
  PRIMARY KEY (`siteid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of site
-- ----------------------------
INSERT INTO `site` VALUES ('1', 'zhuishubang', null, null);
INSERT INTO `site` VALUES ('2', 'biqugecc', null, null);

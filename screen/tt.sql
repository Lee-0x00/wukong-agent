/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50536
Source Host           : localhost:3306
Source Database       : tt

Target Server Type    : MYSQL
Target Server Version : 50536
File Encoding         : 65001

Date: 2017-12-19 16:18:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `name` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('test', '111111');
INSERT INTO `user` VALUES ('admin', 'admin');

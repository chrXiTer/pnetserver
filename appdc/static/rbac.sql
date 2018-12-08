
CREATE DATABASE `vhr` DEFAULT CHARACTER SET utf8mb4;

USE `vhr`;

/*
 Navicat Premium Data Transfer

 Source Server         : docker-mysql
 Source Server Type    : MySQL
 Source Server Version : 50641
 Source Host           : localhost
 Source Database       : vhr

 Target Server Type    : MySQL
 Target Server Version : 50641
 File Encoding         : utf-8

 Date: 09/09/2018 16:27:50 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `ua_res`
-- ----------------------------
DROP TABLE IF EXISTS `ua_res`;
CREATE TABLE `ua_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `ua_res_role`
-- ----------------------------
DROP TABLE IF EXISTS `ua_res_role`;
CREATE TABLE `ua_res_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `res_name` varchar(100) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`),
  UNIQUE KEY `res_name` (`res_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `ua_role`
-- ----------------------------
DROP TABLE IF EXISTS `ua_role`;
CREATE TABLE `ua_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100)  NOT NULL,
  `comment` varchar(255)  NOT NULL COMMENT '角色名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `ua_user`
-- ----------------------------
DROP TABLE IF EXISTS `ua_user`;
CREATE TABLE `ua_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '人员id',
  `name` varchar(100) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `showname` varchar(32) DEFAULT NULL COMMENT '显示名',
  `phone` varchar(12) DEFAULT NULL COMMENT '手机号码',
  `email` varchar(20) DEFAULT NULL COMMENT '邮箱',
  `userface` varchar(255) DEFAULT NULL COMMENT '头像',
  `user_type` int(11) DEFAULT '3',
  `enabled` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `ua_user_role`
-- ----------------------------
DROP TABLE IF EXISTS `ua_user_role`;
CREATE TABLE `ua_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

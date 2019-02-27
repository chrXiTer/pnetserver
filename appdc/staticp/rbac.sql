
CREATE DATABASE `pnet` DEFAULT CHARACTER SET utf8mb4;

USE `pnet`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


DROP TABLE IF EXISTS `ua_res`;
CREATE TABLE `ua_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `ua_role`;
CREATE TABLE `ua_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100)  NOT NULL,
  `comment` varchar(255)  NOT NULL COMMENT '角色显示名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `ua_user`;
CREATE TABLE `ua_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `account` varchar(100) NOT NULL COMMENT '与id类似-不可变-应用系统生成',
  `username` varchar(100) NOT NULL COMMENT '用户名-可用于登录或显示-唯一',
  `phone` varchar(12) DEFAULT NULL COMMENT '手机号码',
  `email` varchar(20) DEFAULT NULL COMMENT '邮箱',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `nickname` varchar(32) DEFAULT "" COMMENT '昵称-可用于显示-可重复',
  `userface` varchar(255) DEFAULT "" COMMENT '头像',
  `usertype` int(11) DEFAULT '3',
  `status` int(11) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`)
  UNIQUE KEY `username` (`username`)
  UNIQUE KEY `phone` (`phone`)
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `ua_res_role`;
CREATE TABLE `ua_res_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `res_name` varchar(100) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `res_name_role` (`res_name`,`role_name`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `ua_user_role`;
CREATE TABLE `ua_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name_role` (`user_name`,`role_name`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

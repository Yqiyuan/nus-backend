/*
 Navicat Premium Data Transfer

 Source Server         : ali-nus
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : 8.130.49.155:3306
 Source Schema         : nus

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 23/07/2021 11:25:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for meals
-- ----------------------------
DROP TABLE IF EXISTS `meals`;
CREATE TABLE `meals`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `image_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `calories` float(11, 0) NULL DEFAULT NULL,
  `fat` float(11, 0) NULL DEFAULT NULL,
  `protein` float(11, 0) NULL DEFAULT NULL,
  `carbs` float(11, 0) NULL DEFAULT NULL,
  `weight` double NULL DEFAULT NULL,
  `meal_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'breakfast, lunch, dinner, other',
  `valid` binary(1) NULL DEFAULT NULL COMMENT '1 for valid',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;

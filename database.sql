DROP  DATABASE IF EXISTS `evote`;
CREATE DATABASE `evote`;
USE `evote`;

-- ---
-- Table 'user'
-- 
-- ---

DROP TABLE IF EXISTS `user`;
		
CREATE TABLE `user` (
  `user_id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(100) NOT NULL,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(40) NOT NULL,
  `vcode` VARCHAR(40) NOT NULL,
  `is_verified` TINYINT(1) NOT NULL DEFAULT 0,
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY (`email`)
);

-- ---
-- Table 'poll'
-- 
-- ---

DROP TABLE IF EXISTS `poll`;

CREATE TABLE `poll` (
  `poll_id` INTEGER(50) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  `description` MEDIUMTEXT NOT NULL,
  `created` DATETIME NOT NULL,
  `ends` DATETIME NOT NULL,
  `state` MEDIUMTEXT NOT NULL,
  `public_key` VARCHAR(500) NOT NULL,
  `private_key` VARCHAR(700) DEFAULT NULL,
  PRIMARY KEY (`poll_id`)
);

-- ---
-- Table 'vote'
-- 
-- ---

DROP TABLE IF EXISTS `vote`;
		
CREATE TABLE `vote` (
  `poll_id` INTEGER(50) NOT NULL,
  `user_id` INTEGER(50) NOT NULL,
  `value` VARCHAR(300) DEFAULT NULL,
  PRIMARY KEY (`poll_id`, `user_id`)
);

-- ---
-- Table 'polladmin'
-- 
-- ---

DROP TABLE IF EXISTS `polladmin`;
		
CREATE TABLE `polladmin` (
  `poll_id` INTEGER(50) NOT NULL,
  `user_id` INTEGER(50) NOT NULL,
  `key_chunk` VARCHAR(300) NOT NULL,
  PRIMARY KEY (`poll_id`, `user_id`),
  KEY (`poll_id`)
);

-- ---
-- Table 'choice'
-- choice 
-- ---

DROP TABLE IF EXISTS `choice`;
		
CREATE TABLE `choice` (
  `poll_id` INTEGER(50) NOT NULL,
  `choice_id` INTEGER NOT NULL,
  `choice_value` VARCHAR(300) NOT NULL,
  `choice_result` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`choice_id`, `poll_id`),
  KEY (`poll_id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `vote` ADD FOREIGN KEY (poll_id) REFERENCES `poll` (`poll_id`);
ALTER TABLE `vote` ADD FOREIGN KEY (user_id) REFERENCES `user` (`user_id`);
ALTER TABLE `polladmin` ADD FOREIGN KEY (poll_id) REFERENCES `poll` (`poll_id`);
ALTER TABLE `polladmin` ADD FOREIGN KEY (user_id) REFERENCES `user` (`user_id`);
ALTER TABLE `choice` ADD FOREIGN KEY (poll_id) REFERENCES `poll` (`poll_id`);

-- ---
-- Table Properties
-- ---

ALTER TABLE `user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
ALTER TABLE `poll` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
ALTER TABLE `vote` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
ALTER TABLE `polladmin` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
ALTER TABLE `choice` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `user` (`user_id`,`email`,`username`,`password`,`vcode`,`is_verified `,`is_admin`) VALUES
-- ('','','','','','','');
-- INSERT INTO `poll` (`poll_id`,`name`,`description`,`created`,`ends`,`state`,`public_key`,`private_key`) VALUES
-- ('','','','','','','','');
-- INSERT INTO `vote` (`poll_id`,`user_id`,`value`) VALUES
-- ('','','');
-- INSERT INTO `polladmin` (`poll_id`,`user_id`,`key_chunk `) VALUES
-- ('','','');
-- INSERT INTO `choice` (`poll_id`,`choice_id`,`choice_value`,`choice_result`) VALUES
-- ('','','','');


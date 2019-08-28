CREATE DATABASE `intoj_rebuild` CHARACTER SET utf8;

use intoj_rebuild;

CREATE TABLE users(
	`id` INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`username` VARCHAR(30),
	`password` VARCHAR(64),
	`salt` VARCHAR(64),
	`email` VARCHAR(100) DEFAULT NULL,
	`sex` INT(2) DEFAULT 0,
	`motto` VARCHAR(1024) DEFAULT NULL,
	`realname` VARCHAR(32) DEFAULT NULL,
	`background-url` VARCHAR(256) DEFAULT NULL,
	`rating` INT(10) DEFAULT 1500
);

CREATE TABLE user_privileges(
	`id` INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`username` VARCHAR(30),
	`privilege` VARCHAR(60)
);

CREATE TABLE problems(
	`id` INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`title` VARCHAR(100),
	`description` MEDIUMTEXT,
	`input_format` MEDIUMTEXT,
	`output_format` MEDIUMTEXT,
	`example` MEDIUMTEXT,
	`limit_and_hint` MEDIUMTEXT,
	`time_limit` INT,
	`memory_limit` INT,
	`is_public` TINYINT(1) DEFAULT 1
);

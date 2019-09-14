CREATE DATABASE `intoj` CHARACTER SET utf8;

use intoj;

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
	`username` VARCHAR(30) NOT NULL,
	`privilege` VARCHAR(32)
);
/*
权限列表：
system_admin
problemset_manager
problem_owner
problem_tag_manager
user_manager
contest_manager
contest_owner
*/

CREATE TABLE problems(
	`id` INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`title` VARCHAR(100),
	`background` MEDIUMTEXT,
	`description` MEDIUMTEXT,
	`input_format` MEDIUMTEXT,
	`output_format` MEDIUMTEXT,
	`limit_and_hint` MEDIUMTEXT,
	`time_limit` INT,
	`memory_limit` INT,
	`is_public` TINYINT(1) DEFAULT 0,
	`provider` VARCHAR(30)
);

CREATE TABLE problem_examples(
	`id` INT UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`problem_id` INT,
	`kth` INT,
	`input` MEDIUMTEXT,
	`output` MEDIUMTEXT,
	`explanation` MEDIUMTEXT
);

CREATE TABLE submissions(
	`id`            INT NOT NULL PRIMARY KEY auto_increment,
	`problem_id`    INT NOT NULL,
	`contest_id`    INT DEFAULT 0,
	`submitter`     VARCHAR(30),
	`submit_time`   DATETIME,
	`language`      VARCHAR(20),
	`status`        INT DEFAULT 1,
	`score`         DOUBLE DEFAULT 0,
	`detail`        LONGTEXT DEFAULT '',
	`time_usage`    INT DEFAULT 0,
	`memory_usage`  INT DEFAULT 0,
	`code`          MEDIUMTEXT,
	`compilier_message` LONGTEXT DEFAULT '',
	`system_message`    TEXT DEFAULT ''
);

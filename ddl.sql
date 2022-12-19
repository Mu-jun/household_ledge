create database HouseholdLedge character set utf8mb4 collate utf8mb4_general_ci;
use HouseholdLedge;

CREATE TABLE `Bookmark`
(
    `id`    bigint NOT NULL,
    `member_id`    bigint NOT NULL,
    `amount`    int NOT NULL,
    `memo`    varchar(1000) NOT NULL,
 PRIMARY KEY ( `id` )
);


CREATE TABLE `HouseholdLedge`
(
    `id`    bigint NOT NULL,
    `member_id`    bigint NOT NULL,
    `date`    datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `amout`    int DEFAULT 0 NOT NULL,
    `memo`    varchar(1000) DEFAULT '' NOT NULL,
 PRIMARY KEY ( `id` )
);


CREATE TABLE `Member`
(
    `id`    bigint NOT NULL,
    `email`    varchar(100) NOT NULL,
    `password`    varchar(250) NOT NULL,
 PRIMARY KEY ( `id` )
);


CREATE TABLE `ShortUrl`
(
	`short_url`    varchar(25) NOT NULL,
    `target_url`    varchar(2100) NOT NULL,
    `expire_date`    DATETIME NOT NULL,
 PRIMARY KEY ( `short_url` )
);

ALTER TABLE `ShortUrl`
 ADD CONSTRAINT `ShortUrl_UK` UNIQUE ( `target_url` );
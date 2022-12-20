create database HouseholdLedge character set utf8mb4 collate utf8mb4_general_ci;
use HouseholdLedge;
CREATE TABLE `Bookmark`
(
    `id`    bigint UNSIGNED NOT NULL AUTO_INCREMENT,
    `member_id`    bigint NOT NULL,
    `amount`    int NOT NULL,
    `memo`    varchar(1000) NOT NULL,
 PRIMARY KEY ( `id` )
);

CREATE INDEX `Bookmark_member_idx` ON `Bookmark`
( `member_id` );


CREATE TABLE `HouseholdLedge`
(
    `id`    bigint UNSIGNED NOT NULL AUTO_INCREMENT,
    `member_id`    bigint NOT NULL,
    `date`    datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `amount`    int DEFAULT 0 NOT NULL,
    `memo`    varchar(1000) DEFAULT '' NOT NULL,
 PRIMARY KEY ( `id` )
);

CREATE INDEX `HouseholdLedge_member_idx` ON `HouseholdLedge`
( `member_id` );


CREATE TABLE `Member`
(
    `id`    bigint UNSIGNED NOT NULL AUTO_INCREMENT,
    `email`    varchar(100) NOT NULL,
    `password`    varchar(250) NOT NULL,
 PRIMARY KEY ( `id` )
);

CREATE UNIQUE INDEX `Member_UK` ON `Member`
( `email` );


CREATE TABLE `ShortUrl`
(
    `short_url`    varchar(20) NOT NULL,
    `target_url`    varchar(2100) NOT NULL,
    `expire_date`    DATETIME NOT NULL,
 PRIMARY KEY ( `short_url` )
);

CREATE UNIQUE INDEX `ShortUrl_PK` ON `ShortUrl`
( `short_url` );
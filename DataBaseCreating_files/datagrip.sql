CREATE DATABASE IF NOT EXISTS quera_project1;
USE Transfermarkt;

DROP TABLE IF EXISTS `Club_Statistics`;
DROP TABLE IF EXISTS `Player_Statistics`;
DROP TABLE IF EXISTS `transfer`;
DROP TABLE IF EXISTS `player_club`;
DROP TABLE IF EXISTS `Awards_Winners`;
DROP TABLE IF EXISTS `club_Stadium`;
DROP TABLE IF EXISTS `club`;
DROP TABLE IF EXISTS `player`;
DROP TABLE IF EXISTS `Awards`;
DROP TABLE IF EXISTS `Coach`;
DROP TABLE IF EXISTS `Stadium`;


CREATE TABLE `Awards`(
    `id` varchar(8) NOT NULL,
    `name` varchar(128) NOT NULL ,
    PRIMARY KEY (`id`));

CREATE TABLE `club`(
    `id` varchar(8) NOT NULL,
    `name` varchar(128) NOT NULL ,
    `country` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`));


CREATE TABLE `Stadium`(
    `Stadium_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`Stadium_id`));

CREATE TABLE `club_Stadium`
(
    `id`         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `Stadium_id` BIGINT          NOT NULL,
    `club_id`    varchar(8)      NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club` (`id`),
    FOREIGN KEY (`Stadium_id`) REFERENCES `stadium`(`Stadium_id`)
);


CREATE TABLE `Awards_Winners`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `award_id` varchar(8) NOT NULL,
    `club_id` varchar(8) NOT NULL,
    `season` varchar(8) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`),
    FOREIGN KEY (`award_id`) REFERENCES `Awards`(`id`)
);

CREATE TABLE `club_statistics`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `club_id` varchar(8) NOT NULL,
    `league` varchar(255),
    `season` varchar(8) NOT NULL,
    `income` DECIMAL(15, 2) ,
    `Expenditure` DECIMAL(15, 2) ,
    `overall_balance` DECIMAL(15, 2),
    `Average age of players` DOUBLE(8, 2),
    `ARRIVALS` INT,
    `DEPARTURES` INT,
    `Total market value` DECIMAL(15, 2),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`)
);

CREATE TABLE `player`(
    `id` varchar(8) NOT NULL,
    `full_name` VARCHAR(255) NOT NULL,
    `birth_date` DATETIME,
    `height` DOUBLE(8, 2) ,
    `foot` ENUM(''),
    `main_position` varchar(255),
    `goals_scored` INT(11),
    `goals_assisted` INT(11),
    `goals_conceded` INT(11),
    `clean_sheets` INT(11),
    `total_appearence` INT(11),
    `agent` VARCHAR(255),
     PRIMARY KEY (`id`));

CREATE TABLE `transfer`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` varchar(8) NOT NULL,
    `season` varchar(8) NOT NULL,
    `date` DATE,
    `left` varchar(8),
    `joined` varchar(8),
    `mv` DECIMAL(15, 2),
    `fee` DECIMAL(15, 2),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
    FOREIGN KEY (`left`) REFERENCES `club`(`id`),
    FOREIGN KEY (`joined`) REFERENCES `club`(`id`)
);

CREATE TABLE `player_statistics`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` varchar(8) NOT NULL,
    `club_id` VARCHAR(8),
    `contract_expires` DATETIME,
    `position` VARCHAR(8),
    `season` INT NOT NULL,
    `squad` INT,
    `own_goals` INT,
    `substitution_on` INT,
    `substitution_off` INT ,
    `yellow_cards` INT ,
    `second_yellow_cards` INT,
    `red_cards` INT,
    `penalty_goals` INT,
    `minutes_per_goal` INT,
    `minutes_played` INT,
    `current_international` VARCHAR(255),
    `goals_scored` varchar(255) ,
    `goals_assisted` varchar(255) ,
    `goals_conceded` varchar(255),
    `clean_sheets`   varchar(255),
    `appearance` varchar(255),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`)
);

CREATE TABLE `matches`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
   `host_id` Varchar(8) NOT NULL,
   `guest_id` varchar(8) NOT NULL,
   `host_result` VARCHAR(8),
   `score`  VARCHAR(8),
   `match_id` VARCHAR(8),
   `goals_for` INT,
   `goals_against` INT,
   `season` INT,
   `match_date` DATE,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`host_id`) REFERENCES `club`(`id`),
    FOREIGN KEY (`guest_id`) REFERENCES `club`(`id`)
);



# CREATE TABLE `player_club`(
#     `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
#     `player_id` varchar(8) NOT NULL,
#     `club_id` varchar(8) NOT NULL,
#     `season` BIGINT NOT NULL,
#     `position` ENUM('') ,
#     `Contract expires` DATE,
#     `market_value` DECIMAL(15, 2),
#     `joined` DATE,
#     `signed_from` VARCHAR(8),
#     PRIMARY KEY (`id`),
#     FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
#     FOREIGN KEY (`club_id`) REFERENCES `club`(`id`),
#     FOREIGN KEY (`signed_from`) REFERENCES `club`(`id`)
# );


















CREATE DATABASE IF NOT EXISTS Transfermarkt;
USE Transfermarkt;
DROP TABLE IF EXISTS `club`;
CREATE TABLE `club`(
    `id` varchar(8) NOT NULL,
    `name` varchar(128) NOT NULL ,
    `country` VARCHAR(255) NOT NULL,
    `income` DECIMAL(15, 2) NOT NULL,
    `Expenditure` DECIMAL(15, 2) NOT NULL,
    `overall_balance` DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (`id`));

DROP TABLE IF EXISTS `player`;

CREATE TABLE `player`(
    `id` varchar(8) NOT NULL,
    `full_name` VARCHAR(255) NOT NULL,
    `birth_date` DATETIME NOT NULL,
    `height` DOUBLE(8, 2) NOT NULL,
    `current_international` VARCHAR(255) NOT NULL,
    `main_position` VARCHAR(255) NOT NULL,
    `foot` ENUM('') NOT NULL,
    `current_club` INT NOT NULL,
    `goals_scored` BIGINT NOT NULL,
    `goals_assisted` BIGINT NOT NULL,
    `total_appearance` BIGINT NOT NULL,
    `agent` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`));

DROP TABLE IF EXISTS `club_statistics`;

CREATE TABLE `club_statistics`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `club_id` varchar(8) NOT NULL,
    `league` INT NOT NULL,
    `season` ENUM('') NOT NULL,
    `cup_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`)
);

DROP TABLE IF EXISTS `transfer`;

CREATE TABLE `transfer`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `season` ENUM('') NOT NULL,
    `date` DATE NOT NULL,
    `left` varchar(255) NOT NULL,
    `joined` varchar(255) NOT NULL,
    `mv` BIGINT NOT NULL,
    `fee` BIGINT NOT NULL,
    `player_id` varchar(8) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `player`(`id`)
);

DROP TABLE IF EXISTS `player_statistics`;

CREATE TABLE `player_statistics`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` varchar(8) NOT NULL,
    `club_id` varchar(8) NOT NULL,
    `season` ENUM('') NOT NULL,
    `appearance` INT NOT NULL,
    `goals` INT NOT NULL,
    `assists` INT NOT NULL,
    `own_goals` INT NOT NULL,
    `substitution_on` INT NOT NULL,
    `substitution_off` INT NOT NULL,
    `yellow_cards` INT NOT NULL,
    `second_yellow_cards` INT NOT NULL,
    `red_cards` BIGINT NOT NULL,
    `penalty_goals` BIGINT NOT NULL,
    `minutes_per_goal` BIGINT NOT NULL,
    `minutes_played` BIGINT NOT NULL,
    `league` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`)
);

DROP TABLE IF EXISTS `player_club`;

CREATE TABLE `player_club`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` varchar(8) NOT NULL,
    `club_id` varchar(8) NOT NULL,
    `season` BIGINT NOT NULL,
    `position` ENUM('') NOT NULL,
    `age` BIGINT NOT NULL,
    `joined` DATE NOT NULL,
    `signed_from` varchar(255) NOT NULL,
    `contract` DATE NOT NULL,
    `market_value` DECIMAL(15, 2) NOT NULL,
    `loan_from` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`player_id`) REFERENCES `player`(`id`),
    FOREIGN KEY (`club_id`) REFERENCES `club`(`id`)
);

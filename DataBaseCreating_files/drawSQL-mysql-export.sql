CREATE TABLE `club`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `country` VARCHAR(255) NOT NULL,
    `market_value` BIGINT NOT NULL,
    `income` BIGINT NOT NULL,
    `Expenditure` BIGINT NOT NULL,
    `overall_balance` BIGINT NOT NULL,
    `founded` BIGINT NOT NULL
);
ALTER TABLE
    `club` ADD PRIMARY KEY(`id`);
CREATE TABLE `player`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NULL,
    `birth_date` DATETIME NOT NULL,
    `height` DOUBLE(8, 2) NOT NULL,
    `current_international` VARCHAR(255) NOT NULL,
    `main_position` VARCHAR(255) NOT NULL,
    `foot` ENUM('') NOT NULL,
    `current_club` INT NOT NULL,
    `goals_scored` BIGINT NOT NULL,
    `goals_assisted` BIGINT NOT NULL,
    `total_appearance` BIGINT NOT NULL,
    `agent` VARCHAR(255) NOT NULL
);
ALTER TABLE
    `player` ADD PRIMARY KEY(`id`);
CREATE TABLE `club_statistics`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `club_id` INT NOT NULL,
    `league` INT NOT NULL,
    `season` ENUM('') NOT NULL,
    `cup_name` VARCHAR(255) NOT NULL
);
ALTER TABLE
    `club_statistics` ADD PRIMARY KEY(`id`);
CREATE TABLE `transfer`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `season` ENUM('') NOT NULL,
    `date` DATE NOT NULL,
    `left` INT NOT NULL,
    `joined` INT NOT NULL,
    `mv` BIGINT NOT NULL,
    `fee` BIGINT NOT NULL,
    `player_id` BIGINT NOT NULL
);
ALTER TABLE
    `transfer` ADD PRIMARY KEY(`id`);
CREATE TABLE `player_statistics`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` INT NOT NULL,
    `club_id` INT NOT NULL,
    `season` ENUM('') NOT NULL,
    `appearance` INT NOT NULL,
    `goals` INT NULL,
    `assists` INT NULL,
    `own_goals` INT NOT NULL,
    `substitution_on` INT NULL,
    `substitution_off` INT NULL,
    `yellow_cards` INT NOT NULL,
    `second_yellow_cards` INT NULL,
    `red_cards` BIGINT NOT NULL,
    `penalty_goals` BIGINT NOT NULL,
    `minutes_per_goal` BIGINT NOT NULL,
    `minutes_played` BIGINT NOT NULL,
    `league` VARCHAR(255) NOT NULL
);
ALTER TABLE
    `player_statistics` ADD PRIMARY KEY(`id`);
CREATE TABLE `player_club`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `player_id` BIGINT NOT NULL,
    `club_id` BIGINT NOT NULL,
    `season` BIGINT NOT NULL,
    `position` ENUM('') NOT NULL,
    `age` BIGINT NOT NULL,
    `joined` DATE NOT NULL,
    `signed_from` INT NOT NULL,
    `contract` DATE NOT NULL,
    `market_value` BIGINT NOT NULL,
    `loan_from` INT NOT NULL
);
ALTER TABLE
    `player_club` ADD PRIMARY KEY(`id`);
ALTER TABLE
    `club_statistics` ADD CONSTRAINT `club_statistics_club_id_foreign` FOREIGN KEY(`club_id`) REFERENCES `club`(`id`);
ALTER TABLE
    `player_club` ADD CONSTRAINT `player_club_player_id_foreign` FOREIGN KEY(`player_id`) REFERENCES `player`(`id`);
ALTER TABLE
    `transfer` ADD CONSTRAINT `transfer_left_foreign` FOREIGN KEY(`left`) REFERENCES `club`(`id`);
ALTER TABLE
    `transfer` ADD CONSTRAINT `transfer_joined_foreign` FOREIGN KEY(`joined`) REFERENCES `club`(`id`);
ALTER TABLE
    `player_statistics` ADD CONSTRAINT `player_statistics_club_id_foreign` FOREIGN KEY(`club_id`) REFERENCES `club`(`id`);
ALTER TABLE
    `transfer` ADD CONSTRAINT `transfer_player_id_foreign` FOREIGN KEY(`player_id`) REFERENCES `player`(`id`);
ALTER TABLE
    `player_club` ADD CONSTRAINT `player_club_signed_from_foreign` FOREIGN KEY(`signed_from`) REFERENCES `club`(`id`);
ALTER TABLE
    `player_club` ADD CONSTRAINT `player_club_loan_from_foreign` FOREIGN KEY(`loan_from`) REFERENCES `club`(`id`);
ALTER TABLE
    `player_statistics` ADD CONSTRAINT `player_statistics_player_id_foreign` FOREIGN KEY(`player_id`) REFERENCES `player`(`id`);
ALTER TABLE
    `player_club` ADD CONSTRAINT `player_club_club_id_foreign` FOREIGN KEY(`club_id`) REFERENCES `club`(`id`);

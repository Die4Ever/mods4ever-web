
DROP TABLE IF EXISTS `old_leaderboard_data`;
RENAME TABLE IF EXISTS `leaderboard_data` TO `old_leaderboard_data`;

CREATE TABLE leaderboard_data (
    log_id INT UNSIGNED NOT NULL,
    `name` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
    `value` VARCHAR(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
    --`int_val` INT,
    PRIMARY KEY (`log_id`, `name`)
);

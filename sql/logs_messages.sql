
DROP TABLE IF EXISTS `old_logs_messages`;
RENAME TABLE IF EXISTS `logs_messages` TO `old_logs_messages`;

CREATE TABLE logs_messages (
    id INT UNSIGNED NOT NULL,
    `message` VARCHAR(30000) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
    PRIMARY KEY (`id`)
);

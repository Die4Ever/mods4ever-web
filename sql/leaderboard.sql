DROP TABLE IF EXISTS `old_leaderboard`;
RENAME TABLE IF EXISTS `leaderboard` TO `old_leaderboard`;

CREATE TABLE leaderboard (
    log_id INT UNSIGNED NOT NULL,
    totaltime INT UNSIGNED NOT NULL,
    gametime INT UNSIGNED NOT NULL,
    score INT NOT NULL,
    name VARCHAR(1000) NOT NULL,
    setseed BOOL NOT NULL,
    rando_difficulty DECIMAL(5,2) NOT NULL,
    combat_difficulty DECIMAL(5,2) NOT NULL,
    deaths INT UNSIGNED NOT NULL,
    loads INT UNSIGNED NOT NULL,
    saves INT UNSIGNED NOT NULL,
    bingos INT UNSIGNED NOT NULL,
    bingo_spots INT UNSIGNED NOT NULL,
    ending INT UNSIGNED NOT NULL,
    newgameplus_loops INT UNSIGNED NOT NULL,
    initial_version INT UNSIGNED NOT NULL,
    PRIMARY KEY(log_id),
    KEY(score)
);

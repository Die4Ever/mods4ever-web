DROP TABLE IF EXISTS `old_leaderboard`;
RENAME TABLE IF EXISTS `leaderboard` TO `old_leaderboard`;

CREATE TABLE leaderboard (
    log_id INT UNSIGNED,
    totaltime INT UNSIGNED,
    gametime INT UNSIGNED,
    score INT,
    flagshash INT,
    name VARCHAR(1000),
    setseed BOOL,
    stable_version BOOL,
    rando_difficulty DECIMAL(5,2),
    combat_difficulty DECIMAL(5,2),
    deaths INT UNSIGNED,
    loads INT UNSIGNED,
    saves INT UNSIGNED,
    bingos INT UNSIGNED,
    bingo_spots INT UNSIGNED,
    ending INT UNSIGNED,
    newgameplus_loops INT UNSIGNED,
    initial_version INT UNSIGNED,
    PRIMARY KEY(log_id),
    KEY(score),
    KEY(flagshash, score)
);

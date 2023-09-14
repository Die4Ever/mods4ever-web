
import json
from dxlog.base import get_config
from dxlog.db import QueryLeaderboard, GroupLeaderboard, db_connect

def leaderboard(SortBy='score'):
    config = get_config()
    if config and config.get('database'):
        db = db_connect(config)
        cursor = db.cursor(dictionary=True)
        leaderboard = QueryLeaderboard(cursor, {}, None, 1000, SortBy=SortBy)
    else:
        with open('leaderboardtest.json') as f:
            cursor = json.load(f)
        leaderboard = GroupLeaderboard(cursor, {}, None, 1000)
    
    keys = ['name', 'score', 'totaltime', 'seed', 'flagshash', 'setseed', 'place', 'playthrough_id']
    ret = []
    for run in leaderboard:
        run = zip(keys, run)
        ret.append(dict(run))
    return ret

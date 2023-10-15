
import json
from dxlog.base import get_config
from dxlog.db import QueryLeaderboard, GroupLeaderboard, db_connect, get_data

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
    
    ret = []
    for run in leaderboard:
        if config and config.get('database') and cursor:
            data = get_data(cursor, run['log_id'], run)
            run.update(data)
        run.pop('ip')
        ret.append(run)
    return ret

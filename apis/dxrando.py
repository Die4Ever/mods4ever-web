
import json
from dxlog.base import get_config, unrealscript_sanitize
from dxlog.db import _QueryLeaderboard, QueryLeaderboard, GroupLeaderboard, db_connect, get_data, write_leaderboard_data

def leaderboard(SortBy='score', Grouped=True):
    config = get_config()
    if config and config.get('database'):
        db = db_connect(config)
        cursor = db.cursor(dictionary=True)
        _QueryLeaderboard(cursor, SortBy=SortBy)
    else:
        with open('leaderboardtest.json') as f:
            cursor = json.load(f)

    if Grouped not in (False, 'False', 'false'):
        leaderboard = GroupLeaderboard(cursor, {}, None, 1000)
    else:
        leaderboard = []
        place = 1
        for (d) in cursor:
            name = unrealscript_sanitize(d['name'])
            leaderboard.append({ **d, 'name': name, 'place': place })
            place += 1
    
    ret = []
    for run in leaderboard:
        if config and config.get('database') and cursor:
            run = get_data(cursor, run['log_id'], run)
            write_leaderboard_data(cursor, run['log_id'], run)
        run.pop('ip', None)
        ret.append(run)
    return ret

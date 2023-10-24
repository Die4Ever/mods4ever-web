
import json
from dxlog.base import ToHex, get_config, unrealscript_sanitize
from dxlog.db import _QueryLeaderboard, GroupLeaderboard, db_connect

def leaderboard(SortBy='score', Grouped=True, GameMode=-1):
    config = get_config()
    Filters = {'GameMode': GameMode}
    if config and config.get('database'):
        db = db_connect(config)
        cursor = db.cursor(dictionary=True)
        _QueryLeaderboard(cursor, SortBy=SortBy, Filters=Filters)
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
        run.pop('ip', None)
        run['playthrough_id'] = ToHex(run.get('playthrough_id', 0))
        run['flagshash'] = ToHex(run.get('flagshash', 0))
        ret.append(run)

    if config and config.get('database'):
        cursor.close()
        db.close()

    return ret

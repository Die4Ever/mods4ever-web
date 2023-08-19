
from dxlog.base import get_config
from dxlog.db import _QueryLeaderboard, GroupLeaderboard, db_connect

def leaderboard(SortBy='score'):
    config = get_config()
    if config and config.get('database'):
        db = db_connect(config)
        cursor = db.cursor(dictionary=True)
        leaderboard = _QueryLeaderboard(cursor, {}, 0, 100, SortBy=SortBy)
    else:
        cursor = [
            dict(name='testrun1', playthrough_id=1, score=9002, time=10000, seed=123, flagshash=123, setseed=1),
            dict(name='testrun2', playthrough_id=123, score=9001, time=40000, seed=123, flagshash=123, setseed=1),
            dict(name='testrun3', playthrough_id=1234, score=9000, time=90015, seed=123, flagshash=123, setseed=1),
        ]
        leaderboard = GroupLeaderboard(cursor, {}, 0, 100)
    
    keys = ['name', 'score', 'time', 'seed', 'flagshash', 'setseed', 'place', 'playthrough_id']
    ret = []
    for run in leaderboard:
        run = zip(keys, run)
        ret.append(dict(run))
    return ret

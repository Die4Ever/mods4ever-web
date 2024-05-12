
import json
import sys
import urllib
from dxlog.base import ToHex, VersionStringToInt, get_config, unrealscript_sanitize
from dxlog.db import _QueryLeaderboard, GroupLeaderboard, db_connect

def leaderboard(SortBy='score', Grouped=True, GameMode=-1, version='v2.3.0.0'):
    config = get_config()
    Filters = {'GameMode': GameMode}
    version = VersionStringToInt(version, silent=True)
    if not version:
        version = None
    if config and config.get('database'):
        db = db_connect(config)
        cursor = db.cursor(dictionary=True)
        _QueryLeaderboard(cursor, version=version, SortBy=SortBy, Filters=Filters)
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


def read_binary_content(data:bytes) -> str:
    try:
        return data.decode('utf-8','ignore')
    except Exception as e:
        print(e, file=sys.stderr)
        return data.decode('iso_8859_1','ignore')
    return data.decode()

def saveContentToFile(content):
    cleanContent = urllib.parse.unquote_plus(content)
    cleanContent = cleanContent.lstrip("bingo=")
    f = open("public/bingo.txt", 'w')
    f.write(cleanContent)
    f.close()

def writebingo(data):
    content = read_binary_content(data)
    content = content.replace('\x00','').replace('\r','')
    saveContentToFile(content)
    response = {'status': "ok received "+str(len(data))+" bytes"}
    print('writebingo', response, file=sys.stderr)
    return response

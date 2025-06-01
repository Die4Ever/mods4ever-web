
import json
import sys
import urllib
from apis import NewsItem
from dxlog.base import ToHex, VersionStringToInt, VersionToInt, get_config, unrealscript_sanitize
from dxlog.db import _QueryLeaderboard, GroupLeaderboard, db_connect

def leaderboard(SortBy='score', Grouped=True, GameMode=-1, version='v2.3.0.0'):
    config = get_config()
    Filters = {'GameMode': GameMode}
    version = VersionStringToInt(version, silent=True)
    if not version:
        version = VersionToInt(2,3,0,0)
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
    f = open("public/bingo.txt", 'w')
    f.write(content)
    f.close()

def writebingo(data):
    content = read_binary_content(data)
    content = content.replace('\x00','').replace('\r','')
    try:
        content = json.loads(content)
        content = json.dumps(content, indent=4)
    except Exception as e:
        return {'error': 'invalid json'}, 400
    saveContentToFile(content)
    response = {'status': "ok received "+str(len(data))+" bytes"}
    print('writebingo', response, file=sys.stderr)
    return response


def dxrando_news():
    news = []

    news.append(NewsItem('2025-06-01', "v3.5 This One's Got Legs",
    [   "Unless you use the 'Speed Enhancement' loadout, you will now start with the new Running Enhancement aug instead.",
        "Many new goals rando locations, including Gordon Quick's location.",
        "New 'The Three Leg Augs' loadout with new augs.",
        "New 'My Vision Is Augmented' loadout with new augs.",
        "New 'Speedrun Training' game mode.",
        "New 'Strong Augs' game mode.",
        "New speedrun timer option for WaltonWare, for use on speedrun.com/dxrando",
    ]))
    
    news.append(NewsItem('2025-03-26', "v3.4.1 Hotfix",
    [   "TNT in Battery Park subway is no longer shuffled with goals rando disabled",
        "Disabled randomizing the guy with the East Gate key in M03 Airfield if goals rando is disabled",
        "Fixed In-Game Settings menu for some of the flags at the bottom",
        "Fixed medbot/repairbot stat rando consistency",
        "Fixed Smuggler's call button in Revision",
    ]))

    news.append(NewsItem('2025-03-19', "v3.4 We Welcome All",
    [   "Normal Randomizer game mode has been renamed to Full Randomizer, and the new Normal Randomizer mode is the new default",
        "Zero Rando now disables many more balance changes, making it a great way to play Deus Ex for the first time",
        "Multiple, rotating quicksave slots",
        "Slowed down WaltonWare difficulty increases",
        "New menu to change current game settings",
        "New loadouts and improvements to old ones",
        "Tweaks to The Merchant items and pricing, now selling more relevant items with more appropriate prices",
    ]))

    news.append(NewsItem('2025-01-06', "v3.3.1 Bug Fixes",
    [   "You must now pet Starr instead of simply visiting her for bingo",
        "Fixed bug where game would end if you completed a bingo line without a Bingo Win setting configured",
        "Deus Ex: Revision support improved more (may have some oddities with old saves until reaching a new map)",
    ]))

    news.append(NewsItem('2024-12-11', "v3.3 Mr. Page's Mean Bingo Machine",
    [   "Mr. Page's Mean Bingo Machine: A new mode where you play through the whole game, but must complete a set number of bingo lines before being allowed to progress to the next mission. Once you get to the next mission, you are given a new bingo board!",
        "One Item Mode: Our new dumbest game mode! All items in a map will be replaced with a single type of item (eg. all flares, all biocells, or all beers)",
        "Augs can now receive randomized slots (so speed can be an eye aug) (look in the Advanced New Game menu)",
        "Deus Ex: Revision support is massively improved as a whole",
    ]))

    news.append(NewsItem('2024-10-29', "v3.2.4 Halloween Bug Fixes",
    [   "Fixed Mr. H from counting in the M04 raid enemy counter",
        "Fixed zombie Howards preventing Silo from completing",
        "Some fixes for endgame cutscenes and NG+",
        "We've seen some confusion with Limited Fixed Saves. When you have a Memory Containment Unit in your inventory (or 2 for the new Extreme version) you only need to have the box highlight on the computer and then you can use the normal Save Game menu or Quicksave button. The only freebie autosave you get is at the very start of the game. Make sure to save before going to Battery Park! Sometimes you might want to backtrack to save. Remember that if you die not all is lost, because you now have a better plan!",
    ]))
    
    return news

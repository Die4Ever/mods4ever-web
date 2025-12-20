
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

    news.append(NewsItem('2025-12-19', "v3.6.7 All I Want For Christmas Is Bug Fixes",
    [   "The sewer exit leaving the inside of the Mission 9 dry dock now has a keypad instead of a button in modes outside of Entrance Randomizer. The keypad uses Jenny's number, so the code can be found in the dockyards.",
        "The location of Jock is now randomized when leaving the graveyard at the end of Mission 9.",
    ]))

    news.append(NewsItem('2025-10-10', "v3.6.6.6 Happy Halloween 2025!",
    [   "Added new Stalker types! Read the wiki for hints on how to deal with them.",
        "New game mode: Mr. Page's Horrifying Bingo Machine",
        "Fixed and/or Limited Saves modes now get emergency autosaves for crashes and when exiting the game, same as WaltonWare Hardcore",
    ]))

    news.append(NewsItem('2025-09-18', "v3.6.1 Welcome Back, Walt!",
    [   "Fixed Area 51 Sectors 2 and 3 goals rando locations not working",
        "The Ballistic Protection aug now uses slightly less energy (when Augs Balance Changes are enabled), and has a shorter auto linger time (when Semi-Automatic Augs are enabled)",
        "On WaltonWare Gas Station, Ocean Lab, and Silo starts you can backtrack to Carla in Vandenberg (at the vanilla start, on the roof of the Command Center) to get the Vandenberg map",
    ]))

    news.append(NewsItem('2025-08-21', "v3.6 Time to Get Serious",
    [   "New game mode Serious Rando: disables memes and silly goal locations.",
        "New game mode WaltonWare Hardcore: saving is disabled, and there is no healing!",
        "Options for auto enabling auto augs when installed.",
        "Pool tables are much improved.",
        "Added scaling and blackout options for scopes and binoculars, with a cool automatic 'Fit to Screen' option that doesn't rely on fixed size textures and adapts to any screen resolution/ratio.",
    ]))

    news.append(NewsItem('2025-06-02', "v3.5.1 Bingo Hotfix",
    [   "Fixed issue with dolphin jumps breaking some other bingo goals.",
        "June 22nd will be an all Deus Ex day on Sum of Besties.",
        "We're looking for speedrunners!  If you can beat the game in under 3 hours, or do more than 4 WaltonWare loops in 1 hour, contact us!",
    ], andMore=False))

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

    return news

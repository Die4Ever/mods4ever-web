import autoinstaller
from typeguard import typechecked, install_import_hook

from dxlog.db import _GetLeaderboardPlacement# functions starting with an underscore aren't imported in *
install_import_hook('dxlog')
from dxlog.base import *
from dxlog.db import *
from dxlog.parsing import *
from dxlog.twitter import *
from dxlog.request import *
from dxlog.deaths import *
from better_profanity import profanity
import unittest
import datetime

@typechecked
class TestLog(unittest.TestCase):
	def test_parse_content(self):
		d = parse_content("""DX.DXRando0: RandoEnter() firstTime: True, IsTravel: False, seed: 601088 DX
INFO: DX.DXRando0: randomizing DX using seed 601088
INFO: DX.DXRFlags0: PreFirstEntry DX DeusEx.DXRFlags - v1.7.3.5 Beta, seed: 601088, flagshash: 90622488, playthrough_id: 1686707255, flagsversion: 1070305, gamemode: 0, difficulty: 1.000000, loadout: 0, brightness: 15, newgameplus_loops: 0, autosave: 2, crowdcontrol: 0, codes_mode: 2
DEATH: 01_NYC_UNATCOIsland.JCDentonMale8: JC Denton was killed by JCDentonMale JC Denton with exploded damage in 01_NYC_UNATCOISLAND (748.419373,-433.573730,-123.300003)
INFO: 01_NYC_UNATCOIsland.JCDentonMale8: Speed Enhancement deactivated""")
		print(d['firstword'])
		self.assertEqual(d['firstword'], "PreFirstEntry")
		self.assertEqual(len(d.keys()), 17, 'found correct number of keys')

		d = parse_content("""INFO: 01_NYC_UNATCOIsland.DXRando14: RandoEnter() firstTime: False, IsTravel: False, seed: 828672 01_NYC_UNATCOISLAND
INFO: 01_NYC_UNATCOIsland.DXRFlags14: AnyEntry 01_NYC_UNATCOISLAND GMDXRandomizer.DXRFlags - version: v1.8.0.1 Beta, flagshash: 1595221376, seed: 828672, autosave: 0, brightness: 15, crowdcontrol: 0, loadout: 0, codes_mode: 0, newgameplus_loops: 0, playthrough_id: 1920337562, gamemode: 0, difficulty: 0, minskill: 1, maxskill: 5, ammo: 90
INFO: 01_NYC_UNATCOIsland.DXRFlags14: multitools: 90, lockpicks: 90, biocells: 90, speedlevel: 4, keys: 4, keys_containers: 0, doorspickable: 100, doorsdestructible: 100, deviceshackable: 100, passwordsrandomized: 100, medkits: 90, enemiesrandomized: 20, hiddenenemiesrandomized: 0, enemiesshuffled: 100, infodevices: 100, infodevices_containers: 0
INFO: 01_NYC_UNATCOIsland.DXRFlags14: dancingpercent: 25, doorsmode: 513, enemyrespawn: 0, skills_disable_downgrades: 0, skills_reroll_missions: 1, skills_independent_levels: 0, startinglocations: 100, goals: 100, equipment: 5, medbots: 100, repairbots: 100, medbotuses: 0, repairbotuses: 0, medbotcooldowns: 1, repairbotcooldowns: 1, medbotamount: 1
INFO: 01_NYC_UNATCOIsland.DXRFlags14: AnyEntry 01_NYC_UNATCOISLAND repairbotamount: 1, turrets_move: 100, turrets_add: 50, merchants: 100, banned_skills: 5, banned_skill_level: 5, enemies_nonhumans: 60, swapitems: 100, swapcontainers: 100, augcans: 100, aug_value_rando: 100, skill_value_rando: 100, min_weapon_dmg: 50, max_weapon_dmg: 150, min_weapon_shottime: 50, max_weapon_shottime: 150
INFO: 01_NYC_UNATCOIsland.DXRTelemetry13: health: 100, HealthLegLeft: 100, HealthLegRight: 100, HealthTorso: 100, HealthHead: 100, HealthArmLeft: 100, HealthArmRight: 100
""")
		print(repr(d))
		print(d['firstword'])
		self.assertEqual(d['firstword'], "AnyEntry")
		self.assertEqual(len(d.keys()), 74, 'found correct number of keys')

		d = parse_content("""INFO: 00_Intro.DXRando6: RandoEnter() firstTime: True, IsTravel: True, seed: 0 INTRO
INFO: 00_Intro.DXRando6: randomizing INTRO using seed 0
INFO: 00_Intro.DXRFlags5: PreFirstEntry INTRO DeusEx.DXRFlags - version: v2.4.0.3, flagshash: 781491456, seed: 0, playthrough_id: -1427472606, maxrando: 0, autosave: 2, crowdcontrol: 0, loadout: 0, newgameplus_loops: 0, gamemode: 4, setseed: 1, difficulty: 1, minskill: 85, maxskill: 85, ammo: 100, multitools: 100, lockpicks: 100
INFO: 00_Intro.DXRFlags5: biocells: 100, speedlevel: 0, keys: 0, keys_containers: 0, doorspickable: 0, doorsdestructible: 0, deviceshackable: 0, passwordsrandomized: 0, medkits: 100, enemiesrandomized: 0, enemystats: 0, hiddenenemiesrandomized: 0, enemiesshuffled: 0, infodevices: 0, infodevices_containers: 0, dancingpercent: 0
INFO: 00_Intro.DXRFlags5: doorsmode: 771, enemyrespawn: 0, skills_disable_downgrades: 0, skills_reroll_missions: 0, skills_independent_levels: 0, startinglocations: 0, goals: 0, equipment: 0, medbots: -1, repairbots: -1, medbotuses: 10, repairbotuses: 10, medbotcooldowns: 0, repairbotcooldowns: 0, medbotamount: 0, repairbotamount: 0
INFO: 00_Intro.DXRFlags5: turrets_move: 0, turrets_add: 0, merchants: 0, banned_skills: 0, banned_skill_level: 0, enemies_nonhumans: 0, bot_weapons: 0, bot_stats: 0, swapitems: 0, swapcontainers: 0, augcans: 0, aug_value_rando: 0, skill_value_rando: 0, min_weapon_dmg: 100, max_weapon_dmg: 100, min_weapon_shottime: 100, max_weapon_shottime: 100
INFO: 00_Intro.DXRFlags5: PreFirstEntry INTRO prison_pocket: 0, bingo_win: 0, bingo_freespaces: 1, spoilers: 1, menus_pause: 1, health: 100, energy: 100
INFO: 00_Intro.DXRando6: done randomizing INTRO using seed 0
INFO: 00_Intro.DXRFlags5: AnyEntry INTRO DeusEx.DXRFlags - version: v2.4.0.3, flagshash: 781491456, seed: 0, playthrough_id: -1427472606, maxrando: 0, autosave: 2, crowdcontrol: 0, loadout: 0, newgameplus_loops: 0, gamemode: 4, setseed: 1, difficulty: 1, minskill: 85, maxskill: 85, ammo: 100, multitools: 100, lockpicks: 100, biocells: 100
INFO: 00_Intro.DXRFlags5: speedlevel: 0, keys: 0, keys_containers: 0, doorspickable: 0, doorsdestructible: 0, deviceshackable: 0, passwordsrandomized: 0, medkits: 100, enemiesrandomized: 0, enemystats: 0, hiddenenemiesrandomized: 0, enemiesshuffled: 0, infodevices: 0, infodevices_containers: 0, dancingpercent: 0, doorsmode: 771
INFO: 00_Intro.DXRFlags5: enemyrespawn: 0, skills_disable_downgrades: 0, skills_reroll_missions: 0, skills_independent_levels: 0, startinglocations: 0, goals: 0, equipment: 0, medbots: -1, repairbots: -1, medbotuses: 10, repairbotuses: 10, medbotcooldowns: 0, repairbotcooldowns: 0, medbotamount: 0, repairbotamount: 0, turrets_move: 0
INFO: 00_Intro.DXRFlags5: turrets_add: 0, merchants: 0, banned_skills: 0, banned_skill_level: 0, enemies_nonhumans: 0, bot_weapons: 0, bot_stats: 0, swapitems: 0, swapcontainers: 0, augcans: 0, aug_value_rando: 0, skill_value_rando: 0, min_weapon_dmg: 100, max_weapon_dmg: 100, min_weapon_shottime: 100, max_weapon_shottime: 100
INFO: 00_Intro.DXRFlags5: AnyEntry INTRO prison_pocket: 0, bingo_win: 0, bingo_freespaces: 1, spoilers: 1, menus_pause: 1, health: 100, energy: 100
INFO: 00_Intro.DXRTelemetry5: health: 100, HealthLegLeft: 100, HealthLegRight: 100, HealthTorso: 100, HealthHead: 100, HealthArmLeft: 100, HealthArmRight: 100""")
		print(repr(d))
		self.assertEqual(d['firstword'], "PreFirstEntry")
		self.assertEqual(d['seed'], '0', 'got seed 0')
		self.assertEqual(d['playthrough_id'], '-1427472606', 'got playthrough_id')
		self.assertEqual(d['flagshash'], '781491456', 'got flagshash')
		self.assertEqual(d['map'], '00_Intro', 'got map')
		self.assertEqual(len(d.keys()), 86, 'found correct number of keys')

	def test_profanity(self):
		load_profanity_filter()
		self.not_censored('Pimp')
		self.not_censored('.71, 7.8')
		for i in range(1000):#range(100000):
			self.not_censored(i/10)
			self.not_censored(i/100)
			self.not_censored(i/1000)
	

	def not_censored(self, val):
		self.assertNotIn('*', profanity.censor(str(val)), str(val))

	def test_twitter(self):
		load_profanity_filter()
		msg = gen_event_msg({'type': 'DEATH', 'player': 'fuck', 'killer': 'thug', 'killerclass': 'thug', 'dmgtype': 'shot', 'location': '1.7456324, 2, 3.0,', 'map': 'fuck', 'mapname': 'fucking map', 'mission': 12}, {'seed': 123, 'flagshash': 456}, 'DeusEx', 'v1.5.0')
		info(msg)
		assert 'fuck' not in msg
		assert 'thug' in msg
		msg = gen_event_msg({'type': 'DEATH', 'victim': '# fuck @', 'killer': 'fucker', 'killerclass': 'fucker', 'dmgtype': 'fucked', 'location': '1.1, 2.34, 0.3,', 'map': 'fuck', 'mapname': 'fucking map', 'mission': 12}, {'seed': '123', 'flagshash': '456'}, 'Fake#Mod@', 'v1.5.0')
		info(msg)
		assert 'fuck' not in msg
		assert '@' not in msg
		assert '# ****' not in msg
		assert 'Fake#Mod@' not in msg
		assert 'FakeMod' not in msg

		msg = gen_event_msg({'type': 'BeatGame', 'PlayerName': '# fuck @', 'ending': '1', 'time': '123'}, {'seed': '123', 'flagshash': '456'}, 'Fake#Mod@', 'v1.5.0')
		info(msg)
		msg = gen_event_msg({'type': 'SavedPaul', 'PlayerName': '# fuck @', 'PaulHealth': '69'}, {'seed': '123', 'flagshash': '456'}, 'Fake#Mod@', 'v1.5.0')
		info(msg)
		self.assertEqual(censor_name('Thug'), 'Thug')
		self.assertEqual(censor_name('Hooker'), 'Hooker')
		self.assertEqual(censor_name('Bum'), 'Bum')
		self.assertEqual(censor_name('Terrorist'), 'Terrorist')
		self.assertEqual(censor_name('Junkie'), 'Junkie')
		self.assertEqual(censor_name('Smuggler'), 'Smuggler')
		self.assertEqual(censor_name('10 in'), '10 in')
		self.assertNotIn('igger', censor_name('Higger'))

	def test_version_strings(self):
		self.assertEqual( twitter_version_to_string('v1.9.1.10'), 'v1.9.1' )
		self.assertEqual( twitter_version_to_string('v1.9.1.10 Beta'), 'v1.9.1.10 Beta' )
		self.assertFalse( VersionStringIsStable('v2.3.0.1 Beta') )
		self.assertTrue( VersionStringIsStable('v2.3.0.2') )
	
	def test_update_notification(self):
		resp = update_notification("vanilla", "v2.0.0", {'map':'DX', 'firstword':'PreFirstEntry'})
		self.assertIn('notification', resp)
		resp = update_notification("vanilla", "v2.0.0", {'map':'01_NYC_UNATCOHQ', 'firstword':'PreFirstEntry'})
		self.assertNotIn('notification', resp)
		resp = update_notification("vanilla", "v2.0.0", {'map':'DX', 'firstword':'Whatever'})
		self.assertNotIn('notification', resp)
		resp = update_notification("vanilla", "v100.0.0", {'map':'DX', 'firstword':'PreFirstEntry'})
		self.assertNotIn('notification', resp)

	def test_bingo_board_generation(self):
		print('\n\ntesting bingo board\n')
		testStr = """{"type":"BeatGame","ending":"4","time":"54999","SaveCount":"256","deaths":"9","maxrando":"0","PlayerName":"Asstro","map":"06_HONGKONG_WANCHAI_CANAL","mapname":"Hong Kong - Waterways","mission":"6","TrueNorth":"0","PlayerIsFemale":"True","GameMode":"Normal Randomizer","newgameplus_loops":"0","loadout":"All Items Allowed","NumberOfBingos":"1","bingo-0-0":{"event":"M06BoughtVersaLife","desc":"Get maps of the VersaLife building","progress":1,"max":1},"bingo-0-1":{"event":"CamilleConvosDone","desc":"Get info from Camille","progress":0,"max":1},"bingo-0-2":{"event":"TiffanySavage_Dead","desc":"Kill Tiffany Savage","progress":0,"max":1},"bingo-0-3":{"event":"BathroomBarks_Played","desc":"Embarass UNATCO","progress":1,"max":1},"bingo-0-4":{"event":"PaulDenton_Dead","desc":"Let Paul die","progress":1,"max":1},"bingo-1-0":{"event":"M08WarnedSmuggler","desc":"Warn Smuggler","progress":0,"max":1},"bingo-1-1":{"event":"TerroristCommander_Dead","desc":"Kill the Terrorist Commander","progress":1,"max":1},"bingo-1-2":{"event":"MeetAI4_Played","desc":"Talk to Morpheus","progress":0,"max":1},"bingo-1-3":{"event":"JoshFed","desc":"Give Josh some food","progress":0,"max":1},"bingo-1-4":{"event":"support1","desc":"Blow up a gas station","progress":0,"max":1},"bingo-2-0":{"event":"Terrorist_ClassUnconscious","desc":"Knock out 15 NSF Terrorists","progress":18,"max":15},"bingo-2-1":{"event":"M07ChenSecondGive_Played","desc":"Party with the Triads","progress":0,"max":1},"bingo-2-2":{"event":"Free Space","desc":"Free Space","progress":1,"max":1},"bingo-2-3":{"event":"StantonAmbushDefeated","desc":"Defend Dowd from the ambush","progress":0,"max":1},"bingo-2-4":{"event":"M02BillyDone","desc":"Give Billy some food","progress":0,"max":1},"bingo-3-0":{"event":"FoundScientistBody","desc":"Search the canal","progress":0,"max":1},"bingo-3-1":{"event":"VandenbergToilet","desc":"Use the only toilet in Vandenberg","progress":0,"max":1},"bingo-3-2":{"event":"JocksToilet","desc":"Use Jock's toilet","progress":0,"max":1},"bingo-3-3":{"event":"LeoToTheBar","desc":"Bring the terrorist commander to the bar","progress":3,"max":1},"bingo-3-4":{"event":"SubwayHostagesSaved","desc":"Save both hostages in the subway","progress":0,"max":1},"bingo-4-0":{"event":"FlushToilet","desc":"Use 30 toilets","progress":38,"max":30},"bingo-4-1":{"event":"SpiderBot_ClassDead","desc":"Destroy 15 Spider Bots","progress":1,"max":15},"bingo-4-2":{"event":"ManWhoWasThursday","desc":"Read 4 parts of The Man Who Was Thursday","progress":1,"max":4},"bingo-4-3":{"event":"BoatEngineRoom","desc":"Access the engine room on the boat in the Hong Kong canals","progress":0,"max":1},"bingo-4-4":{"event":"NiceTerrorist_Dead","desc":"Ignore Paul in the 747 Hangar","progress":1,"max":1}}"""
		d = json.loads(testStr)
		board = generateBingoBoardAttachment(d,False)
		assert board != None

	def test_aug_screen_generation(self):
		print('\n\ntesting aug screen\n')
		testStr = """{"type": "BeatGame", "ending": "2", "time": "206851", "SaveCount": "800", "deaths": "0", "maxrando": "0", "PlayerName": "Asstro", "map": "ENDGAME2", "mapname": "", "mission": "99", "TrueNorth": "0", "PlayerIsFemale": "False", "GameMode": "Normal Randomizer", "newgameplus_loops": "0", "loadout": "All Items Allowed", "NumberOfBingos": "12", "bingo-0-0": {"event": "paris_hostage_Dead", "desc": "Kill both the hostages in the catacombs", "progress": 2, "max": 2}, "bingo-0-1": {"event": "ClubEntryPaid", "desc": "Help Mercedes and Tessa", "progress": 1, "max": 1}, "bingo-0-2": {"event": "M10EnteredBakery", "desc": "Enter the bakery", "progress": 1, "max": 1}, "bingo-0-3": {"event": "TobyAtanwe_Dead", "desc": "Kill Toby Atanwe", "progress": 1, "max": 1}, "bingo-0-4": {"event": "TerroristCommander_Dead", "desc": "Kill the Terrorist Commander", "progress": 1, "max": 1}, "bingo-1-0": {"event": "Gray_ClassDead", "desc": "Kill 5 Grays", "progress": 10, "max": 5}, "bingo-1-1": {"event": "ActivateVandenbergBots", "desc": "Activate both of the bots at Vandenberg", "progress": 2, "max": 2}, "bingo-1-2": {"event": "KnowsAnnasKillphrase", "desc": "Learn both parts of Anna's Killphrase", "progress": 2, "max": 2}, "bingo-1-3": {"event": "MolePeopleSlaughtered", "desc": "Slaughter the Mole People", "progress": 1, "max": 1}, "bingo-1-4": {"event": "MoonBaseNews", "desc": "Read news about the Lunar Mining Complex", "progress": 3, "max": 1}, "bingo-2-0": {"event": "JocksToilet", "desc": "Use Jock's toilet", "progress": 1, "max": 1}, "bingo-2-1": {"event": "M02BillyDone", "desc": "Give Billy some food", "progress": 1, "max": 1}, "bingo-2-2": {"event": "Free Space", "desc": "Free Space", "progress": 1, "max": 1}, "bingo-2-3": {"event": "MJ12Commando_ClassDead", "desc": "Kill 10 MJ12 Commandos", "progress": 33, "max": 10}, "bingo-2-4": {"event": "lemerchant_Dead", "desc": "Kill Le Merchant", "progress": 1, "max": 1}, "bingo-3-0": {"event": "JoeGreene_Dead", "desc": "Kill Joe Greene", "progress": 1, "max": 1}, "bingo-3-1": {"event": "MilitaryBot_ClassDead", "desc": "Destroy 5 Military Bots", "progress": 5, "max": 5}, "bingo-3-2": {"event": "SpinShipsWheel", "desc": "Spin 3 ships wheels", "progress": 4, "max": 3}, "bingo-3-3": {"event": "AnnaNavarre_Dead", "desc": "Kill Anna Navarre", "progress": 1, "max": 1}, "bingo-3-4": {"event": "BoatEngineRoom", "desc": "Access the engine room on the boat in the Hong Kong canals", "progress": 1, "max": 1}, "bingo-4-0": {"event": "HumanStompDeath", "desc": "Stomp 3 humans to death", "progress": 4, "max": 3}, "bingo-4-1": {"event": "ManWhoWasThursday", "desc": "Read 4 parts of The Man Who Was Thursday", "progress": 6, "max": 4}, "bingo-4-2": {"event": "HotelHostagesSaved", "desc": "Save all hostages in the hotel", "progress": 1, "max": 1}, "bingo-4-3": {"event": "Chad_Dead", "desc": "Kill Chad", "progress": 1, "max": 1}, "bingo-4-4": {"event": "TongsHotTub", "desc": "Take a dip in Tracer Tong's hot tub", "progress": 1, "max": 1}, "Aug-7": {"name": "AugUnknown", "level": 3}, "Aug-3": {"name": "AugCloak", "level": 3}, "Aug-4": {"name": "AugRadarTrans", "level": 3}, "Aug-9": {"name": "AugShield", "level": 3}, "Aug-10": {"name": "AugHealing", "level": 3}, "Aug-13": {"name": "AugIFF", "level": 0}, "Aug-12": {"name": "AugLight", "level": 0}, "Aug-6": {"name": "AugMuscle", "level": 3}, "Aug-8": {"name": "AugVision", "level": 3}, "Aug-5": {"name": "AugDrone", "level": 3}, "Aug-14": {"name": "AugDatalink", "level": 0}, "Aug-11": {"name": "AugHeartLung", "level": 0}}"""
		d = json.loads(testStr)
		augDrawer = AugScreenDrawer(d, isFemale=d["PlayerIsFemale"])
		augScreen = augDrawer.getImageInMemory()
		assert augScreen != None

		augDrawer = AugScreenDrawer(d, isFemale="True")
		augScreen = augDrawer.getImageInMemory()
		assert augScreen != None

	def test_maggie_bday(self):
		testStr = '{"type":"Flag","flag":"06_Datacube05","immediate":"False","location":"-731.622498,-1130.981323,73.800011","extra":" June 18 ","PlayerName":"Die4Ever","map":"06_HONGKONG_WANCHAI_STREET","mapname":"Hong Kong - Tonnochi Road","mission":"6","TrueNorth":"0","PlayerIsFemale":"False","GameMode":"Normal Randomizer","newgameplus_loops":"0","loadout":"All Items Allowed"}'
		d = json.loads(testStr)
		d2 = {'seed': '123', 'flagshash': '456'}
		HKtimezone = datetime.timezone(datetime.timedelta(hours=8))
		currentDate = datetime.datetime.now(tz=HKtimezone).date()

		d['extra'] = currentDate.strftime('%B %d')
		msg = gen_event_msg(d, d2, 'vanilla', 'v2.1.0.1 Beta')
		self.assertIn('Happy birthday', msg)

		day = (currentDate.day+2)%27 + 1 # make sure it isn't 0
		date = currentDate.replace(day=day)# a different day that isn't today
		d['extra'] = date.strftime('%B %d')
		msg = gen_event_msg(d, d2, 'vanilla', 'v2.1.0.1 Beta')
		self.assertNotIn('Happy birthday', msg)

		date = currentDate.replace(month=(currentDate.month+1)%12)# a different month that isn't the current month, but same day
		d['extra'] = date.strftime('%B %d')
		msg = gen_event_msg(d, d2, 'vanilla', 'v2.1.0.1 Beta')
		self.assertNotIn('Happy birthday', msg)

		d = {'PlayerName': 'Die4Ever', 'flag': '06_Datacube05', 'extra': 'July 18'}
		r = FlagEventMsg(d, 'RevRandomizer')
		self.assertIn('Hello Maggie', r)

		d = {'PlayerName': 'Die4Ever', 'flag': '06_Datacube05', 'extra': 'July 18th'}
		r = FlagEventMsg(d, 'RevRandomizer')
		self.assertIn('Hello Maggie', r)
	
	def test_leaderboard(self):
		print('\n\ntest_leaderboard')
		cursor = [
			dict(name='Die4Ever', playthrough_id=1, score=9002, totaltime=1000, seed=123, flagshash=123, setseed=1),
			dict(name='Die4Ever', playthrough_id=123, score=9000, totaltime=1000, seed=123, flagshash=123, setseed=1),
		]
		for i in range(100):
			d = dict(name='Die4Ever', playthrough_id=456, score=8999, totaltime=1000, seed=123, flagshash=123, setseed=1)
			d['playthrough_id'] += i
			d['score'] -= i
			if d['playthrough_id'] == 500:
				theone = d
			cursor.append(d)
		event = dict(PlayerName='Die4Ever')
		playthrough_id = theone['playthrough_id']
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Die4Ever', playthrough_id, 2, num_runs=3)
		self.assertEqual(leaderboard[0][6], 1, 'First place')
		self.assertGreater(leaderboard[0][1], theone['score'], 'First place score greater than mine')

		self.assertEqual(leaderboard[1][6], '--', 'the run we just did placement')
		self.assertEqual(leaderboard[1][7], ToHex(playthrough_id), 'the run we just did placethrough id')
		self.assertEqual(leaderboard[1][1], theone['score'], 'the run we just did score')

		self.assertEqual(leaderboard[2][6], '--', 'Hidden run, the one we just beat placement')
		self.assertLess(leaderboard[2][1], theone['score'], 'the one we just beat score')

		i=0
		for d in cursor:
			d['name'] = 'test'+str(i)
			i+=1
		theone['name'] = 'Die4Ever'

		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Die4Ever', playthrough_id, 47)
		self.assertEqual(leaderboard[0][6], 1, 'First place')
		self.assertEqual(leaderboard[12][7], ToHex(playthrough_id), 'the run we just did placethrough id')
		self.assertNotEqual(leaderboard[14][6], 15, 'last entry not 15th place')

		cursor = []
		for i in range(100):
			d = dict(name='Die4Ever', playthrough_id=456, score=8999, totaltime=1000, seed=123, flagshash=123, setseed=1)
			d['name'] = 'Die4Ever' + str(i%4)
			d['playthrough_id'] = i
			d['score'] = i
			cursor.append(d)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Die4Ever2', 42, 5, num_runs=6)

		print('\nreal db data')
		runs_dbdata = [
			["Serious Jesus 2", 118546, -23381102],
			["Jehuty 19 Max Rando", 111862, 1925599382],
			["Jehuty 12 ProdPlus", 111158, 1964890607],
			["Jehuty 15 Autosave", 110078, 685496802],
			["Jesus 12 June", 108824, -901629229],
			["Jehuty 10", 108666, 1653135951],
			["Jesus 28 May", 108552, 1430094222],
			["Jesus Down with the sickness", 108223, 599663118],
			["Jehuty 16 Full Bingo", 108171, 1887935333],
			["Jehuty 25", 105621, 2098955228],
			["Jehuty 27", 104208, 1258875203],
			["htaportsAehT", 97926, -726513848],
			["Jesus Birthday woot", 96612, 1228225928],
			["Jesus 13 april 2023", 94619, 1533056676],
			["Jesus 13 april 2023", 94541, 1533056676],
			["Jesus Crowd Control Sim 19 4 23", 94454, 948679561],
			["Jesus 13 april 2023", 93438, 1533056676],
			["Jesus Third Person", 90519, 362786397],
			["Jesus Serious Sam respawn", 90444, 1541094718],
			["Ramisme", 86145, 1454581816],
			["jesus 5000 enemies", 82397, 743054318],
			["Jehuty 27", 81316, 1977075558],
			["TheAstropath", 80562, 1315902344],
			["Jehuty 24", 79908, 1925488339],
			["Extreme Jezuz", 79568, 1602688617],
			["Die4Ever", 78758, 1157006666],
			["Ramisme", 73498, 1417294301],
			["TheAstropath iMac", 73422, 1386568112],
			["TheAstropath", 68699, 1305193558],
			["TheAstropath Bogus", 66008, -917692161],
			["TheAstropath Bogus", 65887, 1510924585],
			["Die4Ever", 64862, 1656622478],
			["Die4Ever", 64225, 1656622478],
			["Die4Ever", 63481, 1656622478],
			["Jehuty 18 Prod Pure", 63284, 333508554],
			["Jehuty 23 Gutsman", 61406, 1372459519],
			["Jehuty 17 Heavy and Explosives", 60920, 665704856],
			["Jehuty 22 EntRando", 60513, 754226256],
			["TheAstropath ogniB", 60508, -1904543835],
			["TheAstropath", 58872, 1517837098],
			["TheAstropath", 58802, 1517837098],
			["TheAstropath Bogus", 55637, 242814721],
			["Jehuty 21 Suitmode", 55301, 793633467],
			["Jehuty 21 Suitmode", 55166, 793633467],
			["Jehuty 21 Suitmode", 55089, 793633467],
			["TheAstropath", 53094, 148060962],
			["TheAstropath ogniB", 48998, -1904543835],
			["TheAstropath ogniB", 48873, -1904543835],
			["Jehuty 27", 48822, 13713069],
			["TheAstropath ogniB", 48270, -1480940464],
			["TheAstropath Boing", 46433, -1722030244],
			["TheAstropath Bingo", 42008, 858923826],
			["Jesus Birthday Bingo", 40921, 379215440],
			["Jehuty 20 Mini Infamy", 38821, 409161902],
			["TheAstropath Bingo", 37094, 1080634536],
			["TheAstropath WaltonWare", 31828, -2054749866],
			["Jehuty 12 ProdPlus", 22729, 466213372],
			["Heinki", 17777, 877647836],
			["Heinki", 17081, 318850018],
			["Bingothon", 16787, -1801708934],
			["Jehuty 11 Respawn", 16180, 1553672512],
		]
		cursor = []
		for i in runs_dbdata:
			d = dict(name=i[0], playthrough_id=i[2], score=i[1], totaltime=1000, seed=123, flagshash=123, setseed=1)
			cursor.append(d)

		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Serious Jesus 2', -23381102, 1)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Jehuty 19 Max Rando', 1925599382, 2)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Ramisme', 1454581816, 18)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Ramisme', 1417294301, 24)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Die4Ever', 1656622478, 26)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'Die4Ever', 1656622478, 26, num_runs=42, max_len=None)
		(leaderboard, PBEntry, PlaythroughEntry) = self.check_run(cursor, 'TheAstropath ogniB', -1904543835, 30)

		with open('leaderboardtest.json') as f:
			cursor = json.load(f)
		leaderboard = GroupLeaderboard(cursor, {'PlayerName':'JC Denton'}, -51934675, 15)
		self.assertEqual(len(leaderboard), 15, '15 runs displayed for anon')
		#for i in range(15):
		#	self.assertEqual(leaderboard[i][6], i+1, 'anon leaderboard #' + str(i+1))
		print('\n')


	def check_run(self, cursor, PlayerName, playthrough_id, placement, num_runs=15, max_len=15):
		print('testing', '#'+str(placement), PlayerName, playthrough_id)
		event = dict(PlayerName=PlayerName)
		leaderboard = GroupLeaderboard(cursor, event, playthrough_id, max_len)
		print(repr(leaderboard))
		self.assertEqual(len(leaderboard), num_runs, str(num_runs) + ' runs displayed for '+PlayerName)
		(PBEntry, PlaythroughEntry) = self.find_entries(leaderboard, PlayerName, playthrough_id)
		self.assertEqual( _GetLeaderboardPlacement(leaderboard, playthrough_id), placement, PlayerName + ' _GetLeaderboardPlacement ' + str(placement))
		return (leaderboard, PBEntry, PlaythroughEntry)
	

	def find_entries(self, leaderboard:list, name:str, playthrough:int):
		PBEntry = None
		PlaythroughEntry = None
		for i in leaderboard:
			if i[0] == name and i[6] != '--' and PBEntry is None:
				PBEntry = i
			if i[7] == ToHex(playthrough):
				PlaythroughEntry = i
		print('find_entries', name, playthrough, PBEntry, PlaythroughEntry)
		self.assertTrue(PBEntry, 'found PB for '+name)
		self.assertTrue(PlaythroughEntry, 'found playthrough for '+name)
		return (PBEntry, PlaythroughEntry)

@typechecked
class MockFailCursor:
	def execute(self, q):
		raise Exception("MockFailCursor: "+q)

@typechecked
def run_tests():
	#increase_loglevel(DebugLevels.DEBUG)
	info("running tests...")

	info(repr(update_notification("vanilla", "v1.3.0", {'map':'DX'})))

	# ensure proper error handling
	results = try_exec(MockFailCursor(), "expected failure")
	for t in (results):
		err("we shouldn't hit this")

	d = parse_query_string("version=v1.2.3 Alpha&mod=DeusEx&another=param")
	assert d['version'] == "v1.2.3 Alpha"
	assert d['mod'] == "DeusEx"
	assert d['another'] == "param"

	assert VersionStringToInt(d['version']) == VersionToInt(1, 2, 3, 0)
	assert VersionStringToInt("v1.3.1") == VersionToInt(1, 3, 1, 0)
	assert VersionStringToInt("v1.7.2.5") == VersionToInt(1, 7, 2, 5)
	assert VersionStringToInt("v1.7.3.5 Alpha") == VersionToInt(1, 7, 3, 5)

	info(unrealscript_sanitize("this is a test, Die4Ever; ok: another test {      } \\  bye "))

	# for k in ['name', 'killer', 'damagetype', 'age', 'x', 'y', 'z', 'killerclass']:
	d = [1, 'Die4Ever', '', '', 3600, 0, 0, 0, 'killerclass']
	d2 = d.copy()
	d2[1] = 'TheAstropath'
	d3 = d.copy()
	d3[4] = '3000'
	d3[5] = '10'
	d4 = d.copy()
	d4[5] = 16*150 # 150 feet
	d5 = d.copy()
	d5[1] = 'FUCK'
	deaths = filter_deaths({'a':d, 'b':d2, 'c':d3, 'd':d.copy(), 'e':d4, 'f':d.copy(), 'g':d3.copy(), 'h':d.copy(), 'i':d5})
	info("filter_deaths down to "+repr(deaths))
	assert len(deaths) == 7
	assert 'FUCK' not in json.dumps(deaths)

	info(repr(get_events('EVENT: {"location":"12.3, 4.56, 7.89"}')))
	
	info("path: "+os.path.dirname(os.path.realpath(__file__)))
	info("cwd: "+os.getcwd())
	info("logdir: "+logdir)
	info("db config: " + repr(get_config()))
	#write_db("0", "test")
	unittest.main(verbosity=9, warnings="error", failfast=True)


if __name__ == '__main__':
	run_tests()

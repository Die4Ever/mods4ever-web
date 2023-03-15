import autoinstaller
from typeguard import typechecked, install_import_hook
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

	def test_profanity_numbers(self):
		load_profanity_filter()
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
		augDrawer = AugScreenDrawer(d,"AugDrawImages/",d["PlayerIsFemale"])
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

		date = currentDate.replace(day=currentDate.day+3)
		d['extra'] = date.strftime('%B %d')
		msg = gen_event_msg(d, d2, 'vanilla', 'v2.1.0.1 Beta')
		self.assertNotIn('Happy birthday', msg)

		date = currentDate.replace(month=(currentDate.month+1)%12)
		d['extra'] = date.strftime('%B %d')
		msg = gen_event_msg(d, d2, 'vanilla', 'v2.1.0.1 Beta')
		self.assertNotIn('Happy birthday', msg)


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
	unittest.main(verbosity=9, warnings="error")


if __name__ == '__main__':
	run_tests()

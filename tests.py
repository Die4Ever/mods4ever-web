from dxlog.base import *
from dxlog.db import *
from dxlog.parsing import *
from dxlog.twitter import *
from dxlog.request import *
from better_profanity import profanity
import unittest

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


class MockFailCursor:
	def execute(self, q):
		raise Exception("MockFailCursor: "+q)

def run_tests():
	#increase_loglevel(DebugLevels.DEBUG)
	info("running tests...")

	info(repr(update_notification("vanilla", "v1.3.0")))

	# ensure proper error handling
	results = try_exec(MockFailCursor(), "expected failure")
	for t in (results):
		err("we shouldn't hit this")
	
	for d in get_deaths("\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed by SecurityBot3 UJ-31 with shot damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: Die4Ever was killed in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed with shot damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale2: JC Denton was killed with  damage in 01_NYC_UNATCOISLAND (-502.167694,40.753559,-119.199997)"):
		info(repr(d))

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
	d = [1, 'Die4Ever', '', '', 3600, 0, 0, 0]
	d2 = d.copy()
	d2[1] = 'TheAstropath'
	d3 = d.copy()
	d3[4] = '3000'
	d3[5] = '10'
	d4 = d.copy()
	d4[5] = 16*150 # 150 feet
	deaths = filter_deaths({'a':d, 'b':d2, 'c':d3, 'd':d.copy(), 'e':d4, 'f':d.copy(), 'g':d3.copy(), 'h':d.copy()})
	info("filter_deaths down to "+repr(deaths))
	assert len(deaths) == 6

	info(repr(get_events('EVENT: {"location":"12.3, 4.56, 7.89"}')))
	
	info("path: "+os.path.dirname(os.path.realpath(__file__)))
	info("cwd: "+os.getcwd())
	info("logdir: "+logdir)
	info("db config: " + repr(get_config()))
	#write_db("0", "test")
	unittest.main(verbosity=9, warnings="error")


if __name__ == '__main__':
	run_tests()

from dxlog.base import *
from dxlog.db import *
from dxlog.parsing import *
from dxlog.twitter import *
from dxlog.request import *
import unittest

class TestLog(unittest.TestCase):
	def test_parse_content(self):
		d = parse_content("DX.DXRando0: RandoEnter() firstTime: True, IsTravel: False, seed: 601088 DX\nINFO: DX.DXRando0: randomizing DX using seed 601088\nINFO: DX.DXRFlags0: PreFirstEntry DX DeusEx.DXRFlags - v1.7.3.5 Beta, seed: 601088, flagshash: 90622488, playthrough_id: 1686707255, flagsversion: 1070305, gamemode: 0, difficulty: 1.000000, loadout: 0, brightness: 15, newgameplus_loops: 0, autosave: 2, crowdcontrol: 0, codes_mode: 2\nDEATH: 01_NYC_UNATCOIsland.JCDentonMale8: JC Denton was killed by JCDentonMale JC Denton with exploded damage in 01_NYC_UNATCOISLAND (748.419373,-433.573730,-123.300003)\nINFO: 01_NYC_UNATCOIsland.JCDentonMale8: Speed Enhancement deactivated")
		print(d['firstword'])
		self.assertEqual(d['firstword'], "PreFirstEntry")

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

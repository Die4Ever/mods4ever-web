from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v3.4.0.8"
	parts = SplitVersionString(latest_version)
	if parts[2] != '0':
		short_version = 'v' + parts[0] + '.' + parts[1] + '.' + parts[2]# not part 3 (build number)
	else:
		short_version = 'v' + parts[0] + '.' + parts[1]
	notification = 'Please download update!'
	desc = 'New ' + short_version + '!'
	detail = ""

	dates = []
	headers = []
	msgs = []

	dates.append('2025-03-19')
	headers.append("v3.4 We Welcome All")
	msgs.append(
"""Normal Randomizer game mode has been renamed to Full Randomizer, and the new Normal Randomizer mode is the new default
Zero Rando now disables many more balance changes, making it a great way to play Deus Ex for the first time
Multiple, rotating quicksave slots
Slowed down WaltonWare difficulty increases
New menu to change current game settings
New loadouts and improvements to old ones
Tweaks to The Merchant items and pricing, now selling more relevant items with more appropriate prices
And more! Download from Mods4Ever.com or read the full patch notes on Github.""")

	dates.append('2025-01-06')
	headers.append("v3.3.1 Bug Fixes")
	msgs.append(
"""You must now pet Starr instead of simply visiting her for bingo
Fixed bug where game would end if you completed a bingo line without a Bingo Win setting configured
Deus Ex: Revision support improved more (may have some oddities with old saves until reaching a new map)
And more! Download from Mods4Ever.com or read the full patch notes on Github.""")

	dates.append('2024-12-11')
	headers.append("v3.3 Mr. Page's Mean Bingo Machine")
	msgs.append(
"""Mr. Page's Mean Bingo Machine: A new mode where you play through the whole game, but must complete a set number of bingo lines before being allowed to progress to the next mission. Once you get to the next mission, you are given a new bingo board!
One Item Mode: Our new dumbest game mode! All items in a map will be replaced with a single type of item (eg. all flares, all biocells, or all beers)
Augs can now receive randomized slots (so speed can be an eye aug) (look in the Advanced New Game menu)
Deus Ex: Revision support is massively improved as a whole
And more! Download from Mods4Ever.com or read the full patch notes on Github.""")

	dates.append('2024-10-29')
	headers.append("v3.2.4 Halloween Bug Fixes")
	msgs.append(
"""Fixed Mr. H from counting in the M04 raid enemy counter
Fixed zombie Howards preventing Silo from completing
Some fixes for endgame cutscenes and NG+
And more! Download from Mods4Ever.com or read the full patch notes on Github.
We've seen some confusion with Limited Fixed Saves. When you have a Memory Containment Unit in your inventory (or 2 for the new Extreme version) you only need to have the box highlight on the computer and then you can use the normal Save Game menu or Quicksave button. The only freebie autosave you get is at the very start of the game. Make sure to save before going to Battery Park! Sometimes you might want to backtrack to save. Remember that if you die not all is lost, because you now have a better plan!""")

	dates.append('2024-10-24')
	headers.append("v3.2.3 It Takes Two")
	msgs.append(
"""Extreme Limited Fixed Saves mode, uses 2 Memory Containment Units per save instead of 1. Must also be near a computer like in the other Fixed Saves modes. Pairs well with Halloween Mode for a new challenge!
Reduced Mr. H's health. You still can't kill him, but if you deal enough damage to him then he will run away.
New home for the DXRando Activity bot https://mastodon.social/@DXRandoActivity
And more! Download from Mods4Ever.com or read the full patch notes on Github.
We've seen some confusion with Limited Fixed Saves. When you have a Memory Containment Unit in your inventory (or 2 for the new Extreme version) you only need to have the box highlight on the computer and then you can use the normal Save Game menu or Quicksave button. The only freebie autosave you get is at the very start of the game. Make sure to save before going to Battery Park! Sometimes you might want to backtrack to save. Remember that if you die not all is lost, because you now have a better plan!""")
	
	url = "https://mods4ever.com"
	visit = "Would you like to visit "+url+" now?"

	assert len(desc) < 35
	assert len(detail) < 35
	assert len(headers) == 5
	assert len(dates) == len(headers)
	assert len(msgs) == len(headers)
	assert short_version in headers[0]
	assert short_version in desc

	latest_version_int = VersionStringToInt(latest_version)
	assert latest_version_int > 0

	for header in headers:
		assert len(header) < 200
	
	if data.get('map', '').upper() not in ('DX', 'DXONLY'):
		return response
	if data.get('firstword') != 'PreFirstEntry':
		return response
	
	if VersionStringToInt(version) < latest_version_int:
		response['notification'] = notification
		response['message'] = desc
		response['message'] += "|n" + detail
		response['message'] += "|n" + visit
	
	for i in range(len(headers)):
		response['newsdate' + str(i)] = dates[i]
		response['newsheader' + str(i)] = headers[i]
		msg = msgs[i].replace('\n', '|n|n')# double space, makes word wrapping look better
		response['newsmsg' + str(i)] = msg
	response['url'] = url
	return response


def generate_response(mod, version, response):
	if VersionStringToInt(version) >= VersionToInt(1, 7, 3, 3):
		return json.dumps(response)
	else:
		ret = ''
		ret += response['status'] + "\n"
		if 'notification' in response:
			ret += "notification: " + response['notification']
			ret += "\n" + response['message'] + "\n"
		return ret

def print_response(mod, version, response):
	print(generate_response(mod, version, response))


def get_request():
	s_content_length = os.environ.get('CONTENT_LENGTH')
	if s_content_length is None:
		s_content_length = "0"
	else:
		s_content_length = str(s_content_length)

	content_length = int(s_content_length)
	content:str = ""
	data:bytes = b''

	try:
		#while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
		if content_length > 0:
			data:bytes = sys.stdin.buffer.read()
			content = read_binary_content(data)
			content = content.replace('\x00','').replace('\r','')
	except Exception as e:
		logex(e)
	
	ip = os.environ.get('REMOTE_ADDR')
	qps = query_params()
	return content, content_length, ip, qps


def parse_query_string(q):
	d = {}
	for m in re.finditer(r'(([^=]+)=([^\&]+)&?)', q):
		d[m.group(2)] = m.group(3).replace("%20", " ")
	return d

def query_params():
	if os.environ.get('QUERY_STRING'):
		return parse_query_string(os.environ.get('QUERY_STRING'))
	return {}

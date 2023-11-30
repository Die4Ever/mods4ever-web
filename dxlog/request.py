from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v2.5.5.6"
	parts = SplitVersionString(latest_version)
	if parts[2] != '0':
		short_version = 'v' + parts[0] + '.' + parts[1] + '.' + parts[2]# not part 3 (build number)
	else:
		short_version = 'v' + parts[0] + '.' + parts[1]
	notification = 'New ' + short_version + '!'
	desc = "Please update!"
	detail = ""

	dates = []
	headers = []
	msgs = []

	dates.append('2023-11-30')
	headers.append("v2.5.5 new WaltonWare Entrance Rando mode and more!")
	msgs.append(
"""WaltonWare Entrance Rando mode is a combination of the 2 game modes for extra craziness!
Sub base Jock immediately available in WaltonWare
Kills and knockouts of characters are now distinguished (so knocking someone out won't count as a kill for bingo)
Installer now has an option to apply fixes to vanilla as well, sort of like a "Zero Changes" mode as an alternative to "Zero Rando" mode for the purists.
Added option to make flickering and strobing lights more chill (epilepsy-safe mode)
Ninja JC mode now allows mini-crossbow and knife, this provides more variety without dominating the ninja playstyle
Weapon mods can now be automatically applied to the weapon in your hand
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2023-10-12')
	headers.append("v2.5.4 WaltonWare improvements and bug fixes!")
	msgs.append(
"""Lots more WaltonWare and bingo improvements
Now at 310 bingo goals!
Gave Hela a guaranteed Sewer key and randomized her location within the MJ12 bunker in the catacombs
Many improvements to datacube and nanokey location rules
Tweaked demolition skill balance and buffed attached grenades
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2023-09-14')
	headers.append("v2.5.3 Various improvements and fixes!")
	msgs.append(
"""Lots more WaltonWare and bingo improvements
Now over 250 bingo goals!
Speedrun mode now has an in-game timer and splits viewer
More installer improvements
Fixed bug with nanokey/datacube placements for mirrored maps
Improved autosave again
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2023-08-31')
	headers.append("v2.5.2 Various improvements and fixes!")
	msgs.append(
"""Lots of WaltonWare and bingo improvements
Improved autosave
New Game+ fixes
Randomizer weapon mods types
Shield aug guys now take 10% damage from main resistances rather than none
Revision goals randomization
Bug fixes for Revision Randomizer
Bug fixes for HX Randomizer co-op
Reduced visor chances for enemies
Vision Enhancement augmentation can now see items through walls at level 1 instead of needing level 2.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2023-07-28')
	headers.append("v2.5.1 Augmented Enemies, WaltonWare mode, and more!")
	msgs.append(
"""Augmented Enemies for an increased challenge!
WaltonWare mode: a game mode focused on quickly doing bingos and New Game+
We're also now over 200 bingo events!
New Speedrun mode: speedrun with fewer resets while still being able to enjoy higher difficulties.
Crowd Control online and simulated together for the average streamer that doesn't have many viewers
Fixes to various mirrored maps, so make sure to tell the installer to download the new mirrored maps!
Autofill passwords even in Zero Rando mode, great for Steam Deck players!
We now prevent using lockpicks/multitools on doors/keypads you have the key/code for, great for people who don't read!
New website Mods4Ever.com
And more! Read the full patch notes on Github""")

	url = "https://github.com/Die4Ever/deus-ex-randomizer/releases/latest"
	visit = "Would you like to visit "+url+" now?"

	assert len(desc) < 35
	assert len(detail) < 35
	assert len(headers) <= 5
	assert len(dates) == len(headers)
	assert len(msgs) == len(headers)
	assert short_version in headers[0]
	assert short_version in notification
	for header in headers:
		assert len(header) < 200
	
	if data.get('map', '').upper() not in ('DX', 'DXONLY'):
		return response
	if data.get('firstword') != 'PreFirstEntry':
		return response
	
	if VersionStringToInt(version) < VersionStringToInt(latest_version):
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

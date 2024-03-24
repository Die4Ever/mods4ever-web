from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v2.6.1.1"
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

	dates.append('2024-03-23')
	headers.append("v2.6.1 IMPORTANT HOTFIX!")
	msgs.append(
"""Fixed issue with the door to the Silo Launch Control Computer door getting stuck.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2024-03-21')
	headers.append("v2.6 Augs overhaul, more randomized goal locations, and much more!")
	msgs.append(
"""New option for automatic augmentations, so you don't have to micromanage your F-keys so hard.
More goals with randomized locations such as the transmitter computer in NSF HQ, Jock and the raid spawn points in Return to NYC, and the Launch Control Computer in Vandenberg Silo.
Reduced in-fighting issues.
Saving during infolinks!
Fixed enemies running out of ammo early.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2024-02-07')
	headers.append("v2.5.6 AugBots and more!")
	msgs.append(
"""New AugBot, similar to a MedBot but it cannot heal, only install augmentations.
New bingo goals and many bingo fixes.
Laser mod now turns on automatically when you equip the weapon (optional in the Rando settings menu)
Some maps now have goals rando notes (look in your Images tab), just click the Goal Locations or Goal Spoilers button.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

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

	url = "https://github.com/Die4Ever/deus-ex-randomizer/releases/latest"
	visit = "Would you like to visit "+url+" now?"

	assert len(desc) < 35
	assert len(detail) < 35
	assert len(headers) == 5
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

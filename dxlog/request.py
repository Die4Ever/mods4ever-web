from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v3.0.0.6"
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

	dates.append('2024-06-13')
	headers.append("v3.0 You Can Pet the Dog!")
	msgs.append(
"""You can now pet the dog! And other animals too. With bingo goals.
Loot Refusal options for looting carcasses.
Reworked Synthetic Heart and Spy Drone augmentations
Turn off any glow on datacubes once you've read them, which helps finding datacubes that are close together.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")
	
	dates.append('2024-05-20')
	headers.append("v2.7.2 The Silo's Secret Slide!")
	msgs.append(
"""Fixed M12 vandenberg command, vanilla Jock and Tong location had Tong inside the helicopter which was a softlock
Added datacube to the Lucky Money with the password to the security computer, for opening the freezer door
M02 battery park replaced vents start with shanty town
Moved Silo Machine Shop Computer location from on the desk to on the wall
Fixed weapon's ammo amount when dropped or taken away (M05 grenades)
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2024-05-03')
	headers.append("v2.7.1 Barrels O'Fun!")
	msgs.append(
"""Simplified barrels to combine multiple variants that did the same thing. Also added optional new textures to make it even clearer (look in the Rando menu).
More goal locations mutual exclusions, to reduce the difference between best seed and worst seed for each mission.
Nerfed automatic power recirculator slightly.
Gas colliding with enemies is now more consistent.
Weapons that fall out of enemy hands due to damage now have ammo.
You now start with 6575 skill points, and Zero Rando defaults to Trained pistol with 5000 points remaining like vanilla does.
Added option to automatically put away in-hand items when trying to pick up decorations.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")
	
	dates.append('2024-04-23')
	headers.append("v2.7 A Fresh Start For WaltonWare")
	msgs.append(
"""Fixed a bug that was causing skill/aug strengths to not be consistent. (Loading older saves will give you different skill/aug strengths from before, but otherwise playable.)
New WaltonWare starting locations, previously we only had 13, now we have 40 of them!
Added 14 more bingo goals.
Vandenberg Silo improvements.
Zero Rando mode improvements.
Fixes for Randomized Music.
More aug tweaks.
Enabled randomized bot weapons by default.
OpenAugTree by WCCC (for Steam Deck or controller players)
Allow animals to be knocked unconscious.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2024-04-02')
	headers.append("v2.6.2 Time for a New Perspective")
	msgs.append(
"""Options for third person camera or fixed camera
Fixed M04 street doors not opening after talking to Paul
Fixed M03 airfield helibase, chance for the key to not be available if the enemy is not there
Randomize MaxAmmo, and maxCopies for stackable items
Laser triggers now ignore in flight projectiles (such as throwing an EMP grenade at them), and the weapons that enemies are carrying
Reduced lower-bound door/keypad strength adjustments, to try to increase variety
Explosives Only loadout
Rubber Baton for Stick With the Prod Plus, Grenades Only, and Explosives Only
More aug improvements
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	url = "https://github.com/Die4Ever/deus-ex-randomizer/releases/latest"
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

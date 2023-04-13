from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	notification = "New v2.3!"# don't forget to update below if VersionStringToInt(version) < VersionToInt(x, x, x, x):
	desc = "Anna overhaul"
	detail = "and MUCH more!"

	dates = []
	headers = []
	msgs = []

	dates.append('2023-04-13')
	headers.append("v2.3.2 IMPORTANT HOTFIX")
	msgs.append(
"""IMPORTANT HOTFIX FOR MISSION 8
    -Fixed issue where Harley Filben might not appear
Map teleporters now have better names
Improved Entrance Rando spoiler logs
Leaderboard improvements (look in the credits)""")
	
	dates.append('2023-04-10')
	headers.append("v2.3.1 Support for Vanilla? Madder. 1.75, and more!")
	msgs.append(
"""Vanilla? Madder. 1.75 was just released today!
    -Many new mechanics and features that synergize really well with the Randomizer.
    -Definitely try this out, this combination is possibly the most in depth Deus Ex experience ever!
Goal Locations Randomization improvements:
    -Mission 2 Email Computer now tells you where the Generator is and the Generator's Computer
    -Slightly updated locations for Dragon's Tooth Sword so they're a little more visible
        -Jock's Bed instead of his couch
        -Sniper's Nest is now slightly sticking out over the ledge so you can see from below
    -Mission 14 move datalink with UC computer
    -Mission 14 Email Computer now tells you where the UC Computer is
Other changes:
    -Option for menus not pausing the game
    -Balance tweaks to shotguns, throwing knives, and security computers
    -Improved physics for gibbing enemies
    -Added DiscordBot for a Discord version of Crowd Control
    -Slightly reduced weapon animation speed scaling with high skills compared to v2.3
And more! Read the Github for more details.""")
	
	dates.append('2023-03-29')
	headers.append("v2.3 Anna overhaul, balance changes, and much more!")
	msgs.append(
"""Way too many changes to list here! Including:
    Anna Navarre overhaul
    Many improvements to goal randomization
    Buffs to grenades, plasma rifle, and Private Lloyd
    Weapon animation speeds now scale with your skill
    Tweaked doors rules and hackable devices for more variety
    Bingo red highlighting for missed goals
    Score and leaderboard in the credits
And much more! Read the Github for more details.""")

	dates.append('2023-03-16')
	headers.append("v2.2.7 Various fixes")
	msgs.append(
"""Removed Vinny's fears in mission 8, which is helpful if he spawns in the sewers
Fixed mission 5 inventory placement when the player loses their items
Fixed rounding issues with text saying how many lockpicks/multitools are required
Better update notifications and news on the main menu""")

	dates.append('2023-03-10')
	headers.append("v2.2.6 Buffed chairs and many other fixes")
	msgs.append(
"""Buffed chairs by lowering their collision so you can use them for stacking and climbing
Fixed missions mask for kill Jojo bingo event, so the bingo square correctly highlights
Fixes for datacubes in non-vanilla mods
Entrance Rando fixes for Vandenberg
Fixes for music bugs when changing maps during a music transition
Improved weapon descriptions, showing damage and number of projectiles separately
Crowd Control fixes for fire weapon, trigger alarms, and next HUD theme
Fixed bingo event for learning Gunther's killphrase
Randomize weapon damage for LAMs, LAWs, Greasel Spit, Gray Spit, and MJ12 Commando rockets
Fixed limited loadouts trying to give the player banned items at the start of the game, which spammed your logs
Fixed VMD 14_Oceanlab_Lab double buttons
Death Markers now have a collision size of 12 instead of 16, so they don't get in the way as often
More possible locations for 02_NYC_Warehouse datacubes
Toned down the memes in the cutscenes
Fixed keypads that are supposed to be hidden in non-vanilla mods
Fixed 03_NYC_747 out of bounds datacube
Improved mission 8 sewer goal location so it's visible from above""")
	
	url = "https://github.com/Die4Ever/deus-ex-randomizer/releases"
	visit = "Would you like to visit "+url+" now?"

	assert len(desc) < 35
	assert len(detail) < 35
	assert len(headers) <= 5
	assert len(dates) == len(headers)
	assert len(msgs) == len(headers)
	for header in headers:
		assert len(header) < 200
	
	if data.get('map', '').upper() not in ('DX', 'DXONLY'):
		return response
	if data.get('firstword') != 'PreFirstEntry':
		return response
	
	if VersionStringToInt(version) < VersionToInt(2, 3, 0, 6):
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


def print_response(mod, version, response):
	if VersionStringToInt(version) >= VersionToInt(1, 7, 3, 3):
		print(json.dumps(response))
	else:
		print(response['status'])
		if 'notification' in response:
			print("notification: " + response['notification'])
			print(response['message'])



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

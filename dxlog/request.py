from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v2.5.1.9"
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

	dates.append('2023-07-28')
	headers.append("v2.5.1 Augmented Enemies, Walton Ware mode, and more!")
	msgs.append(
"""Augmented Enemies for an increased challenge!
Walton Ware mode: a game mode focused on quickly doing bingos and New Game+
We're also now over 200 bingo events!
New Speedrun mode: speedrun with fewer resets while still being able to enjoy higher difficulties.
Crowd Control online and simulated together for the average streamer that doesn't have many viewers
Fixes to various mirrored maps, so make sure to tell the installer to download the new mirrored maps!
Autofill passwords even in Zero Rando mode, great for Steam Deck players!
We now prevent using lockpicks/multitools on doors/keypads you have the key/code for, great for people who don't read!
New website Mods4Ever.com
And more! Read the full patch notes on Github""")

	dates.append('2023-06-22')
	headers.append("v2.5 srorriM erA eroM nuF nahT noisiveleT")
	msgs.append(
"""Mirrored Maps!
    - Play through the game with a random mix of mirrored maps, which will keep you on your toes even more than the randomizer has before!
    - Choose what percentage of maps should be mirrored!
Choose what map to start the game on
New installer program
    - Supports installing on top of vanilla, LDDP, GMDX, Revision, HX, or Vanilla? Madder.
Randomized visors for enemies
    - Gives resistance to pepper spray and gas grenades
And more! Read the full patch notes on Github""")

	dates.append('2023-05-24')
	headers.append("v2.4.1 Fixes, Balance Tweaks, and Remembering Recently Skipped Songs!")
	msgs.append(
"""A little more ammo for Stick With the Prod modes
Serious Sam mode tweaked settings to increase ammo and medkits
Rando options menu
    - Option for disabling memes
    - Remembering recently skipped songs
        - This is still different from disabling the song since it's temporary
        - Remembers the 10 most recently skipped songs for as long as the game is open
    - Option for enemies throwing melee weapons when dying
- Merging picked up melee weapons you already have (helps if you have the melee weapons option set to don't throw)
- Medbots/Repairbots greatly reduced cooldowns
- Detection of bad dynamic patrol routes, so enemies don't get stuck standing still, they will switch to wandering
- M12 Vandenberg Command, added a ShopLight for climbing to the roof (#446)
- AugMuscle now has randomized cost instead of strength
- Shotguns reduced range and accuracy
- Don't swap M03 Airfield boatguard with other enemies, because he has the east gate key
- Tweaked scoring for flags, see the Wiki
- Crowd Control 2.0 preparation
And more!""")

	dates.append('2023-05-16')
	headers.append("v2.4 The Enemies Are On Patrol!")
	msgs.append(
"""Huge overhaul of enemy randomization:
    - Randomized patrol routes
    - Random chance to have a helmet or not, affecting damage resistance for their head
    - Improved shuffling
    - Faction-appropriate pairings (no more thugs with MJ12)
    - New appearances
New game modes:
    - Zero Rando: great for first time Deus Ex players
    - Randomizer Lite: subtle randomization without affecting the mood of the game
    - Serious Sam: tons of enemies with tuned difficulty to compensate
Option to use music from Unreal and Unreal Tournament
Improved accessibility
Less pixel hunting
Important items will be easier to spot instead of having to pixel hunt for them
Balance tweaks
And much more!""")

	dates.append('2023-04-14')
	headers.append("v2.3.3 ANOTHER HOTFIX")
	msgs.append(
"""ANOTHER IMPORTANT HOTFIX FOR MISSION 8
    -Fixed issue where Harley Filben might not appear
        (for real this time!)
Improved AI getting closer to use shotguns
Fixed teleporter names in the training mission""")
	
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

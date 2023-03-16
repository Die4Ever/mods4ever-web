from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	notification = "New v2.2.7 available!"
	desc = "Various fixes"
	detail = ""

	dates = []
	headers = []
	msgs = []

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
	
	dates.append('2023-02-16')
	headers.append("v2.2.5 Randomly swapped music, and much more")
	msgs.append(
"""Randomly swapped music: each song will be replaced with a different song.
Spoiler-free Goal Locations lists in the Notes screen (for people too lazy to open the Wiki)
Moved "Confirm Note Deletion" to Rando settings menu
More goal locations for mission 5 Paul and mission 10 Jaime (see the Wiki)
Mission 5 guaranteed weapon now has a slightly randomized location
Greatly increased knock backs (like in Blood!)
Improved aug descriptions for AugVision, AugLight, AugHealing
Increased Button1 collision size
Smaller collision for helicopters, so you can walk around Jock at the Chateau!
Credits time table improvements
Stats in credits for set seed vs random seed, saves, autosaves, and loads
Fix keypad bugs for non-vanilla mods
Fixed Vandenberg Command override keypads for VMD
Fixed wonky front door in 09_NYC_SHIP, when you talk to Vinny now the door will be unlocked
Fixed Paris Metro Hostel manager talking to you while flying away softlock
Some more death screen hints
Small tweak to Gunther chapel location
Upgrading swimming skill while in water will now properly update your stats immediately
Howard Stronger: now he has ballistic armor (in VMD he will actually use the armor, otherwise I gave him extra health to pretend he's using the armor), and more randomized weapons. I've also removed his fears.
Plasma Rifle buffs: from 9 to 14 damage (used to be 8 previously), removed robot's damage resistance, reduced blast radius, increased ammo
PS40 tweaks: 200 damage instead of 400 and reduced blast radius, but removed robot's damage resistance
Plasma rifle now slightly more common for enemies (5% to 7%), PS40 slightly less common (5% to 3%)
EMP grenades now disable enemy shields (MJ12 Commandos, Gunther, etc), this allows you to EMP them and then things like plasma, fire, the prod, and tranquilizier darts will be more effective against them. Maybe now you'll have a chance in Stick With the Prod Plus mode?
MJ12 Commandos now take bonus damage from Sabot rounds (although you might wanna save it for spiderbots instead!)
Grays now take a tenth damage from fire and plasma, instead of being completely immune
Vision Enhancement aug will now show goals through walls, but to compensate it has less view distance at max level than it did previously""")
	
	dates.append('2023-02-01')
	headers.append("v2.2.4 Continuous music and many fixes")
	msgs.append(
"""Continuous Music! Music now smoothly continues across maps and even when loading saves!
    This can be disabled in the Rando settings menu just in case it causes issues, let us know!
    Also fixed vanilla music bug of reentering level with combat music being stuck in ambient music
Update goal locations for Walton Simons in the Oceanlab crew module, and Vandenberg Silo Jock water location
Fixed Jock names on Vandenberg Silo to reduce confusion, highlight him to see which one is which
Fixed HUD highlight text for how many shots/hits to break a door with the current weapon
Fixes for projectile damage randomization
Adjusted plasma rifle damage (slightly stronger for vanilla, slightly weaker for some other mods, plasma rifle has complicated damage calculations)
Apply more map fixes to Vanilla? Madder.
Fixed bingo highlighting for some goals
Fixed merchant flags expiration, so he remembers he already sold you things
Remove debug messages about keypads
Make the ship ramp unbreakable
Give credit to medbots and repairbots for their explosion kills https://twitter.com/DxRandoActivity/status/1618477613088899072
Reduce health on ship weld points so they always only take 1 GEP rocket
Brightness boost now also fixes saturation so colors don't get messed up
Improved look of bingo screen in credits
Don't reduce ammo that enemies can use, only reduce what they drop""")

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
	
	if VersionStringToInt(version) < VersionToInt(2, 2, 6, 5):
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

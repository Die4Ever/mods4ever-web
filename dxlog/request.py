from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	notification = "New v2.2.6 available!"
	desc = "Buffed chairs"
	detail = "and much more!"

	longmsg = "v2.2.6 Buffed chairs and many other fixes!\n\n"
	longmsg += """Buffed chairs by lowering their collision so you can use them for stacking and climbing
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
Improved mission 8 sewer goal location so it's visible from above"""
	longmsg = longmsg.replace('\n', '|n')

	url = "Would you like to visit https://github.com/Die4Ever/deus-ex-randomizer/releases now?"
	assert len(desc) < 35
	assert len(detail) < 35
	if data.get('map', '') not in ('DX', 'DXONLY'):
		return response
	
	if VersionStringToInt(version) < VersionToInt(2, 2, 6, 5):
		response['notification'] = notification
		response['message'] = desc
		response['message'] += "|n" + detail
		response['message'] += "|n" + url
		response['longmsg'] = longmsg + "|n|n" + url
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

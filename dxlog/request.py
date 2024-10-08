from dxlog.base import *

def update_notification(mod, version, data):
	response = {}
	latest_version = "v3.2.2.2"
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
	
	dates.append('2024-10-09')
	headers.append("v3.2.2 Halloween Mode Tweaks")
	msgs.append(
"""When playing with Fixed Saves (such as in Halloween mode) there is now 1 Memory Containment Unit in each map, instead of being just an 80% chance
Jail no longer takes away your Memory Containment Units
Mr. H can now swim
Fixed regen not getting boosted past level 4 when using Synthetic Heart
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")
	
	dates.append('2024-10-01')
	headers.append("v3.2.1 Halloween Hotfix!")
	msgs.append(
"""Fixes for cosmetics outside of Halloween modes, especially the lighting.
New special light aug tweaks for Halloween Modes!
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")
	
	dates.append('2024-10-01')
	headers.append("v3.2 Happy Halloween!")
	msgs.append(
"""Many new game modes for Halloween! Check out our new trailer video or just download and play!
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

	dates.append('2024-09-06')
	headers.append("v3.1.1 Hotfix")
	msgs.append(
"""Fixed an issue in Vandenberg Command with the comms door sometimes not opening after killing the enemy bots.
Fixed rounding issues with timers for armors.
Color options for Tech Goggles/Vision Enhancement.
And more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")
	
	dates.append('2024-08-29')
	headers.append("v3.1 Area 51: Now With Added Confusion!")
	msgs.append(
"""Area 51 goal locations are now randomized.
Many balance tweaks.
Cats now purr when you pet them!
And MUCH more! Read the full patch notes on Github, also check out our new website Mods4Ever.com""")

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

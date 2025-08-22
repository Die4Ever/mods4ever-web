from apis.dxrando import dxrando_news
from dxlog.base import *
import random

def update_notification(mod, version, data):
	response = {}
	latest_version = "v3.6.0.2"
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
	news = dxrando_news()[:5]
	for n in news:
		dates.append(n.date)
		headers.append(n.header)
		msg = ''
		for change in n.changes:
			msg += '~ ' + change + '|n|n'
		if n.isVersionUpdate and n.andMore:
			msg += 'And more! Download from Mods4Ever.com or read the full patch notes on Github.'
		elif n.isVersionUpdate:
			msg += 'Download from Mods4Ever.com or read the full patch notes on Github.'
		else:
			msg = msg[:-4]
		msgs.append(msg)

	latest_version_int = VersionStringToInt(latest_version)
	assert latest_version_int > 0

	url = "https://mods4ever.com"
	visit = "Would you like to visit "+url+" now?"
	url += '/?utm_source=game&utm_medium=onlineupdate&utm_version=' + str(VersionStringToInt(version)) + '&utm_campaign=' + str(latest_version_int)

	assert len(desc) < 35
	assert len(detail) < 35
	assert len(headers) == 5
	assert len(dates) == len(headers)
	assert len(msgs) == len(headers)
	if news[0].isVersionUpdate:
		assert short_version in headers[0]
		assert short_version in desc

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
	if VersionStringToInt(version) < VersionStringToInt('v3.0.0.6'):
		notifs = ['YOU ARE SO FAR BEHIND ON UPDATES!', 'PLEASE DOWNLOAD THE UPDATE!', "DON'T YOU WANT TO PET THE DOG?"]
		response['notification'] = random.choice(notifs)
	
	for i in range(len(headers)):
		response['newsdate' + str(i)] = dates[i]
		response['newsheader' + str(i)] = headers[i]
		response['newsmsg' + str(i)] = msgs[i]
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

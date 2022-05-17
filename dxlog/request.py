from dxlog.base import *

def update_notification(mod, version):
	response = {}
	notification = "New v1.9 available!"
	desc = "Vanilla? Madder."
	detail = ""
	assert len(desc) < 35
	assert len(detail) < 35
	if VersionStringToInt(version) < VersionToInt(1, 9, 0, 3):
		response['notification'] = notification
		response['message'] = desc
		response['message'] += "|n" + detail
		response['message'] += "|nWould you like to visit https://github.com/Die4Ever/deus-ex-randomizer/releases now?"
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
	content = ""

	try:
		#while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
		if content_length > 0:
			content = content + sys.stdin.read()
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

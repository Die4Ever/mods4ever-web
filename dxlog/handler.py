from dxlog.base import *
from dxlog.db import write_db
from dxlog.parsing import parse_content
from dxlog.request import generate_response, update_notification


def handle_telem(postdata:bytes, ip, params):
	response = {'status': 'ok'}
	try:
		content = read_binary_content(postdata)
		content = content.replace('\x00','').replace('\r','')
	except Exception as e:
		logex(e)

	version = params.get('version', "v1.0.0")
	if VersionStringToInt(version) <= VersionToInt(1, 1, 0, 0):
		warn('unknown version '+version)
	mod = params.get('mod')
	
	try:
		#content = try_encodings(content, [('utf-8', 'replace')])
		data = parse_content(content)
		response.update(update_notification(mod, version, data))
		config = get_config()
		#write_log(mod, version, ip, content, response)
	except Exception as e:
		response['status'] = 'ERROR: failed to parse content'
		print("failed to parse content")
		err("failed to parse content")
		logex(e)

	try:
		db_data = write_db(mod, version, ip, content, config, data)
		response.update(db_data)
	except Exception as e:
		response['status'] = 'ERROR: failed to write to db'
		print("failed to write to db")
		err("failed to write to db")
		logex(e)
	
	return generate_response(mod, version, response)

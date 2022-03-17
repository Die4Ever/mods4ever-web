#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging

from dxlog.base import *
from dxlog.db import *
from dxlog.parsing import *
from dxlog.twitter import *
from dxlog.request import *

def main():
	#cgitb.enable(display=1, logdir=logdir)
	print("Status: 200" )
	print("")

	content, content_length, ip, qps = get_request()

	if ip is None:
		warn('no REMOTE_ADDR?')
		return

	response = {}
	if len(content) != content_length:
		response['status'] = "ERROR: only received "+str(len(content))+"/"+str(content_length)+" bytes"
	else:
		response['status'] = "ok received "+str(len(content))+"/"+str(content_length)+" bytes"

	version = qps.get('version', "v1.0.0")
	if VersionStringToInt(version) <= VersionToInt(1, 1, 0, 0):
		warn('unknown version '+version)
	mod = qps.get('mod')

	response.update(update_notification(mod, version))
	
	config = get_config()

	#write_log(mod, version, ip, content, response)
	
	try:
		db_data = write_db(mod, version, ip, content,config)
		response.update(db_data)
	except Exception as e:
		print("failed to write to db")
		err("failed to write to db")
		logex(e)
	
	print_response(mod, version, response)

if __name__ == '__main__':
	main()

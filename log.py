#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging

if sys.version_info[0] < 3:
    raise ImportError('Python < 3 is unsupported.')

if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise ImportError('Python < 3.5 is unsupported.')

#import cgi
import cgitb
#cgitb.enable()
import sys
import time
import requests
import json
import os
import datetime
import pathlib
import mysql.connector

def main():
	debug=False

	#cgitb.enable()
	cgitb.enable(display=1, logdir="/home/rcarro/dxrando_logs/")
	#exit(0)

	print("Status: 200" )
	print("")
	print( os.environ.get('REMOTE_ADDR') )

	content, content_length = get_content()

	response = ""
	if len(content) != content_length:
		response = "ERROR: only received "+str(len(content))+"/"+str(content_length)+" bytes"
	else:
		response = "ok received "+str(len(content))+"/"+str(content_length)+" bytes"

	version = get_version()

	if version != 'v1.7.2.9' and 'v1.7.3' not in version:
		response += " notification: New v1.7.2 available!\nMany updates!|nWould you like to visit https://github.com/Die4Ever/deus-ex-randomizer/releases now?"

	write_log(version, content, response)
	try:
		write_db(version, content)
	except Exception as e:
		print("failed to write to db")
		print("failed to write to db", file=sys.stderr)
		print(repr(e), file=sys.stderr)

	print(response)


def write_db():
	config = {}
	with open('/home/rcarro/dxrando_logs/config.json', 'r') as f:
		config = json.load(f)
	mydb = None
	try:
		mydb = None# mysql.connector.connect(**config)
	except Exception as e:
		print("failed to connect to db")
		print("failed to connect to db", file=sys.stderr)
		print(repr(e), file=sys.stderr)
	



def get_version():
	version = ""
	if os.environ.get('QUERY_STRING'):
		version = os.environ.get('QUERY_STRING')
		version = version.replace("version=", "").replace("%20", " ")
	return version


def write_log(version, content, response):
	try:
		now = datetime.datetime.now()
		foldername = "/home/rcarro/dxrando_logs/"+ now.strftime("%Y-%m") +"/"
		filename = foldername + os.environ.get('REMOTE_ADDR') + "_" + version + ".txt"
		pathlib.Path(foldername).mkdir(parents=True, exist_ok=True)
		with open( filename, "a") as file:
			file.write( "\n" + now.strftime("%Y-%m-%d %H:%M:%S") + ": " + version + ": " + response +"\n" + content + "\n")
	except Exception as e:
		print(repr(e))


def get_content():
	s_content_length = os.environ.get('CONTENT_LENGTH')
	if s_content_length is None:
		s_content_length = "0"
	else:
		s_content_length = str(s_content_length)

	content_length = int(s_content_length)
	content = ""

	try:
		#while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
		content = content + sys.stdin.read()
		content = content.replace('\x00','').replace('\r','')
	except Exception as e:
		print(repr(e))
	
	return content, content_length


main()

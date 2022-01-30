#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging

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
debug=False

#cgitb.enable()
cgitb.enable(display=1, logdir="/home/rcarro/dxrando_logs/")
#exit(0)

print("Status: 200" )
print("")
print( os.environ.get('REMOTE_ADDR') )

s_content_length = os.environ.get('CONTENT_LENGTH')
if s_content_length is None:
	s_content_length = "0"
else:
	s_content_length = str(s_content_length)

content_length = int(s_content_length)
now = datetime.datetime.now()
args = ""

try:
	#while len(args) < content_length AND (datetime.datetime.now() - now).total_seconds() < 10:
	args = args + sys.stdin.read()
	args = args.replace('\x00','').replace('\r','')
except Exception as e:
	print(repr(e))

response = ""
if len(args) != content_length:
	response = "ERROR: only received "+str(len(args))+"/"+s_content_length+" bytes"
else:
	response = "ok received "+str(len(args))+"/"+s_content_length+" bytes"

version = ""
if os.environ.get('QUERY_STRING'):
	version = os.environ.get('QUERY_STRING')
	version = version.replace("version=", "").replace("%20", " ")

if version != 'v1.7.2.9' and 'v1.7.3' not in version:
	response += " notification: New v1.7.2 available!\nMany updates!|nWould you like to visit https://github.com/Die4Ever/deus-ex-randomizer/releases now?"

try:
	foldername = "/home/rcarro/dxrando_logs/"+ now.strftime("%Y-%m") +"/"
	filename = foldername + os.environ.get('REMOTE_ADDR') + "_" + version + ".txt"
	pathlib.Path(foldername).mkdir(parents=True, exist_ok=True)
	with open( filename, "a") as file:
		file.write( "\n" + now.strftime("%Y-%m-%d %H:%M:%S") + ": " + version + ": " + response +"\n" + args + "\n");
except Exception as e:
	print(repr(e))

print(response)

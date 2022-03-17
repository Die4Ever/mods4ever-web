import sys

if sys.version_info[0] < 3:
	raise ImportError('Python < 3 is unsupported.')
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
	raise ImportError('Python < 3.5 is unsupported.')

import os
from os.path import dirname
import datetime
import pathlib
import re
import traceback
import math
import json
#from csv import excel_tab
#from ctypes import sizeof
import cgitb
import time
import datetime

path = os.path.dirname(os.path.realpath(dirname(__file__)))
logdir = path + "/dxrando_logs/"
location_split = re.compile('\s*,\s*')

def get_config():
	with open(path+'/config.json', 'r') as f:
		return json.load(f)
	err("failed to load config")
	return {}


def write_log(mod, version, ip, content, response):
	warn('obsolete write_log function')
	try:
		now = datetime.datetime.now()
		foldername = logdir + now.strftime("%Y-%m") +"/"
		filename = foldername + ip + "_" + version + ".txt"
		pathlib.Path(foldername).mkdir(parents=True, exist_ok=True)
		with open( filename, "a") as file:
			file.write( "\n" + now.strftime("%Y-%m-%d %H:%M:%S") + ": " + version + ": " + response['status'] +"\n" + content + "\n")
	except Exception as e:
		logex(e)


def unrealscript_sanitize(s):
	allow = "-_[]\{\}()`~!@#$%^&*\+=|;:<>,."
	s = re.sub('[^\w\d %s]' % allow, '', str(s))
	s = re.sub('\s+', ' ', s)
	return s


error_log = logdir + "error_log"
def write_error_log(msg):
	print(msg, file=sys.stderr)
	with open(error_log, "a") as file:
			file.write(msg+"\n")


def info(msg):
	write_error_log("INFO: "+msg)

def warn(msg):
	write_error_log("WARNING: "+msg)

def err(msg):
	write_error_log("ERROR: "+msg)

def logex(e):
	write_error_log("ERROR: "+traceback.format_exc())


# copied from DXRando
def VersionToInt(major, minor, patch, build):
	return int(major)*1000000+int(minor)*10000+int(patch)*100+int(build)

def VersionStringToInt(version):
	try:
		m = re.search(r'v(\d+)\.(\d+)\.(\d+)(\.(\d+))?', version)
		group5 = m.group(5)
		if group5 is None:
			group5 = "0"
		return VersionToInt(m.group(1), m.group(2), m.group(3), group5)
	except Exception as e:
		print("VersionStringToInt error parsing "+version)
		logex(e)
	return 0

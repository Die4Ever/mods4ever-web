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
import cgitb
import time
import datetime
import ctypes
from better_profanity import profanity

profanity_loaded = False
def load_profanity_filter():
	global profanity_loaded
	if profanity_loaded:
		return
	profanity_loaded = True
	profanity.load_censor_words(whitelist_words=[
		'thug', 'hooker', 'junkie', 'god', 'hell', 'urinal', 'ass', 'asses',
		'717', 'tit', 't1t', 'titi', 'titis', 'tits', 'titt', 'titts', 'teat', 'teats', 'teets', 'toots',
		'teste', 'testee', 'testes', 'loin', 'omg', 'nad'
	])
	
	custom_badwords = get_config().get('custom_badwords',[])
	profanity.add_censor_words(custom_badwords)


path = os.path.dirname(os.path.realpath(dirname(__file__)))
logdir = path + "/dxrando_logs/"
location_split = re.compile('\s*,\s*')

_config = None
def get_config():
	global _config
	if _config:
		return _config
	with open(path+'/config.json', 'r') as f:
		_config = json.load(f)
		return _config
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
def write_error_log(prefix:str, msg:str, *args):
	try:
		print(prefix, msg, file=sys.stderr)
		with open(error_log, "a") as file:
				print(prefix, msg, *args, file=file)
	except Exception as e:
		try:
			with open(error_log, "a") as file:
					print('ERROR IN write_error_log!', file=file)
					logex(e)
					print(msg, file=file)
					for s in [*args]:
						print(s, file=file)
		except:
			pass

def read_binary_content(data:bytes) -> str:
	# try:
	# 	with open(logdir + 'binlog', 'ab') as file:
	# 		file.write(data)
	# 		file.write(b'\n\n')
	# except Exception as e:
	# 	logex(e)
	
	try:
		return data.decode('utf-8', 'ignore')
	except Exception as e:
		logex(e)
		return data.decode('iso_8859_1', 'ignore')
	return data.decode()

def debug(msg, *args):
	#write_error_log("DEBUG:", msg)
	pass

def info(msg, *args):
	write_error_log("INFO:", msg, *args)

def warn(msg, *args):
	write_error_log("WARNING:", msg, *args)

def err(msg, *args):
	write_error_log("ERROR:", msg, *args)

def logex(e):
	write_error_log("ERROR:", traceback.format_exc(100))


# copied from DXRando
def VersionToInt(major, minor, patch, build):
	return int(major)*1000000+int(minor)*10000+int(patch)*100+int(build)


def SplitVersionString(version):
	try:
		m = re.search(r'v(\d+)\.(\d+)\.(\d+)(\.(\d+))?( (\w+))?', version)
		group5 = m.group(5)
		if group5 is None:
			group5 = "0"
		return (m.group(1), m.group(2), m.group(3), group5, m.group(7))
	except Exception as e:
		print("SplitVersionString error parsing "+version)
		logex(e)
	return None


def VersionStringToInt(version:str):
	try:
		m = SplitVersionString(version)
		return VersionToInt(m[0], m[1], m[2], m[3])
	except Exception as e:
		print("VersionStringToInt error parsing "+version)
		logex(e)
	return 0

def VersionStringIsStable(version:str):
	try:
		m = SplitVersionString(version)
		return not m[4]
	except Exception as e:
		print("VersionStringIsStable error parsing "+version)
		logex(e)
	return False

def PlaythroughIdToHex(playthrough_id):
	# int playthrough_id to make sure the player doesn't sneak anything into the hashtag
	try:
		playthrough_id = int(playthrough_id)
		playthrough_id = ctypes.c_uint32(playthrough_id).value# force unsigned
		return hex(playthrough_id)[2:]# hex to make it shorter?
	except:
		return ''

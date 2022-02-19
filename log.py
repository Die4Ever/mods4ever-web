#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging

import sys
if sys.version_info[0] < 3:
    raise ImportError('Python < 3 is unsupported.')

if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise ImportError('Python < 3.5 is unsupported.')

#import cgi
import cgitb
#cgitb.enable()
import time
import requests
import json
import os
import datetime
import pathlib
import mysql.connector
import mysql.connector.errorcode

path = os.path.dirname(os.path.realpath(__file__))
logdir = path + "/dxrando_logs/"

def main():
	debug=False

	#cgitb.enable()
	cgitb.enable(display=1, logdir=logdir)
	#exit(0)

	print("Status: 200" )
	print("")
	print( os.environ.get('REMOTE_ADDR') )

	content, content_length = get_content()

	if content_length == 0:
		run_tests()
		return

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
		err("failed to write to db")
		err(repr(e))

	print(response)


def get_db_config():
	with open(path+'/config.json', 'r') as f:
		return json.load(f)
	err("failed to load db config")
	return {}


def db_connect():
	config = get_db_config()
	db = None
	try:
		db = mysql.connector.connect(**config)
	except Exception as e:
		print("failed to connect to db")
		err("failed to connect to db")
		err(repr(e))
	return db


def write_db(version, content):
	db = db_connect()
	cursor = None
	try:
		create_tables(db)
		cursor = db.cursor()
	except Exception as e:
		print("failed to write to db")
		err("failed to write to db")
		err(repr(e))
	
	cursor.close()
	db.close()


def create_table(db, name, desc):
	cursor = db.cursor()
	desc = "CREATE TABLE " + name + " (" + desc + ")"
	try:
		cursor.execute("SHOW CREATE TABLE deaths")
		curr_desc = ""
		for (table, tdesc) in cursor:
			curr_desc = tdesc
		if curr_desc.count(',') != desc.count(','):
			info("old deaths table: "+curr_desc)
			try:
				cursor.execute("RENAME TABLE deaths TO old_deaths")
			except Exception as e:
				err(repr(e))
			cursor.execute(desc)
	except mysql.connector.Error as e:
		if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
			print("table already exists.")
		else:
			err(repr(e))
	cursor.close()


def create_tables(db):
	create_table(db, "deaths", "id int unsigned NOT NULL AUTO_INCREMENT, PRIMARY KEY(id)")
	create_table(db, "logs", "id int unsigned NOT NULL AUTO_INCREMENT, PRIMARY KEY(id)")

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
		if content_length > 0:
			content = content + sys.stdin.read()
			content = content.replace('\x00','').replace('\r','')
	except Exception as e:
		print(repr(e))
	
	return content, content_length


def run_tests():
	info("running tests...")
	info("path: "+os.path.dirname(os.path.realpath(__file__)))
	info("cwd: "+os.getcwd())
	info("logdir: "+logdir)
	info("db config: " + repr(get_db_config()))
	info("test success")

error_log = logdir + "error_log"
def write_error_log(msg):
	print(msg, file=sys.stderr)
	with open(error_log, "a") as file:
			file.write(msg+"\n")


def info(msg):
	write_error_log("INFO: "+msg)

def warn(msg):
	write_error_log("INFO: "+msg)

def err(msg):
	write_error_log("INFO: "+msg)

main()

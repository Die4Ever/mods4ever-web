import mysql.connector
import mysql.connector.errorcode
from dxlog.base import *
from dxlog.parsing import parse_content
from dxlog.twitter import tweet
from dxlog.deaths import *

def db_connect(config):
	db = None
	
	dbconfig = {}
	dbconfig["user"]=config["user"]
	dbconfig["password"]=config["password"]
	dbconfig["host"]=config["host"]
	dbconfig["database"]=config["database"]
	dbconfig["raise_on_warnings"]=config["raise_on_warnings"]
	dbconfig["charset"]='utf8'
	dbconfig["use_unicode"]=True
	
	try:
		db = mysql.connector.connect(**dbconfig)
	except Exception as e:
		print("failed to connect to db")
		err("failed to connect to db")
		logex(e)
	return db

def try_encodings(content:str, encodings:list):
	bcontent = b''
	ret = ''
	for e in encodings:
		try:
			bcontent = b''
			if len(e) > 1:
				bcontent = content.encode(e[0], e[1])
			else:
				bcontent = content.encode(e[0])
			if len(e) > 1:
				c = bcontent.decode(e[0], e[1])
			else:
				c = bcontent.decode(e[0])
			if not ret and c:
				ret = c
		except Exception as ex:
			try:
				logex(ex)
				err(bcontent, e)
			except Exception as e2:
				logex(e2)
				err(e)

	return ret


def write_db(mod, version, ip, content:str, config, data):
	ret = {}
	db = db_connect(config)
	cursor = None
	
	if db == None:
		return ret
	
	try:
		data['ip'] = ip
		d=data
		cursor = db.cursor(dictionary=True)
		d = get_playthrough(cursor, mod, ip, d)
		log_id = 0
		try:
			cursor.execute(
				"INSERT INTO logs SET created=NOW(), "
				+ "firstword=%s, modname=%s, version=%s, ip=%s, map=%s, seed=%s, flagshash=%s, playthrough_id=%s",
				(d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id') ))
			log_id = cursor.lastrowid
			debug("inserted logs id "+str(log_id))
		except Exception as e:
			print("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			err("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			logex(e)
			err(content)
			return
		
		try:
			cursor.execute(
				'INSERT INTO logs_messages SET id=%s, message=%s',
				(log_id, content)
			)
		except Exception as e:
			err("failed to write to db logs_messages, db values: ", d.get('firstword'), mod, version, ip, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
			logex(e)
			err(content)

		ret = {}
		
		if ip not in config.get('banned_ips',[]):
			events = d.get('events', [])
			if len(events) > 0:
				info('log_id: '+str(log_id)+', got events: '+repr(events), repr(d))
			for event in events:
				try:
					if event['type'] == 'DEATH':
						log_death(cursor, log_id, event)
					if event["type"] == "BeatGame":
						log_beatgame(cursor, log_id, mod, version, event, d)
					if event['type'] == 'QueryLeaderboard':
						ret.update(QueryLeaderboardGame(cursor, event, d.get('playthrough_id')))
				except Exception as e:
					err("failed to handle event", event.get('type'), e)
					logex(e)
			try:
				tweet(config, d, events, mod, version)
			except Exception as e:
				err("failed to toot")
				err(repr(events))
				logex(e)
		else:
			warn("IP " + ip + " is banned!")
		
		db.commit()
		if d.get('firstword'):
			ret.update(select_deaths(cursor, mod, d.get('map')))
	except Exception as e:
		err("failed to write to db, db values: ", d.get('firstword'), mod, version, ip, content, d.get('map'), d.get('seed'), d.get('flagshash'), d.get('playthrough_id'))
		logex(e)
		err(content)
	
	db.commit()
	cursor.close()
	db.close()
	return ret


def get_playthrough(cursor, mod, ip, d):
	if 'playthrough_id' in d and 'seed' in d and 'flagshash' in d:
		return d
	
	if 'playthrough_id' not in d:
		cursor.execute("SELECT playthrough_id, seed, flagshash FROM logs WHERE ip=%s ORDER BY id DESC LIMIT 1", (ip,))
	else:
		cursor.execute("SELECT playthrough_id, seed, flagshash FROM logs WHERE ip=%s AND playthrough_id=%s ORDER BY id DESC LIMIT 1", (ip,d['playthrough_id']))
	
	for (r) in cursor:
		if 'playthrough_id' in r:
			d['playthrough_id'] = r['playthrough_id']
		if 'seed' in r and 'seed' not in d:
			d['seed'] = r['seed']
		if 'flagshash' in r and 'flagshash' not in d:
			d['flagshash'] = r['flagshash']
	return d


def get_data(cursor, log_id, d):
	if 'ip' not in d:
		cursor.execute("SELECT ip FROM logs WHERE id=%s ORDER BY id DESC LIMIT 1", (log_id,))
		for (r) in cursor:
			d['ip'] = r['ip']
	
	cursor.execute("SELECT message FROM logs JOIN logs_messages USING(id) WHERE ip=%s AND playthrough_id=%s AND firstword IS NOT NULL AND id <= %s ORDER BY id DESC LIMIT 1", (d['ip'], d['playthrough_id'], log_id))
	for (r) in cursor:
		if 'message' in r:
			data = parse_content(r['message'])
			data.update(d)
			d = data
	return d


def write_leaderboard_data(cursor, log_id, d):
	for (k,v) in d.items():
		try:
			if type(v) == list or type(v) == dict:
				continue
			cursor.execute(
				'INSERT INTO leaderboard_data SET '
				+ 'log_id=%s, name=%s, value=%s '
				+ 'ON DUPLICATE KEY UPDATE '
				+ 'value=VALUES(value) ',
				(log_id, k, v)
			)
		except Exception as e:
			warn('write_leaderboard_data', log_id, k, v)
			logex(e)


def log_beatgame(cursor, log_id, mod, version, e, d):
	if VersionStringToInt(version) < VersionToInt(2, 3, 0, 1):
		return
	try:
		bingo_spots = 0
		for x in range(0,5):
			for y in range(0,5):
				bingoTag = "bingo-"+str(x)+"-"+str(y)
				square = e.get(bingoTag)
				if square and square['progress'] >= square['max'] and square['event'] != "Free Space":
					bingo_spots += 1

		name = unrealscript_sanitize(e['PlayerName'])
		
		cursor.execute(
			'INSERT INTO leaderboard SET '
			+ 'log_id=%s, name=%s,  totaltime=%s,  gametime=%s,           score=%s,   flagshash=%s,       setseed=%s,      stable_version=%s,              rando_difficulty=%s,   combat_difficulty=%s,   deaths=%s,   loads=%s,       saves=%s,       bingos=%s,           bingo_spots=%s, ending=%s,   newgameplus_loops=%s,   initial_version=%s',
			(  log_id,    name,     e['realtime'], e['timewithoutmenus'], e['score'], d.get('flagshash'), e['bSetSeed'],   VersionStringIsStable(version), e['rando_difficulty'], e['combat_difficulty'], e['deaths'], e['LoadCount'], e['SaveCount'], e['NumberOfBingos'], bingo_spots,    e['ending'], e['newgameplus_loops'], e['initial_version'])
		)

		d = get_data(cursor, log_id, d)
		write_leaderboard_data(cursor, log_id, d)

		e['placement'] = GetLeaderboardPlacement(cursor, e, d.get('playthrough_id'))
	except Exception as ex:
		err('log_beatgame failed', log_id, e)
		logex(ex)
		return
	

def _QueryLeaderboard(cursor, version=VersionToInt(2,3,0,0), maxdays=365, SortBy='score', Filters={}):
	if SortBy == 'totaltime':
		SortBy = " ORDER BY totaltime ASC"
	else:
		SortBy = " ORDER BY score DESC"

	try:
		GameMode = int(Filters.get('GameMode', -1))
	except:
		GameMode = -1
	
	try:
		difficulty = int(Filters.get('difficulty', -1))
	except:
		difficulty = -1
	
	Filters = ''
	FilterFormat = ' INNER JOIN leaderboard_data as t_{name} ON(leaderboard.log_id = t_{name}.log_id AND t_{name}.name="{name}" AND t_{name}.value = {val}) '
	if GameMode >= 0:
		Filters += FilterFormat.format(name='gamemode', val=GameMode)
	if difficulty >= 0:
		Filters += FilterFormat.format(name='difficulty', val=difficulty)
	
	query = ("SELECT "
		+ "leaderboard.log_id, leaderboard.name, totaltime, score, leaderboard.flagshash, setseed, seed, date(created) as end_date, UNIX_TIMESTAMP()-UNIX_TIMESTAMP(created) as age, playthrough_id, "
		+ "rando_difficulty, combat_difficulty, deaths, loads, saves, bingos, bingo_spots, newgameplus_loops, initial_version, setseed, stable_version "
		+ "FROM leaderboard JOIN logs ON(leaderboard.log_id=logs.id) "
		+ Filters
		+ "WHERE initial_version >= %s AND created >= NOW()-INTERVAL %s DAY "
		+ SortBy)

	cursor.execute(query,
		(int(version), int(maxdays)))


def GetCutaway(leaderboard, slot):
	start = slot - 2
	start = max(start, 0)
	end = slot + 3
	end = min(end, len(leaderboard))
	end = max(end, start)
	return (start, end)

def _GroupLeaderboard(cursor, event, playthrough_id):
	placement = 1
	users = set()
	leaderboard = []
	newplacement = None
	mypbspot = None
	show_next = False
	for (d) in cursor:
		name = unrealscript_sanitize(d['name'])
		if event.get('PlayerName') == name:
			if mypbspot is None:
				mypbspot = len(leaderboard)

		# check if we need to show this run or not
		if event.get('PlayerName') == name and playthrough_id == d['playthrough_id']:
			if newplacement is None:
				newplacement = len(leaderboard)
			show_next = True# show the next run from this user, to see what score they just beat
		elif event.get('PlayerName') == name and show_next and name in users:
			show_next = False# this is my run that I just beat, so I wanna see it
		elif name in users:
			continue# don't show this run
		# ok show the run
		place = placement
		if name in users:
			place = '--'# not my best score
		else:
			placement += 1# yes my best score

		namedate = name
		if 'end_date' in d:
			namedate += ' (' + str(d['end_date']) + ')'
		data = { **d, 'name': namedate, 'place': place }
		leaderboard.append(data)
		users.add(name)
	return {'leaderboard':leaderboard, 'mypbspot':mypbspot, 'newplacement':newplacement}


def GroupLeaderboard(cursor, event, playthrough_id, max_len=15):
	d = _GroupLeaderboard(cursor, event, playthrough_id)
	(leaderboard, mypbspot, newplacement) = (d['leaderboard'], d['mypbspot'], d['newplacement'])
	if not max_len:
		return leaderboard
	
	(pbstart,pbend,newstart,newend) = (None,None,None,None)
	if mypbspot is not None:
		(pbstart,pbend) = GetCutaway(leaderboard, mypbspot)
	if newplacement is not None:
		(newstart,newend) = GetCutaway(leaderboard, newplacement)
	
	if mypbspot is not None and newplacement is not None:
		# handle overlap
		pbend = min(pbend, newstart)
	
	after = None
	afterend = None
	ret = []
	if mypbspot is not None and pbstart != pbend:
		ret += leaderboard[pbstart:pbend]
		after = pbend
	if newplacement is not None and newstart != newend:
		ret += leaderboard[newstart:newend]
		after = newend
	
	end = max_len - len(ret)
	if mypbspot is not None and pbstart != pbend:
		end  = min(end, pbstart)
	if newplacement is not None and newstart != newend:
		end  = min(end, newstart)
	ret = leaderboard[:end] + ret
	if not after:
		after = len(ret)
	if len(ret) < max_len:
		afterend = after + max_len-len(ret)
		ret += leaderboard[after:afterend]
	info(ToHex(playthrough_id), pbstart, pbend, newstart, newend, end, after, afterend, len(ret))
	return ret


def NonGroupedLeaderboard(cursor, event, playthrough_id, max_len=15):
	# TODO: focus on current player spot
	leaderboard = []
	place = 1
	for (d) in cursor:
		name = unrealscript_sanitize(d['name'])
		if 'end_date' in d:
			name += ' (' + str(d['end_date']) + ')'
		leaderboard.append({ **d, 'name': name, 'place': place })
		place += 1
	return leaderboard[:max_len]


def QueryLeaderboardGame(cursor, event, playthrough_id):
	if event.get('GameModeName') == 'Speedrun Mode':
		_QueryLeaderboard(cursor, SortBy='totaltime', version=VersionToInt(2,6,0,0),
			Filters={ 'GameMode': event.get('GameMode'), 'difficulty': event.get('difficulty') }
		)
		leaderboard = NonGroupedLeaderboard(cursor, event, playthrough_id)
	else:
		_QueryLeaderboard(cursor)
		leaderboard = GroupLeaderboard(cursor, event, playthrough_id)

	ret = {}
	for i in range(min(15,len(leaderboard))):
		d = leaderboard[i]
		arr = [ d['name'], d['score'], d['totaltime'], d['seed'], d['flagshash'], d['setseed'], d['place'], ToHex(d['playthrough_id']) ]
		ret['leaderboard-'+str(i)] = arr
	return ret


def GetLeaderboardPlacement(cursor, event, playthrough_id):
	_QueryLeaderboard(cursor)
	leaderboard = GroupLeaderboard(cursor, event, playthrough_id)
	_GetLeaderboardPlacement(leaderboard, playthrough_id)


def _GetLeaderboardPlacement(leaderboard, playthrough_id):
	prev_placement = 1
	for run in leaderboard:
		if run['playthrough_id'] == playthrough_id:
			if run['place'] != '--':
				return run['place']
			else:
				return prev_placement + 1
		
		if run['place'] != '--':
			prev_placement = run['place']
	return None


def try_exec(cursor, query):
	try:
		cursor.execute(query)
	except mysql.connector.Error as e:
		if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
			print("table already exists.")
		else:
			logex(e)
		return ()
	except Exception as e:
		logex(e)
		return ()
	return cursor

from dxlog.base import *

# for k in [0: 'num', 1: 'name', 2: 'killer', 3: 'damagetype', 4: 'age', 5: 'x', 6: 'y', 7: 'z', 8: 'killerclass']:
def compare_deaths(a, b):
	# name
	if a[1] != b[1]:
		return False

	# age, difference of 1 hour
	if abs(a[4] - b[4]) > 3600:
		return False
	
	# x, y, z, checking for > 100 feet
	dist = math.sqrt((a[5] - b[5]) ** 2 + (a[6] - b[6]) ** 2 + (a[7] - b[7]) ** 2)
	if dist > 16*100:
		return False
	
	return True

def filter_deaths(deaths):
	if not deaths:
		return deaths

	load_profanity_filter()
	
	for d in deaths.values():
		d[0] = int(d[0])
		d[1] = profanity.censor(d[1])
		d[2] = profanity.censor(d[2])
		d[3] = profanity.censor(d[3])
		d[4] = int(d[4])
		d[5] = float(d[5])
		d[6] = float(d[6])
		d[7] = float(d[7])
		d[8] = profanity.censor(d[8])
	
	keys = sorted(deaths.keys(), key=lambda d: deaths[d][4])
	end = len(keys)
	
	i = 0
	while i < end:
		j = i + 1
		bads = 0
		while j < end:
			if compare_deaths(deaths[keys[i]], deaths[keys[j]]):
				bads += 1
				if bads > 3:
					deaths[keys[i]][0] += 1
					del keys[j]
					end -= 1
					j -= 1
			j += 1
		i += 1
	
	newdeaths = {}
	for k in keys[:50]:
		newdeaths[k] = deaths[k]
	return newdeaths


def select_deaths(cursor, mod, map):
	if not map:
		map = "01_nyc_unatcoisland"
	ret = {}
	# we select more than we return because we might combine some, or choose some more spread out ones instead of just going by age?
	modcondition = ""
	if mod == "RevRandomizer":
		modcondition = " AND modname = \"RevRandomizer\" "
	else:
		modcondition = " AND NOT modname <=> \"RevRandomizer\" "

	# select more than we want, because filter_deaths will remove the excess
	cursor.execute("SELECT "
		+ "deaths.id as deathid, modname, ip, name, killer, killerclass, damagetype, x, y, z, UNIX_TIMESTAMP()-UNIX_TIMESTAMP(created) as age "
		+ "FROM deaths JOIN logs on(deaths.log_id=logs.id) "
		+ "WHERE map=%s "
		+ modcondition
		+ " ORDER BY created DESC LIMIT 100", (map,))
	
	for (d) in cursor:
		# need to sanitize these because unrealscript's json parsing isn't perfect
		key = 'deaths.' + str(d['deathid']) #d['x']+','+d['y']+','+d['z']
		d.pop('ip', None)
		d['num'] = 1
		ret[key] = []
		for k in ['num', 'name', 'killer', 'damagetype', 'age', 'x', 'y', 'z', 'killerclass']:
			s = unrealscript_sanitize(d[k])
			if not s:
				s = ''
			ret[key].append(s)
	
	return filter_deaths(ret)

		
def log_death(cursor, log_id, death):
	info(repr(death))
	location = location_split.split(death['location'])
	if 'victim' not in death:
		death['victim'] = death['player']
	cursor.execute("INSERT INTO deaths SET log_id=%s, name=%s, killer=%s, killerclass=%s, damagetype=%s, x=%s, y=%s, z=%s",
		(log_id, death['victim'], death.get('killer'), death.get('killerclass'), death.get('dmgtype'), location[0], location[1], location[2]))

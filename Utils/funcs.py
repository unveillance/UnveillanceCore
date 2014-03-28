import os, sys, signal, json
from subprocess import Popen, PIPE
from hashlib import md5

def passesParameterFilter(param_string):
	# TODO
	return True

def parseQueryString(query_string):
	# if query string is already json, return that
	try:
		if passesParameterFilter(query_string):
			return json.loads(query_string)
		else: return None
	except ValueError as e: pass
	
	# otherwise...
	params = dict()
	for kvp in [w for w in query_string.split("&") if w != ""]:
		kvp = kvp.split("=")
		k = kvp[0]
		v = kvp[1]
		
		if not passesParameterFilter(k) or not passesParameterFilter(v):
			return None
		
		params[k] = asTrueValue(v)
	
	return params

def hashEntireFile(path_to_file):
	try:
		m = md5()
		with open(path_to_file, 'rb') as f:
			for chunk in iter(lambda: f.read(4096), b''):
				m.update(chunk)
		return m.hexdigest()
	
	except: pass
	return None

def startDaemon(log_file, pid_file):
	print "DAEMONIZING PROCESS>>>"
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except OSError, e:
		print e.errno
		sys.exit(1)
		
	os.chdir("/")
	os.setsid()
	os.umask(0)
	
	try:
		pid = os.fork()
		if pid > 0:
			f = open(pid_file, 'w')
			f.write(str(pid))
			f.close()
			
			sys.exit(0)
	except OSError, e:
		print e.errno
		sys.exit(1)
	
	si = file('/dev/null', 'r')
	so = file(log_file, 'a+')
	se = file(log_file, 'a+', 0)
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())

	print ">>> PROCESS DAEMONIZED"

def stopDaemon(pid_file, extra_pids_port=None):
	pid = False
	try:
		f = open(pid_file, 'r')
		try:
			pid = int(f.read().strip())
		except ValueError as e:
			print "NO PID AT %s" % pid_file
	except IOError as e:
		print "NO PID AT %s" % pid_file
	
	if pid:
		print "STOPPING DAEMON on pid %d" % pid
		try:
			os.kill(pid, signal.SIGTERM)
			
			if extra_pids_port is not None:
				pids = Popen(['lsof', '-t', '-i:%d' % extra_pids_port], stdout=PIPE)
				pid = pids.stdout.read().strip()
				pids.stdout.close()
				
				for p in pid.split("\n"):
					cmd = ['kill', str(p)]
					Popen(cmd)
			
			return True
		except OSError as e:
			print "could not kill process at PID %d" % pid

	return False

def generateNonce(bottom_range=21, top_range=46):
	import string, random, time
	orderings = [
			string.ascii_uppercase, 
			string.digits, 
			string.ascii_lowercase, 
			string.digits, 
			string.ascii_uppercase,
			'*@~._!$%',
			str(time.time())
	]
	
	random.shuffle(orderings)
	choices = ''.join(orderings)
	numChars = random.choice(range(bottom_range,top_range))
	
	return ''.join(random.choice(choices) for x in range(numChars))

def generateMD5Hash(content=None, salt=None):
	if content is None:
		content = generateNonce()
	
	m = md5()
	m.update(str(content))
	if salt is not None: m.update(str(salt))
	return m.hexdigest()
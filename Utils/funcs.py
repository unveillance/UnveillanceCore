import os, sys, signal
from hashlib import md5

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

def stopDaemon(pid_file):
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
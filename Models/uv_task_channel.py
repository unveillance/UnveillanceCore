import httplib, socket, random, string

from threading import Thread
from time import sleep

from conf import DEBUG

class UnveillanceTaskChannel(Thread):
	def __init__(self, task_id, host, port):
		self.host = host
		self.port = port
		self.task_id = task_id

		self._session = str(random.randint(0, 1000))
		self._id = ''.join(random.choice(string.ascii_lowercase + string.digits) for c in range(8))

		Thread.__init__(self)
		self.get_socket_info()

	def get_socket_info(self):
		con = 0
		
		try:
			con = httplib.HTTPConnection(self.host, self.port)
			con.request('GET', '/%s/info' % self.task_id)
			r = con.getresponse()

			if DEBUG:
				print "GETTING INFO FIRST:"
				print r.status, r.reason, r.read()

			self.start()

		finally:
			if not con: con.close()

	def die(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()	

	def run(self):
		url = "/%s" % '/'.join([self.task_id, self._session, self._id, "xhr_streaming"])
		if DEBUG:
			print "TRYING URL %s" % url

		con = httplib.HTTPConnection(self.host, self.port)
		con.request('POST', url)

		r = con.getresponse()
		self.sock = socket.fromfd(r.fileno(), socket.AF_INET, socket.SOCK_STREAM)
		
		data = 1
		while data:
			data = self.sock.recv(1)
			if data == 'o':
				if DEBUG: print "CONNECTION!"
				pass

			if data == 'c':
				if DEBUG: print "DISCONNECTION"

			if data in ('m', 'a'):
				msg = self.sock.recv(1000)

				if DEBUG: 
					print "MESSAGE!"
					print msg

		sleep(0)
		if DEBUG: print "Channel to task %s closed." % self.task_id
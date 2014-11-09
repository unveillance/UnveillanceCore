import httplib, socket, random, string

import threading
from time import sleep

from conf import DEBUG

class UnveillanceTaskChannel(threading.Thread):
	def __init__(self, chan, host, port, use_ssl=None, auto_start=True):
		self.host = host
		self.port = port
		self.chan = chan

		if use_ssl is None:
			self.use_ssl = True if self.port == 443 else False
		elif type(use_ssl) is bool:
			self.use_ssl = use_ssl
		else:
			self.use_ssl = False


		self._session = str(random.randint(0, 1000))
		self._id = ''.join(random.choice(string.ascii_lowercase + string.digits) for c in range(8))

		super(UnveillanceTaskChannel, self).__init__()

		print self.host, self.port, self.chan, self.use_ssl

		if auto_start:
			self.get_socket_info()

	def get_socket_info(self):
		con = 0
		
		try:
			if self.use_ssl:
				con = httplib.HTTPSConnection(self.host, self.port)
			else:
				con = httplib.HTTPConnection(self.host, self.port)

			con.request('GET', '/%s/info' % self.chan)
			r = con.getresponse()

			if DEBUG:
				print "GETTING INFO FIRST:"
				print r.status, r.reason, r.read()

			self.start()

		finally:
			if not con:
				print "NO CON!"
				con.close()

	def route_annex_channel_message(self, message):
		pass

	def die(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def run(self):
		url = "/%s" % '/'.join([self.chan, self._session, self._id, "xhr_streaming"])
		if DEBUG:
			print "TRYING URL %s" % url

		if self.use_ssl:
			con = httplib.HTTPSConnection(self.host, self.port)
		else:
			con = httplib.HTTPConnection(self.host, self.port)
		
		con.request('POST', url)

		r = con.getresponse()
		self.sock = socket.fromfd(r.fileno(), socket.AF_INET, socket.SOCK_STREAM)
		
		data = 1
		while data:
			data = self.sock.recv(1)
			if data == 'o':
				#if DEBUG: print "CONNECTION!"
				pass

			if data == 'c':
				#if DEBUG: print "DISCONNECTION"
				pass

			if data in ('m', 'a'):
				msg = self.sock.recv(1000)
				self.route_annex_channel_message(msg)

		sleep(0)
		if DEBUG: print "Channel to task %s closed." % self.chan
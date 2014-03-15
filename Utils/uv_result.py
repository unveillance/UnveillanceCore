class Result(object):
	def __init__(self):
		self.result = 404

	def emit(self): return self.__dict__
from collections import namedtuple

EmitSentinel = namedtuple("EmitSentinel", "attr type s_replace")
AnnexDescriptor = namedtuple("AnnexDescriptor", "farm p22 p8888")

class Result(object):
	def __init__(self):
		self.result = 404

	def emit(self): return self.__dict__
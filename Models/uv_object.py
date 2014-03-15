__metaclass__ = type

import os, json
from collections import namedtuple
from copy import deepcopy

EmitSentinel = namedtuple("EmitSentinel", "attr type s_replace")

EMIT_SENTINELS = [
		EmitSentinel("emit_sentinels", "EmitSentinel", None)]

class UnveillanceObject(object):
	def __init__(self):
		self.emit_sentinels = deepcopy(EMIT_SENTINELS)
	
	def emit(self, remove=None):
		emit_ = deepcopy(self.__dict__)
		for e in [e for e in self.emit_sentinels if hasattr(self, e.attr)]:				
			if e.s_replace is None:
				del emit_[e.attr]
			else:
				rep = getattr(self, e.attr)				
				if type(rep) is list:
					emit_[e.attr] = [getattr(r, e.s_replace) for r in rep]
				else:
					emit_[e.attr] = getattr(rep, e.s_replace)
		
		if remove is not None:
			if type(remove) is not list:
				remove = [remove]
			
			for r in remove: del emit_[r]

		return emit_
	
	def inflate(self, attrs):
		print attrs
		for k,v in attrs.iteritems():
			setattr(self, k, v)
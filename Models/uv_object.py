__metaclass__ = type

import os, json
from collections import namedtuple
from copy import deepcopy

from conf import ANNEX_DIR
EmitSentinel = namedtuple("EmitSentinel", "attr type s_replace")

EMIT_SENTINELS = [
		EmitSentinel("emit_sentinels", "EmitSentinel", None)]

class UnveillanceObject(object):
	def __init__(self, emit_sentinels=None, _id=None, inflate=None):
		self.emit_sentinels = deepcopy(EMIT_SENTINELS)
		
		if emit_sentinels is not None:
			if type(emit_sentinels) is not list:
				emit_sentinels = [emit_sentinels]
			
		if inflate is not None: 
			try: self._id = inflate['_id']
			except KeyError as e:
				print e
				return
			
			base_path = os.path.join(".data", inflate['_id'])
			if not os.path.exists(os.path.join(ANNEX_DIR, base_path)):
				os.makedirs(os.path.join(ANNEX_DIR, base_path))
			
			inflate['base_path'] = base_path
			inflate['manifest'] = os.path.join(base_path, "manifest.json")
			
			self.emit_sentinels.extend(emit_sentinels)
			self.inflate(inflate)
		
		elif _id is not None:
			print "have to look up thing somehow..."
	
	def addAsset(self, data, file_name, asset_path, as_literal=True, **metadata):
		if data is not None:
			if not as_literal: data = dumps(data)
			
			try:
				with open(asset_path, 'wb+') as file: file.write(data)
			except Exception as e:
				print e
				return False
		
		asset = { 'file_name' : file_name }
		for k,v in metadata.iteritems():
			asset[k] = v
			if DEBUG: print "metadata added: %s = %s" % (k, v)
			
		if not hasattr(self, "assets"): self.assets = []
		
		entry = [e for e in self.assets if e['file_name'] == asset['file_name']]
		if len(entry) == 1: entry[0].update(asset)
		else: self.assets.append(asset)
		
		self.save()
		return asset_path
	
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
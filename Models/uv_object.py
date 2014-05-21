__metaclass__ = type

import os, json
from collections import namedtuple
from copy import deepcopy
from time import time

from conf import DEBUG
from vars import EmitSentinel, ALLOWED_DATA_ROOTS

EMIT_SENTINELS = [
		EmitSentinel("emit_sentinels", "EmitSentinel", None)]

class UnveillanceObject(object):
	def __init__(self, emit_sentinels=None, _id=None, inflate=None):
		from conf import ANNEX_DIR
		self.emit_sentinels = deepcopy(EMIT_SENTINELS)
		
		if emit_sentinels is not None:
			if type(emit_sentinels) is not list:
				emit_sentinels = [emit_sentinels]
			
			self.emit_sentinels.extend(emit_sentinels)
			
		if inflate is not None: 
			try: self._id = inflate['_id']
			except KeyError as e:
				print e
				return
			
			if self._id is None: 
				if DEBUG: print "why is Id none???"
				return
			
			#.data
			relative_root = ALLOWED_DATA_ROOTS[0]
			if "relative_root" in inflate.keys():
				relative_root = inflate['relative_root']
				del inflate['relative_root']
				
			if relative_root not in ALLOWED_DATA_ROOTS:
				if DEBUG: print "OH HELLLLL NO!"
				return
			
			base_path = os.path.join(relative_root, inflate['_id'])
			if not os.path.exists(os.path.join(ANNEX_DIR, base_path)):
				os.makedirs(os.path.join(ANNEX_DIR, base_path))
			
			inflate['base_path'] = base_path
			inflate['date_added'] = time() * 1000
			
			self.inflate(inflate)
			self.save()
		
		elif _id is not None: self.getObject(_id)
		print "HIIIIIIII %s" % _id
	
	def addAsset(self, file_name, asset_path, as_literal=True, **metadata):		
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
	
	def loadAsset(self, file_name):
		asset_path = self.getAsset(file_name, return_only="path")
		print "LOADING ASSET FROM PATH: %s" % asset_path
		
		if asset_path is not None:
			try:
				with open(asset_path, 'rb') as f: return f.read()
			except Exception as e: print e
		
		return None
	
	def getAsset(self, file_name, return_only=None):
		if not hasattr(self, "assets"): return None
		
		assets = [a for a in self.assets if a['file_name'] == file_name]
		if len(assets) == 1:
			asset_path = os.path.join(ANNEX_DIR, self.base_path, file_name)
			if return_only is not None:
				if return_only == "path":
					return asset_path
				elif return_only == "entry":
					return asset[0]
			else:
				return (asset[0], asset_path)
		
		return None
	
	def getAssetsByTagName(self, tag):
		if not hasattr(self, 'assets'): return None
		
		assets = [a for a in self.assets if "tags" in a and tag in a['tags']]
		
		if len(assets) == 0: return None
		return assets
	
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
	
	def invalidate(self, error=None):
		self.invalid = True
		if error is not None:
			if not hasattr(self, "errors"): self.errors = []
			self.errors.append(error)
	
	def inflate(self, attrs):
		print attrs
		for k,v in attrs.iteritems():
			setattr(self, k, v)
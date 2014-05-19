import json, os
from importlib import import_module
from multiprocessing import Process
from crontab import CronTab

from uv_object import UnveillanceObject
from lib.Frontend.lib.Core.Utils.funcs import generateMD5Hash

from conf import DEBUG, API_PORT, ANNEX_DIR
from vars import TASKS_ROOT, EmitSentinel

class UnveillanceSyncTask(UnveillanceObject):
	def __init__(self, inflate=None, _id=None):
		if DEBUG: print "sync task init"
		
		if inflate is not None:
			if "frequency" not in inflate.keys() and "duration" not in inflate.keys():
				self.invalid = True
				return

			try:
				inflate['task_path'] = ".".join([TASKS_ROOT, inflate['task_path']])
			except KeyError as e:
				if DEBUG: print e
				self.invalid = True
				return
		
			p, f = inflate['task_path'].rsplit(".", 1)
		
			try:
				module = import_module(p)
				func = getattr(module, f)				
			except Exception as e:
				if DEBUG: print e
				pass
			
			if func is None:
				self.invalid = True
				return
			
			if "args" not in inflate.keys():
				inflate['args'] = {}
							
			cmd_id = generateMD5Hash(content=json.dumps(inflate['args']),
				salt=inflate['task_path'])
			
			cmd = [
				"curl", "-X", "POST", "localhost:%d/run_synctask/" % API_PORT,
				"-H", "\"Content-Type: application/json\"", 
				"-d", "\'%s\'" % json.dumps({'_id' : cmd_id })
			]
			
			inflate.update({
				'_id' : cmd_id,
				'command' :  "".join(cmd),
				'is_running' : False,
				'relative_root' : ".synctasks/local"
			})
			
			if DEBUG: print inflate

		super(UnveillanceSyncTask, self).__init__(inflate=inflate, _id=_id,
			emit_sentinels=[EmitSentinel("cron", CronTab, None)])

	def save(self):
		manifest_path = os.path.join(ANNEX_DIR, ".synctasks/local", self._id, "manifest")
		with open(manifest_path, 'wb+') as manifest:
			manifest.write(json.dumps(self.emit()))
		
		self.start(restart=True)
		self.run()
	
	def getObject(self, _id):
		# get from synctasks folder
		try:
			manifest_path = os.path.join(ANNEX_DIR, ".synctasks/local", _id, "manifest")
			with open(manifest_path, 'rb') as manifest:
				self.inflate(json.loads(manifest.read()))
				self.run()

		except Exception as e:
			if DEBUG: print "ERROR GETTING OBJECT: %s" % e
			self.invalidate(error="ERROR GETTING OBJECT: %s" % e)
			
	def run(self):
		if DEBUG: print "RUNNING A TASK!!!\n%s" % self.emit()
		
		try:
			p, f = self.task_path.rsplit(".", 1)
			module = import_module(p)
			func = getattr(module, f)				
		except Exception as e:
			if DEBUG: print e
			pass
		
		if func is None:
			self.invalidate(error="NO FUNC!")
			return
		
		p = Process(target=func, args=[self.args])
		p.start()
		
	def start(self, restart=False):
		if DEBUG: print "RUNNING CRON %s" % self._id
		
		# if it's running, chill (or not!)
		cron_job = self.locateCronJob(init=True)
		if cron_job is not None:
			if not cron_job.is_enabled() or restart:
				cron_job.enable(False)
				cron_job.enable()
		try:
			return cron_job.is_enabled()
		except Exception as e:
			if DEBUG: print e
			
		return False
	
	def stop(self):
		if DEBUG: print "STOPPING CRON %s" % self._id
		
		cron_job = self.locateCronJob()
		if cron_job is not None:
			cron_job.enable(False)
		
		try:
			return cron_job.is_enabled()
		except Exception as e:
			if DEBUG: print e
		
		return False
		
	def setupCronJob(self):
		# TODO: THIS IS NOT PLATFORM-AGNOSTIC
		self.cron = CronTab(user=True)
		cron_job = cron.new(command=self.command, comment=self._id)
		
		if self.frequency == "m": cron_job.minute.every(self.duration)
		elif self.frequency == "h": cron_job.hour.every(self.duration)
		elif self.frequency == "d": cron_job.day.every(self.duration)
		
		return cron_job
	
	def locateCronJob(self, init=False):
		try:
			return self.cron.find_comment(self._id)[0]
		except Exception as e: 
			print e
			if init: return self.setupCronJob()
			
		return None
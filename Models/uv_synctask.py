from crontab import CrontTab
from uv_object import UnveillanceObject

class UnveillanceSyncTask(object):
	def __init__(self):
		print "sync task init"
	
		if inflate is not None:
			inflate['is_running'] = False
		
	def setupCronJob(self):
		# TODO: THIS IS NOT PLATFORM-AGNOSTIC
		cron = CronTab(user=True)
		cron_job = cron.new(command=self.command, comment=self._id)
		
		if self.frequency == "m": cron_job.minute.every(self.duration)
		elif self.frequency == "h": cron_job.hour.every(self.duration)
		elif self.frequency == "d": cron_job.day.every(self.duration)
		
		return cron_job
	
	def start(self):
		self.cron_job = self.locateCronJob(init=True)
		if self.cron_job is not None:
			if not self.cron_job.is_valid(): return False
			if self.cron_job.is_enabled(): return False
			
			self.cron_job.enable()			
			self.save()
			
			return self.cron_job.is_enabled()
		
		return False
		
	def stop(self):
		if hasattr(self, 'cron_job') and self.cron_job is not None:
			if not self.cron_job.is_valid(): return False
			if not self.cron_job.is_enabled(): return False
			
			self.cron_job.enable(False)
			self.save()
			
			return not self.cron_job.is_enabled()
			
		return False
	
	def locateCronJob(self, init=False):
		try:
			return cron.find_comment(self._id)][0]
		except Exception as e: 
			print e
			if init: return setupCronJob()
			
		return None
		
	def save(self):
		#	MAYBE is_enabled doesn't mean what i think it does?
		if hasattr(self, 'cron_job') and self.cron_job is not None:
			self.is_running = self.cron_job.is_enabled()
from crontab import CrontTab

class UnveillanceSyncTask(object):
	def __init__(self):
		print "sync task init"		
		
	def setupCronJob(self):
		# TODO: THIS IS NOT PLATFORM-AGNOSTIC
		self.cron = CronTab(user=True)
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
			return self.cron_job.is_enabled()
		
		return False
		
	def stop(self):
		if hasattr(self, 'cron_job') and self.cron_job is not None:
			if not self.cron_job.is_valid(): return False
			if not self.cron_job.is_enabled(): return False
			
			self.cron_job.enable(False)			
			return not self.cron_job.is_enabled()
			
		return False
	
	def locateCronJob(self, init=False):
		try:
			return self.cron.find_comment(self._id)][0]
		except Exception as e: 
			print e
			if init: return self.setupCronJob()
			
		return None
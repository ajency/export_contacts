import os,sys,time,csv,datetime,platform

class Handler():
	"""docstring for Handler"""
	def __init__(self, driver, logger):
		super(Handler, self).__init__()
		self.driver = driver
		self.logger = logger

	def success(self, message):
		self.logger.log(message,{
	      'url': self.driver.current_url,
	      'type': 'Completed',
	      'data': "\n Page Source: \n"+self.driver.page_source+"\n"
	    })
		# self.logger.info(message)
		# self.logger.file_log(message, url=self.driver.current_url, type='Completed')
		pass

	def in_progress(self, message):
		self.logger.log(message,{
	      'url': self.driver.current_url,
	      'type': 'Processing',
	      'data': ""
	    })
		# self.logger.info(message)
		# self.logger.file_log(message, url=self.driver.current_url, type='Processing')
		pass

	def exception(self, message):
		self.logger.log(message,{
	      'url': self.driver.current_url,
	      'type': 'Exception',
	      'data': "\n Page Source: \n"+self.driver.page_source+"\n"
	    })
		# self.logger.error(message)
		# self.logger.file_log("\n Exception: "+message+"\n Page Source: \n"+self.driver.page_source+"\n", url=self.driver.current_url, type='Exception')
		pass

	def warning(self, message):
		self.logger.log(message,{
	      'url': self.driver.current_url,
	      'type': 'Warning',
	      'data': "\n Page Source: \n"+self.driver.page_source+"\n"
	    })
		# self.logger.warning(message)
		# self.logger.file_log(message+"\n", url=self.driver.current_url, type='Warning')
		pass

	def retry_process(self):
		pass

	def continue_process(self):
		pass
	
	def exit_process(self, message=''):
		if not message:
			message = "Exit script execution"
		self.logger.log(message,{
	      'url': self.driver.current_url,
	      'type': 'Exit Script',
	      'data': ""
	    })
		# self.logger.error(message)
		# self.logger.file_log(message, url=self.driver.current_url, type='Exit Script')
		self.driver.close()
		sys.exit()
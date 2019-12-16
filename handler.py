import os,sys,time,csv,datetime,platform

class Handler():
	"""docstring for Handler"""
	def __init__(self, driver, logger, socketio, screenshot):
		super(Handler, self).__init__()
		self.driver = driver
		self.logger = logger
		self.socketio = socketio
		self.screenshot = screenshot

	def success(self, message, current_url='', page_source=''):
		if not current_url:
			current_url = self.driver.current_url
		if not page_source:
			page_source = self.driver.page_source
		self.socketio.emit('action', str(message))
		self.screenshot.capture(message.replace(' ', '_'))
		self.logger.info(str(message))
		# self.logger.file_log(str(message), url=self.driver.current_url, type='Completed')
		self.logger.log(str(message),{
	      'url': self.driver.current_url,
	      'type': 'Completed',
	      'data': "\n Page Source: \n"+self.driver.page_source+"\n"
	    })
		pass

	def in_progress(self, message):
		self.socketio.emit('action', str(message))
		self.screenshot.capture(message.replace(' ', '_'))
		self.logger.info(str(message))
		# self.logger.file_log(str(message), url=self.driver.current_url, type='Processing')
		self.logger.log(str(message),{
	      'url': self.driver.current_url,
	      'type': 'Processing',
	      'data': ""
	    })
		pass

	def exception(self, message, current_url='', page_source=''):
		if not current_url:
			current_url = self.driver.current_url
		if not page_source:
			page_source = self.driver.page_source
		self.socketio.emit('action', str(message))
		self.screenshot.capture(message.replace(' ', '_'))
		self.logger.error(str(message))
		# self.logger.file_log("\n Exception: "+str(message)+"\n Page Source: \n"+self.driver.page_source+"\n", url=self.driver.current_url, type='Exception')
		self.logger.log(str(message),{
	      'url': current_url,
	      'type': 'Exception',
	      'data': "\n Page Source: \n"+page_source+"\n"
	    })
		pass

	def warning(self, message, current_url='', page_source=''):
		if not current_url:
			current_url = self.driver.current_url
		if not page_source:
			page_source = self.driver.page_source
		self.socketio.emit('action', str(message))
		self.screenshot.capture(message.replace(' ', '_'))
		self.logger.warning(str(message))
		# self.logger.file_log(str(message)+"\n", url=self.driver.current_url, type='Warning')
		self.logger.log(str(message),{
	      'url': self.driver.current_url,
	      'type': 'Warning',
	      'data': ""
	    })
		pass

	def retry_process(self):
		pass

	def continue_process(self):
		pass
	
	def exit_process(self, message='', current_url='', page_source='', stop_execution=False):
		if not message:
			exit_message = "Exit script execution"
		self.socketio.emit('action', str(exit_message))
		self.screenshot.capture(exit_message.replace(' ', '_'))
		self.logger.error(str(exit_message))
		# self.logger.file_log(str(exit_message), url=self.driver.current_url, type='Exit Script')
		self.logger.log(str(exit_message),{
	      'url': self.driver.current_url,
	      'type': 'Exit Script',
	      'data': ""
	    })
		if stop_execution:
			self.driver.quit()
			sys.exit()

	def _log_(self, message, data=''):
		self.socketio.emit('action', str(message))
		self.logger.info(str(message))
		# self.logger.file_log(str(message), url=self.driver.current_url, type='Processing')
		self.logger.log(str(message),{
	      'url': '',
	      'type': 'LOG',
	      'data': data
	    })
		pass
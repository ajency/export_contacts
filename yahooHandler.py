import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class YahooHandler(base_handler):
	"""docstring for YahooHandler"""
	def __init__(self, driver, logger, socketio, screenshot, credentials):
		super(YahooHandler, self).__init__(driver, logger, socketio, screenshot)
		self.driver = driver
		self.logger = logger
		self.socketio = socketio
		self.yahoo_cred_index = 0
		self.credentials = credentials
		self.login_url = "https://login.yahoo.com/account/"
		self.logout_url = "https://login.yahoo.com/account/"
		self.check_login_url = "https://login.yahoo.com/account/"
		self.import_contacts_url = "https://www.linkedin.com/mynetwork/import-contacts/"



	def exception(self, message, current_url='', page_source=''):
		super(YahooHandler, self).exception(message, current_url, page_source)
		next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		if next_step.strip().lower() == "x":
			self.exit_process(message, current_url, page_source)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process()
		else:
			self.continue_process()
			return False


	def retry_process(self, retry_action, data=[]):
		use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
		if use_diff_cred.strip().lower() == 'y':
			self.yahoo_cred_index += 1

		if self.yahoo_cred_index < len(self.credentials):
			username = self.credentials[self.yahoo_cred_index]['username']
			password = self.credentials[self.yahoo_cred_index]['password']
			self.in_progress("Retrying using "+username)
			return True
		else:
			self.exit_process("No more Yahoo accounts available")
			return False


	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		is_loggedin = False
		try:
			# check if login was successful
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			self.driver.execute_script("arguments[0].click();", clk)
			# Logout
			logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a[2]')))
			# self.driver.find_element_by_id('login-username')
			is_loggedin = True
		except Exception as e:
			is_loggedin = False
			pass
		return is_loggedin


	# Normal page load - login 
	def normal_yahoo_login(self, username, password):
		self.in_progress("Logging into Yahoo as "+username)
		user = self.driver.find_element_by_id('login-username')
		user.clear()
		user.send_keys(username)
		self.driver.find_element_by_id("login-signin").click()
		try:
			error = self.driver.find_element_by_css_selector('#username-error')
			error_msg = error.text
		except Exception as e:
			error_msg = ''

		if error_msg:
			raise Exception(error_msg)

		# check for captcha
		self.not_a_robot_captcha()

		time.sleep(5)
		pwd = self.driver.find_element_by_id("login-passwd")
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = self.driver.find_element_by_id("login-signin")
		login.click()
		time.sleep(2)
		return True



	def not_a_robot_captcha(self):
		try:
			# Not a Robot
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
			self.driver.execute_script("arguments[0].click();", clk)
			time.sleep(5)
			self.driver.find_element_by_xpath('//*[@id="recaptcha-submit"]').click()
			self.success("Validated: Not a Robot", current_url, page_source)
		except Exception as e:
			pass

	# Normal page load - logout 
	def normal_yahoo_logout(self):
		self.in_progress("Logging out from Yahoo")
		# Logout
		self.driver.get("https://login.yahoo.com/account/")
		# Logout drop down
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
		self.driver.execute_script("arguments[0].click();", clk)
		# Logout
		logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a[3]')))
		logout.click()
		self.success("Logging out from Yahoo successful")
		return True



	# email verification
	def email_verification(self, username):
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		self.in_progress("Email verification")
		self.socketio.emit('exception_user_single_request', 'yahoo_email_verification_handler'+' --- '+"Please enter the verification code sent to "+username+" inbox: ")
		verify_email.clear()
		# self.pause_execution()
		# self.wait_until_continue_is_true()
		try:
			verification_entered = WebDriverWait(self.driver, 180).until(lambda driver: len(driver.find_element_by_css_selector("#input__email_verification_pin").get_attribute("value")) == 6)
			if verification_entered:
				confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
				self.driver.execute_script("arguments[0].click();", confirm)
				time.sleep(1)
			return True
		except Exception as e:
			return False

	def email_pin_verify(self, user_input):
		self.continue_with_execution()
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		verify_email.send_keys(user_input)
		pass


	# Recaptcha verification
	def recaptcha_verification(self, username):
		self.in_progress("Recaptcha verification")
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'playCaptchaButton')))
		super(YahooHandler, self).exception("Recaptcha verification", self.driver.current_url, self.driver.page_source)
		return False



	def check_login_status(self):
		username = self.credentials[self.yahoo_cred_index]['username']
		try:
			# check if login was successful
			self.driver.get(self.check_login_url)
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			self.driver.execute_script("arguments[0].click();", clk)
			time.sleep(1)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			loggedin_username = self.driver.find_element_by_css_selector('#ybarAccountMenuBody > ul > li > div > span._yb_j3lqv._yb_16hxw._yb_kyook._yb_1qtbr._yb_vig6z').text
		except Exception as e:
			loggedin_username = ''

			if self.is_user_logged_in():
				if loggedin_username:
					message = "Logged In into Yahoo as "+loggedin_username+" successfully"
				else:
					message = "Log In into yahoo successful"
				self.yahoo_cred_index += 1
				# message = "Logged In into Yahoo as "+username+" successfully"
				self.success(message)
				return True
			else:
				message = "Yahoo login for "+username+" failed"
				super(YahooHandler, self).exception(message, current_url, page_source)
				# self.exception(message, current_url, page_source)
				return False



	def normal_sync_yahoo_account(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember53"]/a')))
		self.driver.execute_script("arguments[0].click();", clk)
		# clk.click()
		time.sleep(3)
		if len(self.driver.window_handles) > 1:
			# switch the pop-up window
			self.driver.switch_to.window(self.driver.window_handles[1])
			self.in_progress("Syncing of yahoo account is in progress")
			time.sleep(5)
			# Check if any account needs to be selected
			confirmAccount = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'oauth2-agree')))
			self.driver.execute_script("arguments[0].click();", confirmAccount)
			#switch back to original window
			time.sleep(0.5)
			if len(self.driver.window_handles) > 1:
				try:
					backToPrevWindow = WebDriverWait(self.driver.window_handles[1], 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="minimal-util-nav"]/ul/li[1]/a')))
					backToPrevWindow.click()
				except Exception as e:
					if len(self.driver.window_handles) > 1:
						self.driver.close()
		self.driver.switch_to.window(self.driver.window_handles[0])
		try:
			time.sleep(3)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact-select-checkbox"]')))
			self.success('Imported contacts')
			return True
		except Exception as e:
			super(YahooHandler, self).exception('Unable to currently import contacts - '+str(e))
			return False

import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class YahooHandler(base_handler):
	"""docstring for YahooHandler"""
	def __init__(self, driver, logger, credentials):
		super(YahooHandler, self).__init__(driver, logger)
		self.driver = driver
		self.logger = logger
		self.yahoo_cred_index = 0
		self.credentials = credentials
		self.login_url = "https://login.yahoo.com/account/"
		self.logout_url = "https://login.yahoo.com/account/"
		self.check_login_url = "https://login.yahoo.com/account/"
		# self.sign_in_chooser_url = "http://accounts.google.com/ServiceLogin/signinchooser"


	def exception(self, message, retry_method, data=[]):
		super(YahooHandler, self).exception(message)
		next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		if next_step.strip().lower() == "x":
			self.exit_process(message)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process(retry_method, data)
		else:
			self.continue_process()
			return False


	def retry_process(self, retry_action, data=[]):
		if retry_action == 'login':
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
		else:
			self.exit_process("Unknown Yahoo Retry Method")
		return False


	# Normal page load - login 
	def normal_yahoo_login(self, username, password):
		self.in_progress("Logging into Yahoo as "+username)
		user = self.driver.find_element_by_id('login-username')
		user.clear()
		user.send_keys(username)
		self.driver.find_element_by_id("login-signin").click()
		time.sleep(5)
		pwd = self.driver.find_element_by_id("login-passwd")
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = self.driver.find_element_by_id("login-signin")
		login.click()
		time.sleep(2)


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



	# email verification
	def email_verification(self, username):
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		self.in_progress("Email verification")
		verify_email.clear()
		user_input = input("Please enter the verification code sent to "+username+" inbox: ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		self.driver.execute_script("arguments[0].click();", confirm)
		pass


	# Recaptcha verification
	def recaptcha_verification(self, username):
		self.in_progress("Recaptcha verification")
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'playCaptchaButton')))
		super(YahooHandler, self).exception("Recaptcha verification")
		pass



	def check_login_status(self):
		username = self.credentials[self.yahoo_cred_index]['username']
		try:
			# check if login was successful
			self.driver.get("https://login.yahoo.com/account/")
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			self.driver.execute_script("arguments[0].click();", clk)
			time.sleep(1)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))

			self.yahoo_cred_index += 1
			message = "Logged In into Yahoo as "+username+" successfully"
			self.success(message)
		except Exception as e:
			message = "Yahoo login for "+username+" failed"
			# super(YahooHandler, self.exception(message)
			self.exception(message, 'login', self.login_url)



	def normal_sync_yahoo_account(self):
		clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember53"]/a')))
		clk.click()
		time.sleep(3)
		if len(self.driver.window_handles) > 1:
			# switch the pop-up window
			self.driver.switch_to.window(self.driver.window_handles[1])
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
	except Exception as e:
		super(YahooHandler, self).exception('Unable to currently import contacts - '+str(e))

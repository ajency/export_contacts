import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class GmailHandler(base_handler):
	"""docstring for GmailHandler"""
	def __init__(self, driver, logger, credentials):
		super(GmailHandler, self).__init__(driver, logger)
		self.driver = driver
		self.logger = logger
		self.gmail_cred_index = 0
		self.credentials = credentials


	def exception(self, message, retry_method):
		next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		if next_step.strip().lower() == "x":
			self.exit_process(message)
			pass
		elif next_step.strip().lower() == "r":
			self.retry_process(retry_method)
			pass
		else:
			self.continue_process()
			pass

	def retry_process(self, retry_action, data):
		if retry_action == 'login':
			use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
			if use_diff_cred.strip().lower() == 'y':
				self.gmail_cred_index += 1
				pass
			if self.gmail_cred_index < len(self.credentials):
				username = self.credentials[self.gmail_cred_index]['username']
				password = self.credentials[self.gmail_cred_index]['password']
				self.in_progress("Retrying using "+username+" : ")
				self.login(data)
			else:
				self.exit_process("No more Gmail accounts available")
			pass
		else:
			self.exit_process("Unknown Gmail Retry Method")
		pass


	def login(self, action_url):
		if self.gmail_cred_index < len(self.credentials):
			self.driver.get(action_url)
			username = self.credentials[self.gmail_cred_index]['username']
			password = self.credentials[self.gmail_cred_index]['password']
			if search_element_by_id(self.driver, 'identifierId'):
				try:
					self.normal_gmail_login(username, password)
				except Exception as e:
					self.exception(e, 'login', action_url)
			else:
				message = "Unable to Identify Gmail Login Page"
				super(GmailHandler, self).exception(message)
				pass
		else:
			self.exit_process("No Gmail accounts available")


	# Normal page load - login 
	def normal_gmail_login(self, username, password):
		self.in_progress("Logging into Gmail as "+username)
		self.driver.get("https://accounts.google.com/signin/v2")
		self.driver.find_element_by_id('identifierId').send_keys(username)
		self.driver.find_element_by_id("identifierNext").click()
		time.sleep(5)
		pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = self.driver.find_element_by_id("passwordNext")
		login.click()


	def logout(self, action_url):
		try:
			self.normal_gmail_logout(action_url)
		except Exception as e:
			message = str(e)
			super(GmailHandler, self).exception(message)
			pass


	# Normal page load - logout 
	def normal_gmail_logout(self, action_url):
		self.in_progress("Logging out from Gmail")
		# Logout
		self.driver.get(action_url)
		self.remove_previous_loggedin_gmail_accounts()
		self.success("Logging out from Gmail successful")


	def verify_account(self):
		username = self.credentials[self.gmail_cred_index]['username']
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Gmail Email verification - Failed \n"+str(e)
				self.exception(message, 'login')
				# super(GmailHandler, self).exception(message)
			pass
		elif search_element_by_id(self.driver, "recaptcha-anchor"):
			try:
				self.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Gmail Recaptcha verification - Failed \n"+str(e)
				self.exception(message, 'login')
				# super(GmailHandler, self).exception(message)
			pass
		else:
			message = "Unable to identify Gmail account verification Page"
			# self.exception(message, 'login')
			super(GmailHandler, self).exception(message)
			pass


	# email verification
	def email_verification(self, username):
		verify_email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		self.in_progress("Email verification")
		verify_email.clear()
		user_input = input("Please enter the verification code sent to "+username+" inbox: ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		driver.execute_script("arguments[0].click();", confirm)
		pass


	# Recaptcha verification
	def recaptcha_verification(self, username):
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
		super(GmailHandler, self).exception("Recaptcha verification")
		pass



	def check_login_status(self):
		username = self.credentials[self.gmail_cred_index]['username']
		try:
			# check if login was successful
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			self.gmail_cred_index += 1
			message = "Gmail login for "+username+" was successful"
			self.success(message)
		except Exception as e:
			message = "Gmail login for "+username+" failed"
			# super(GmailHandler, self.exception(message)
			self.exception(message, 'login')



	def remove_previous_loggedin_gmail_accounts(self):
		self.driver.get("http://accounts.google.com/ServiceLogin/signinchooser")
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]')))
		removeAccounttClk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[3]')))
		removeAccounttClk.click()
		selectClk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/ul/li[1]')))
		selectClk.click()
		# //*[@id="yDmH0d"]/div[5]/div/div[2]/div[3]/div[1]
		removeClk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[5]/div/div[2]/div[3]/div[1]')))
		self.driver.execute_script("arguments[0].click();", removeClk)
		# removeClk.click()
		time.sleep(3)
		message = "Removed currently logged out account from browser"
		self.success(message)

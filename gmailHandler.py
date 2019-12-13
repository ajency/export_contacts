import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class GmailHandler(base_handler):
	"""docstring for GmailHandler"""
	def __init__(self, driver, logger, socketio, screenshot, credentials):
		super(GmailHandler, self).__init__(driver, logger, socketio, screenshot)
		self.driver = driver
		self.logger = logger
		self.socketio = socketio
		self.gmail_cred_index = 0
		self.credentials = credentials
		self.continue_execution = True
		self.login_url = "https://accounts.google.com/signin/v2"
		self.logout_url = "https://www.google.com/accounts/Logout"
		self.check_login_url = "https://accounts.google.com"
		self.sign_in_chooser_url = "http://accounts.google.com/ServiceLogin/signinchooser"
		self.import_contacts_url = "https://www.linkedin.com/mynetwork/import-contacts/"



	def exception(self, message, current_url='', page_source=''):
		super(LinkedInHandler, self).exception(message, current_url, page_source)
		# next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		# self.process_exception(next_step, message)
		self.socketio.emit('exception_user_single_request', 'gmail_exception_handler')
		self.pause_execution()
		self.wait_until_continue_is_true()

	def process_exception(self, next_step, message=''):
		self.continue_execution()
		if next_step.strip().lower() == "x":
			self.exit_process(message)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process()
		else:
			self.continue_process()
			return False

	def process_retry(self, use_diff_cred):
		self.continue_execution()
		if use_diff_cred.strip().lower() == 'y':
			self.linkedin_cred_index += 1

		if self.linkedin_cred_index < len(self.credentials):
			username = self.credentials[self.linkedin_cred_index]['username']
			password = self.credentials[self.linkedin_cred_index]['password']
			self.in_progress("Retrying using "+username)
			return True
		else:
			self.exit_process("No more LinkedIn accounts available")
			return False

	def retry_process(self):
		self.socketio.emit('exception_user_single_request', 'gmail_retry_handler')
		# use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
		# self.process_retry(use_diff_cred)
		self.pause_execution()
		self.wait_until_continue_is_true()


	# Normal page load - login 
	def normal_gmail_login(self, username, password):
		self.in_progress("Logging into Gmail as "+username)
		user = self.driver.find_element_by_id('identifierId')
		user.clear()
		user.send_keys(username)
		self.driver.find_element_by_id("identifierNext").click()
		time.sleep(5)
		pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = self.driver.find_element_by_id("passwordNext")
		login.click()



	# Normal page load - logout 
	def normal_gmail_logout(self):
		self.in_progress("Logging out from Gmail")
		# Logout
		self.driver.get(self.logout_url)
		self.remove_previous_loggedin_gmail_accounts()
		self.success("Logging out from Gmail successful")



	# email verification
	def email_verification(self, username):
		self.in_progress("Email verification")
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		super(GmailHandler, self).exception("Email verification")
		# verify_email.clear()
		# user_input = input("Please enter the verification code sent to "+username+" inbox: ")
		# verify_email.send_keys(user_input)
		# confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		# self.driver.execute_script("arguments[0].click();", confirm)
		pass


	def otp_verification(self, username):
		mobile_verificaiton_button = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
		if mobile_verificaiton_button:
			self.socketio.emit('action', 'Clicking on mobile verification link')
			mobile_verificaiton_button.click()
			self.socketio.emit('gmail_otp_verification', 'Enter the OTP: ')
			self.pause_execution()
			self.wait_until_continue_is_true()


	def gmail_otp_login(self, otp):
		self.continue_execution()
		otp_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
		otp_input.send_keys(otp)
		next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#idvPreregisteredPhoneNext")))
		next_btn.click()
		time.sleep(1)
		try:
			# check if login was successful
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			self.gmail_cred_index += 1
			message = "Successfully logged in to gmail after otp verification"
			# message = "Logged In into Gmail as "+username+" successfully"
			self.success(message)
		except Exception as e:
			message = "Unable to login to gmail..."
			# super(GmailHandler, self.exception(message)
			self.exception(message)


	# Recaptcha verification
	def recaptcha_verification(self, username):
		self.in_progress("Recaptcha verification")
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'playCaptchaButton')))
		super(GmailHandler, self).exception("Recaptcha verification")
		pass



	def check_login_status(self):
		username = self.credentials[self.gmail_cred_index]['username']
		try:
			# check if login was successful
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			self.gmail_cred_index += 1
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			clk.click()
			username = self.driver.find_element_by_css_selector('#gb > div.gb_Md.gb_3d.gb_Ud > div.gb_3a.gb_F.gb_l.gb_4a.gb_na > div.gb_cb > div.gb_eb > div.gb_qb').text
			name = self.driver.find_element_by_css_selector('#gb > div.gb_Md.gb_3d.gb_Ud > div.gb_3a.gb_F.gb_l.gb_4a.gb_na > div.gb_cb > div.gb_eb > div.gb_ob.gb_pb').text
			message = "Logged In into Gmail as "+username+' ('+name+") successfully"
			# message = "Logged In into Gmail as "+username+" successfully"
			self.success(message)
		except Exception as e:
			message = "Gmail login for "+username+" failed"
			# super(GmailHandler, self.exception(message)
			self.exception(message)



	def remove_previous_loggedin_gmail_accounts(self):
		self.driver.get(self.sign_in_chooser_url)
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
		message = "Removed Gmail logged out accounts from browser"
		self.success(message)


	def normal_sync_gmail_account(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember48"]/a')))
		clk.click()
		time.sleep(3)
		if len(self.driver.window_handles) > 1:
			# switch the pop-up window
			self.driver.switch_to.window(self.driver.window_handles[1])
			time.sleep(5)
			# Check if any account needs to be selected
			accountSelector = '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[1]'
			account = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, accountSelector)))
			account.click()
			confirmAccount = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'submit_approve_access')))
			# confirmAccount.click()
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
			super(GmailHandler, self).exception('Unable to currently import contacts - '+str(e))



	def pause_execution(self):
		# SET False to pause execution
		self.continue_execution = False

	def continue_execution(self):
		# SET True to continue execution
		self.continue_execution = True

	def wait_until_continue_is_true(self):
		# wait until self.continue_execution = True
		custom_wait_until_continue_is_true(self, 120)

	def custom_wait_until_continue_is_true(self, waiting_time):
		# wait until self.continue_execution = True OR custom waiting time as passed
		waiting_time = int(waiting_time)
		while not self.continue_execution or waiting_time > 0:
			time.sleep(0.98)
			waiting_time = waiting_time - 1
			custom_wait_until_continue_is_true(self, waiting_time)
			pass
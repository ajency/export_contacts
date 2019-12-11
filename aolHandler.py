import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class AOLHandler(base_handler):
	"""docstring for AOLHandler"""
	def __init__(self, driver, logger, credentials):
		super(AOLHandler, self).__init__(driver, logger)
		self.driver = driver
		self.logger = logger
		self.aol_cred_index = 0
		self.credentials = credentials
		self.login_url = "https://login.aol.com/account/personalinfo"
		self.logout_url = "https://login.aol.com/account/personalinfo"
		self.check_login_url = "https://login.aol.com/account/personalinfo"
		self.import_contacts_url = "https://www.linkedin.com/mynetwork/import-contacts/"


	def exception(self, message, current_url='', page_source=''):
		super(AOLHandler, self).exception(message, current_url, page_source)
		next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		if next_step.strip().lower() == "x":
			self.exit_process(message, current_url, page_source)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process(retry_method, data)
		else:
			self.continue_process()
			return False


	def retry_process(self):
		use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
		if use_diff_cred.strip().lower() == 'y':
			self.aol_cred_index += 1

		if self.aol_cred_index < len(self.credentials):
			username = self.credentials[self.aol_cred_index]['username']
			password = self.credentials[self.aol_cred_index]['password']
			self.in_progress("Retrying using "+username)
			return True
		else:
			super(AOLHandler, self).exception("No more AOL accounts available")
			# self.exit_process("No more AOL accounts available")
			return False


	# Normal page load - login 
	def normal_aol_login(self, username, password):
		self.in_progress("Logging into AOL as "+username)
		user = self.driver.find_element_by_id('login-username')
		user.clear()
		user.send_keys(username)
		self.driver.find_element_by_id("login-signin").click()
		time.sleep(3)
		
		# check for captcha
		self.not_a_robot_captcha()
		
		pwd = self.driver.find_element_by_id('login-passwd')
		pwd.send_keys(password)
		# form submit
		login = self.driver.find_element_by_id("login-signin")
		login.click()


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
	def normal_aol_logout(self):
		# Logout
		self.in_progress("Logging out from AOL")
		# Logout drop down
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
		self.driver.execute_script("arguments[0].click();", clk)
		# Logout
		logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a]')))
		self.driver.execute_script("arguments[0].click();", logout)
		self.success("Logging out from AOL successful")



	def check_login_status(self):
		username = self.credentials[self.aol_cred_index]['username']
		try:
			# check if login was successful
			self.driver.get(self.check_login_url)
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			self.driver.execute_script("arguments[0].click();", clk)
			time.sleep(1)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			loggedin_username = self.driver.find_element_by_css_selector('#ybarAccountMenuBody > ul > li > div > span._yb_152qm._yb_u6kgn._yb_7di8s._yb_fe66m._yb_b2fe8').text
			message = "Logged In into AOL as "+loggedin_username+" successfully"
			self.aol_cred_index += 1
			# message = "Logged In into AOL as "+username+" successfully"
			self.success(message)
		except Exception as e:
			message = "AOL login for "+username+" failed"
			# retry = self.exception(message, current_url, page_source)
			super(AOLHandler, self).exception(message, current_url, page_source)



	def normal_sync_aol_account(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember63"]/a')))
		clk.click()
		self.in_progress("Syncing of AOL account is in progress")
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
			super(AOLHandler, self).exception('Unable to currently import contacts - '+str(e))

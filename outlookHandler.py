import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class OutLookHandler(base_handler):
	"""docstring for OutLookHandler"""
	def __init__(self, driver, logger, credentials):
		super(OutLookHandler, self).__init__(driver, logger)
		self.driver = driver
		self.logger = logger
		self.outlook_cred_index = 0
		self.credentials = credentials
		self.login_url = "https://login.live.com/"
		self.logout_url = "https://account.microsoft.com/"
		self.check_login_url = "https://account.microsoft.com/"
		self.import_contacts_url = "https://www.linkedin.com/mynetwork/import-contacts/"


	def exception(self, message, current_url='', page_source=''):
		super(OutLookHandler, self).exception(message, current_url, page_source)
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
			self.outlook_cred_index += 1

		if self.outlook_cred_index < len(self.credentials):
			username = self.credentials[self.outlook_cred_index]['username']
			password = self.credentials[self.outlook_cred_index]['password']
			self.in_progress("Retrying using "+username)
			return True
		else:
			self.exit_process("No more OutLook accounts available")
			return False


	# Normal page load - login 
	def normal_outlook_login(self, username, password):
		self.in_progress("Logging into OutLook as "+username)
		user = self.driver.find_element_by_id('i0116')
		user.clear()
		user.send_keys(username)
		self.driver.find_element_by_id("idSIButton9").click()
		time.sleep(2)
		try:
			error_txt = self.driver.find_element_by_id("usernameError").text
			self.exception(error_txt)
		except Exception as e:
			self.in_progress("Logging In into OutLook as "+username)
			pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
			pwd.send_keys(password)
			# form submit
			# pwd.send_keys(Keys.RETURN)
			login = self.driver.find_element_by_id("idSIButton9")
			login.click()


	# Normal page load - logout 
	def normal_outlook_logout(self):
		# Logout
		clk = driver.find_element_by_id("mectrl_headerPicture")
		clk.click()
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mectrl_body_signOut')))
		self.in_progress("Logging out from OutLook")
		# logout = driver.find_element_by_id("mectrl_body_signOut")
		logout.click()
		self.success("Logging out from OutLook successful")



	def check_login_status(self):
		username = self.credentials[self.outlook_cred_index]['username']
		try:
			# check if login was successful
			self.driver.get(self.check_login_url)
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mectrl_headerPicture"]')))
			self.driver.execute_script("arguments[0].click();", clk)
			loggedin_username = self.driver.find_element_by_css_selector('#mectrl_currentAccount_secondary').text
			message = "Logged In into OutLook as "+loggedin_username+" successfully"
			self.outlook_cred_index += 1
			# message = "Logged In into OutLook as "+username+" successfully"
			self.success(message)
		except Exception as e:
			message = "OutLook login for "+username+" failed"
			# super(OutLookHandler, self.exception(message, current_url, page_source)
			self.exception(message, current_url, page_source)



	def normal_sync_outlook_account(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember53"]/a')))
		clk.click()
		self.in_progress("Syncing of OutLook account is in progress")
		time.sleep(3)
		if len(self.driver.window_handles) > 1:
			# switch the pop-up window
			self.driver.switch_to.window(self.driver.window_handles[1])
			time.sleep(5)
			# Check if any account needs to be selected
			confirmAccount = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'idBtn_Accept')))
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
			super(OutLookHandler, self).exception('Unable to currently import contacts - '+str(e))

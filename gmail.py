import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common_functions import *

class Gmail():
	"""docstring for Gmail"""
	def __init__(self, exporter):
		super(Gmail, self).__init__()
		self.gmail_cred_index = 0
		self.driver = exporter.driver
		self.exporter = exporter
		self.credentials = self.exporter.get_credentials('gmail')


	def perform_action(self, action, action_url=""):
		# Gmail - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.exporter.logger.info("Already Logged In to Gmail")
				self.exporter.logger.file_log("Already Logged In to Gmail", url=self.driver.current_url, type='')
			else:
				self.login(action_url)
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		# Gmail - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.exporter.logger.info("Need to Login before logging out from Gmail")
				self.exporter.logger.file_log("Need to Login before logging out from Gmail", url=self.driver.current_url, type='')
			else:
				self.logout(action_url)

	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		is_loggedin = False
		try:
			# check if login was successful
			self.driver.get("https://accounts.google.com/")
			self.driver.find_element_by_id('identifierId')
			is_loggedin = False
		except Exception as e:
			is_loggedin = True
			pass
		return is_loggedin


	def login(self, action_url):
		self.driver.get(action_url)
		if self.gmail_cred_index < len(self.credentials):
			username = self.credentials[self.gmail_cred_index]['username']
			password = self.credentials[self.gmail_cred_index]['password']
			
			if search_element_by_id(self.driver, 'identifierId'):
				try:
					self.normal_gmail_login(username, password)
				except Exception as e:
					message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
					self.exporter.logger.error(message)
					self.exporter.logger.file_log(message, self.driver.current_url, "Login Failed")
			else:
				# need to call handler
				pass
		else:
			print("no more gmail accounts")


	def logout(self, action_url):
		self.normal_gmail_logout(self, action_url)
		try:
			self.remove_previous_loggedin_gmail_accounts()
		except Exception as e:
			# log exception
			message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
			self.exporter.logger.error(message)
			self.exporter.logger.file_log(message, url=self.driver.current_url, type='Account Removal - Failed')
			pass


	def verify_account(self):
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
				self.exporter.logger.error(message)
				self.exporter.logger.file_log(message, url=self.driver.current_url, type='Email verify - Failed')
			pass
		elif search_element_by_id(self.driver, "recaptcha-anchor"):
			try:
				self.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
				self.exporter.logger.error(message)
				self.exporter.logger.file_log(message, url=self.driver.current_url, type='Recaptcha verify - Failed')
			pass
		else:
			# need to call handler
			self.exporter.logger.file_log("Page Source:\n"+str(self.driver.page_source)+"\n", url=self.driver.current_url, type='Verification Failure')
			pass



	# Normal page load - login 
	def normal_gmail_login(self, username, password):
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
		login.click()


	# Normal page load - logout 
	def normal_gmail_logout(self):
		self.exporter.logger.info("Logging out from Gmail")
		self.exporter.logger.file_log("Logging out from Gmail", url=self.driver.current_url, type='')
		# Logout
		self.driver.get(action_url)
		self.exporter.logger.info("Logging out from Gmail successful")
		self.exporter.logger.file_log("Logging out from Gmail successful", url=self.driver.current_url, type='')


	# email verification
	def email_verification(self):
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		print("Email verification required")
		verify_email.clear()
		user_input = input("Please enter the verification code sent via mail to "+username+": ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		self.driver.execute_script("arguments[0].click();", confirm)
		pass


	# Recaptcha verification
	def recaptcha_verification(self):
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
		print("Recaptcha verification required")
		pass


	def check_login_status(self):
		username = self.credentials[self.gmail_cred_index]['username']
		try:
			# check if login was successful
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			# self.gmail_cred_index += 1
			message = "Gmail login for "+username+" was successful"
			self.exporter.logger.info(message)
			self.exporter.logger.file_log(message, url=self.driver.current_url, type='Test - success')
		except Exception as e:
			message = "Gmail login for "+username+" failed"
			self.exporter.logger.error(message)
			self.exporter.logger.file_log(message, url=self.driver.current_url, type='Test - failed')



	# LogIn function for Gmail Account
	def login_to_gmail(self):
		self.perform_action("login", "https://accounts.google.com/signin/v2")
		self.perform_action("verify-account")
		self.perform_action("check-login", "https://accounts.google.com")


	# LogOut function for Gmail Account
	def logout_from_gmail(self):
		self.perform_action("logout", "https://www.google.com/accounts/Logout")



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
		print("Removed the account from browser")
		message = "Removed currently logged out account from browser"
		self.exporter.logger.error(message)
		self.exporter.logger.file_log(message, url=self.driver.current_url, type='Test - failed')

import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from linkedInHandler import LinkedInHandler
from common_functions import *

class LinkedIn():
	"""docstring for LinkedIn"""
	def __init__(self, exporter):
		super(LinkedIn, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.linkedin_handler = LinkedInHandler(self.driver, self.logger, exporter.get_credentials('linkedin'))
		# self.linkedin_cred_index = 0
		# self.credentials = exporter.get_credentials('linkedin')


	def perform_action(self, action, data=[]):
		# LinkedIn - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.linkedin_handler.warning("Already Logged In to LinkedIn")
			else:
				self.login()
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		# LinkedIn - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.linkedin_handler.warning("Need to Login before logging out from LinkedIn")
			else:
				self.logout()


	def is_user_logged_in(self):
		is_loggedin = False
		try:
			# check if login was successful
			self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
			time.sleep(1)
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
			is_loggedin = True
			return is_loggedin
			# profile_info = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-nav-item"]/div'))).get_attribute('innerHTML')
			# if profile_info:
				# is_loggedin = True
		except Exception as e:
			is_loggedin = False
			return is_loggedin
			pass
		return is_loggedin


	def login(self):
		# self.linkedin_handler.login(action_url)
		if self.linkedin_handler.linkedin_cred_index < len(self.linkedin_handler.credentials):
			self.driver.get(self.linkedin_handler.login_url)
			username = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['username']
			password = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['password']
			if search_element_by_id(self.driver, 'username'):
				try:
					self.linkedin_handler.normal_linkedin_login(username, password)
					error_msg = self.driver.find_element_by_css_selector('#error-for-password').text
					if error_msg:
						raise "Invalid Username or Password"
				except Exception as e:
					retry = self.linkedin_handler.exception(e, 'login')
					if retry :
						self.login()
			else:
				message = "Unable to Identify LinkedIn Login Page"
				super(self.linkedin_handler, self).exception(message)
				pass
		else:
			self.linkedin_handler.exit_process("No LinkedIn accounts available")


	def logout(self):
		# self.linkedin_handler.logout(action_url)
		self.driver.get(self.linkedin_handler.logout_url)
		if search_element_by_id(self.driver, 'nav-settings__dropdown-trigger'):
			try:
				self.linkedin_handler.normal_linkedin_logout()
			except Exception as e:
				message = str(e)
				super(self.linkedin_handler, self).exception(message)
				pass
		else:
			message = "Unable to Identify LinkedIn Logout Page"
			# super(self.linkedin_handler, self).exception(message)
			retry = self.linkedin_handler.exception(message, 'login')
			if retry:
				self.logout()
			pass


	def verify_account(self):
		# self.linkedin_handler.verify_account()
		username = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['username']
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.linkedin_handler.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Email verification - Failed \n"+str(e)
				# super(self.linkedin_handler, self).exception(message)
				retry = self.linkedin_handler.exception(message, 'login')
				if retry:
					self.verify_account()
			pass
		elif search_element_by_id(self.driver, "recaptcha-anchor"):
			try:
				self.linkedin_handler.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Recaptcha verification - Failed \n"+str(e)
				# super(self.linkedin_handler, self).exception(message)
				retry = self.linkedin_handler.exception(message, 'login')
				if retry:
					self.verify_account()
			pass
		elif search_element_by_xpath(self.driver, '//*[@id="app__container"]/main/a'):
			try:
				self.linkedin_handler.linkedin_manual_verification(username)
			except Exception as e:
				# log exception
				message = "\n Manual verification - Failed \n"+str(e)
				# super(self.linkedin_handler, self).exception(message)
				retry = self.linkedin_handler.exception(message, 'login')
				if retry:
					self.verify_account()
			pass
		else:
			if not self.is_user_logged_in():
				message = "Unable to identify linkedIn account verification Page"
				# super(self.linkedin_handler, self).exception(message)
				retry = self.linkedin_handler.exception(message, 'login')
				if retry:
					self.verify_account()
			pass


	def check_login_status(self):
		self.linkedin_handler.check_login_status()


	# LogIn function for LinkedIn Account
	def login_to_linkedin(self):
		self.perform_action("login")
		self.perform_action("verify-account")
		self.perform_action("check-login")
		self.linkedin_handler.remove_synced_accounts()


	# LogOut function for LinkedIn Account
	def logout_from_linkedin(self):
		self.perform_action("logout")



	# Export contacts
	def export_contacts(self):
		time.sleep(1)
		self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
		time.sleep(5)
		# check if user logged in
		if not self.is_user_logged_in():
			# need to call handler
			self.linkedin_handler.warning("Need to LogIn to LinkedIn with sync contacts for exporting contacts")
		else:
			self.linkedin_handler.export_contacts()




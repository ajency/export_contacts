import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from linkedInHandler import linkedInHandler
from common_functions import *

class LinkedIn():
	"""docstring for LinkedIn"""
	def __init__(self, exporter):
		super(LinkedIn, self).__init__()
		self.linkedin_cred_index = 0
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.linkedin_handler = linkedInHandler(self.driver, self.logger, exporter.get_credentials('linkedin'))
		self.exporter = exporter
		self.credentials = self.exporter.get_credentials('linkedin')


	def perform_action(self, action, action_url=""):
		# LinkedIn - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.linkedin_handler.warning("Already Logged In to LinkedIn")
			else:
				self.login(action_url)
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		# LinkedIn - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.linkedin_handler.warning("Need to Login before logging out from LinkedIn")
			else:
				self.logout(action_url)


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


	def login(self, action_url):
		self.linkedin_handler.login(action_url)


	def logout(self, action_url):
		self.linkedin_handler.logout(action_url)
		pass


	def verify_account(self):
		self.linkedin_handler.verify_account()


	def check_login_status(self):
		self.linkedin_handler.check_login_status()


	# LogIn function for LinkedIn Account
	def login_to_linkedin(self):
		self.perform_action("login", "https://www.linkedin.com/login")
		self.perform_action("verify-account")
		self.perform_action("check-login", "https://www.linkedin.com/mynetwork/import-contacts/")


	# LogOut function for LinkedIn Account
	def logout_from_linkedin(self):
		self.perform_action("logout", "https://www.linkedin.com/mynetwork/import-contacts/")



	# Export contacts
	def export_contacts(self):
		time.sleep(1)
		self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
		time.sleep(5)
		# check if user logged in
		if not self.is_user_logged_in():
			# need to call handler
			self.linkedin_handler.warning("Need to LogIn to LinkedIn before exporting")
		else:
			self.linkedin_handler.export_contacts()




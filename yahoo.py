import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yahooHandler import YahooHandler
from common_functions import *

class Yahoo():
	"""docstring for Yahoo"""
	def __init__(self, exporter):
		super(Yahoo, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.yahoo_handler = YahooHandler(self.driver, self.logger, exporter.get_credentials('yahoo'))
		# self.yahoo_cred_index = 0
		# self.credentials = exporter.get_credentials('yahoo')


	def perform_action(self, action, data=[]):
		# Yahoo - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.yahoo_handler.warning("Already Logged In to Yahoo")
			else:
				self.login()
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		elif action == "sync-account":
			if not self.is_user_logged_in():
				self.yahoo_handler.warning("Need to Login to yahoo before syncing contacts")
				self.login_to_yahoo()
			self.sync_contacts()
		# Yahoo - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.yahoo_handler.warning("Need to Login before logging out from Yahoo")
			else:
				self.logout()


	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		# try:
		# 	# remove previous loggedin yahoo accounts
		# 	self.yahoo_handler.remove_previous_loggedin_yahoo_accounts()
		# except Exception as e:
		# 	pass
		is_loggedin = False
		try:
			# check if login was successful
			self.driver.get("https://login.yahoo.com/account")
			self.driver.find_element_by_id('login-username')
			is_loggedin = False
		except Exception as e:
			is_loggedin = True
			pass
		return is_loggedin


	def login(self):
		# self.yahoo_handler.login(action_url)
		if self.yahoo_handler.yahoo_cred_index < len(self.yahoo_handler.credentials):
			# self.driver.get(self.yahoo_handler.login_url)
			username = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['username']
			password = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['password']
			if search_element_by_id(self.driver, 'login-username'):
				try:
					self.yahoo_handler.normal_yahoo_login(username, password)
				except Exception as e:
					retry = self.yahoo_handler.exception(e, 'login')
					if retry:
						self.login_to_yahoo()
			else:
				message = "Unable to Identify Yahoo Login Page"
				super(self.yahoo_handler, self).exception(message)
				pass
		else:
			self.yahoo_handler.exit_process("No Yahoo accounts available")


	def logout(self):
		# self.yahoo_handler.logout(action_url)
		# self.driver.get(self.yahoo_handler.logout_url)
		if search_element_by_id(self.driver, 'ybarAccountMenu'):
			try:
				self.yahoo_handler.normal_yahoo_logout()
			except Exception as e:
				message = str(e)
				super(self.yahoo_handler, self).exception(message)
				pass
		else:
			message = "Unable to Identify Yahoo Logout Page"
			super(self.yahoo_handler, self).exception(message)
			pass


	def verify_account(self):
		# self.yahoo_handler.verify_account()
		username = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['username']
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.yahoo_handler.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Yahoo Email verification - Failed \n"+str(e)
				# super(self.yahoo_handler, self).exception(message)
				retry = self.yahoo_handler.exception(message, 'login')
				if retry:
					self.login_to_yahoo()
			pass
		elif search_element_by_id(self.driver, "playCaptchaButton"):
			try:
				self.yahoo_handler.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Yahoo Recaptcha verification - Failed \n"+str(e)
				# super(self.yahoo_handler, self).exception(message)
				retry = self.yahoo_handler.exception(message, 'login')
				if retry:
					self.login_to_yahoo()
			pass
		else:
			if not self.is_user_logged_in():
				message = "Unable to identify Yahoo account verification Page"
				# super(self.yahoo_handler, self).exception(message)
				retry = self.yahoo_handler.exception(message, 'login')
				if retry:
					self.login_to_yahoo()
			pass


	def check_login_status(self):
		self.yahoo_handler.check_login_status()


	# LogIn function for Yahoo Account
	def login_to_yahoo(self):
		self.driver.get(self.yahoo_handler.login_url)
		self.perform_action("login")
		self.perform_action("verify-account")
		self.perform_action("check-login")


	# LogOut function for Yahoo Account
	def logout_from_yahoo(self):
		self.driver.get(self.yahoo_handler.logout_url)
		self.perform_action("logout")


	def sync_account(self):
		self.perform_action("sync-account")


	def sync_contacts(self):
		self.driver.get(self.yahoo_handler.import_contacts_url)
		if search_element_by_xpath(self.driver, '//*[@id="ember53"]/a'):
			try:
				self.yahoo_handler.normal_sync_yahoo_account()
			except Exception as e:
				# log exception
				message = "\n Sync Yahoo contacts - Failed \n"+str(e)
				# super(self.yahoo_handler, self).exception(message)
				retry = self.yahoo_handler.exception(message, 'login')
				if retry:
					self.sync_contacts()
			pass
		else:
			if self.is_user_logged_in():
				message = "Unable to identify Yahoo Sync Page"
				# super(self.yahoo_handler, self).exception(message)
				retry = self.yahoo_handler.exception(message, 'login')
				if retry:
					self.sync_contacts()
			else:
				self.login_to_yahoo()


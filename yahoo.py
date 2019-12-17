import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from yahooHandler import YahooHandler
from settings import *
from common_functions import *

class Yahoo():
	"""docstring for Yahoo"""
	def __init__(self, exporter):
		super(Yahoo, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.credentials = exporter.get_credentials('yahoo')
		self.credentials = YAHOO_CREDENTIALS
		self.yahoo_handler = YahooHandler(self.driver, self.logger, self.socketio, self.screenshot, self.credentials)
		# clear browser cookies
		# exporter.delete_all_cookies('yahoo')


	def perform_action(self, action, data=[]):
		# Yahoo - Log In code
		if action == "login":
			self.driver.get(self.yahoo_handler.check_login_url)
			if self.yahoo_handler.is_user_logged_in():
				self.yahoo_handler.warning("Already Logged In to Yahoo")
			else:
				self.driver.get(self.yahoo_handler.login_url)
				return self.login()
		elif action == "sync-account":
			if not self.yahoo_handler.is_user_logged_in():
				self.yahoo_handler.warning("Need to Login to yahoo before syncing contacts")
				self.login_to_yahoo()
			return self.sync_contacts()
		# Yahoo - Log Out code
		elif action == "logout":
			if not self.yahoo_handler.is_user_logged_in():
				self.yahoo_handler.warning("Need to Login before logging out from Yahoo")
				return False
			else:
				return self.logout()



	def login(self):
		# self.yahoo_handler.login(action_url)
		if self.yahoo_handler.yahoo_cred_index < len(self.yahoo_handler.credentials):
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['username']
			password = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['password']
			if search_element_by_id(self.driver, 'login-username'):
				try:
					self.yahoo_handler.normal_yahoo_login(username, password)
					return True
				except Exception as e:
					super(YahooHandler, self.yahoo_handler).exception(e, current_url, page_source)
					# self.yahoo_handler.exception(e, current_url, page_source)
					return False
			else:
				message = "Unable to Identify Yahoo Login Page"
				super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
				return False
		else:
			self.yahoo_handler.exit_process("No Yahoo accounts available")
			return False


	def logout(self):
		# self.yahoo_handler.logout(action_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_id(self.driver, 'ybarAccountMenu'):
			try:
				self.yahoo_handler.normal_yahoo_logout()
				return True
			except Exception as e:
				message = str(e)
				super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
				return False
		else:
			message = "Unable to Identify Yahoo Logout Page"
			super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
			return False


	def verify_account(self):
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		username = self.yahoo_handler.credentials[self.yahoo_handler.yahoo_cred_index]['username']
		if not self.yahoo_handler.is_user_logged_in():
			message = "Unable to identify Yahoo account verification Page"
			super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
			# self.yahoo_handler.exception(message, current_url, page_source)


	def check_login_status(self):
		return self.yahoo_handler.check_login_status()


	# LogIn function for Yahoo Account
	def login_to_yahoo(self):
		is_login_page = self.perform_action("login")
		if is_login_page and self.yahoo_handler.is_user_logged_in():
			self.verify_account()
		is_logged_in = self.check_login_status()

		if is_logged_in:
			self.yahoo_handler._log_("::::: Yahoo - Log In - Success")
		else:
			self.yahoo_handler._log_("::::: Yahoo - Log In - Failed")


	# LogOut function for Yahoo Account
	def logout_from_yahoo(self):
		self.driver.get(self.yahoo_handler.logout_url)
		is_logged_out = self.perform_action("logout")
		if is_logged_out:
			self.yahoo_handler._log_("::::: Yahoo - Log Out - Success")
		else:
			self.yahoo_handler._log_("::::: Yahoo - Log Out - Failed")


	def sync_account(self):
		is_account_synced = self.perform_action("sync-account")
		if is_account_synced:
			self.yahoo_handler._log_("::::: Yahoo - Sync Account - Success")
		else:
			self.yahoo_handler._log_("::::: Yahoo - Sync Account - Failed")


	def sync_contacts(self):
		self.driver.get(self.yahoo_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ember53"]/a'):
			try:
				return self.yahoo_handler.normal_sync_yahoo_account()
			except Exception as e:
				# log exception
				message = "\n Sync Yahoo contacts - Failed \n"+str(e)
				super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
				# self.yahoo_handler.exception(message, current_url, page_source)
				return False
			pass
		else:
			if self.yahoo_handler.is_user_logged_in():
				message = "Unable to identify Yahoo Sync Page"
				super(YahooHandler, self.yahoo_handler).exception(message, current_url, page_source)
				# self.yahoo_handler.exception(message, current_url, page_source)
				return False



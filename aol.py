import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from aolHandler import AOLHandler
from settings import *
from common_functions import *

class AOL():
	"""docstring for AOL"""
	def __init__(self, exporter):
		super(AOL, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.credentials = exporter.get_credentials('aol')
		self.credentials = AOL_CREDENTIALS
		self.aol_handler = AOLHandler(self.driver, self.logger, self.socketio, self.screenshot, self.credentials)
		# clear browser cookies
		# exporter.delete_all_cookies('aol')


	def perform_action(self, action, data=[]):
		# AOL - Log In code
		if action == "login":
			self.driver.get(self.aol_handler.check_login_url)
			if self.aol_handler.is_user_logged_in():
				self.aol_handler.warning("Already Logged In to AOL")
			else:
				self.driver.get(self.aol_handler.login_url)
				self.login()
		elif action == "sync-account":
			self.driver.get(self.aol_handler.check_login_url)
			if not self.aol_handler.is_user_logged_in():
				self.aol_handler.warning("Need to Login to AOL before syncing contacts")
				self.login_to_aol()
			return self.sync_contacts()
		# AOL - Log Out code
		elif action == "logout":
			if not self.aol_handler.is_user_logged_in():
				self.aol_handler.warning("Need to Login before logging out from Yahoo")
				return False
			else:
				return self.logout()



	def login(self):
		self.driver.get(self.aol_handler.login_url)
		if self.aol_handler.aol_cred_index < len(self.aol_handler.credentials):
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.aol_handler.credentials[self.aol_handler.aol_cred_index]['username']
			password = self.aol_handler.credentials[self.aol_handler.aol_cred_index]['password']
			if search_element_by_id(self.driver, 'login-username'):
				try:
					self.aol_handler.normal_aol_login(username, password)
					return True
				except Exception as e:
					super(AOLHandler, self.aol_handler).exception(e)
					# self.aol_handler.exception(e, 'login')
					return False
			else:
				message = "Unable to Identify AOL Login Page"
				super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
				return False
		else:
			self.aol_handler.exit_process("No AOL accounts available")
			return False


	def logout(self):
		self.driver.get(self.aol_handler.logout_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ybarAccountMenu"]'):
			try:
				self.aol_handler.normal_aol_logout()
				return True
			except Exception as e:
				message = 'Log out failed '+str(e)
				super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
				return False
		else:
			message = "Unable to Identify AOL Logout Page"
			super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
			return False


	def verify_account(self):
		# self.aol_handler.verify_account()
		username = self.aol_handler.credentials[self.aol_handler.aol_cred_index]['username']
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if not self.aol_handler.is_user_logged_in():
			message = "Unable to identify AOL account verification Page"
			super(AOLHandler, self.aol_handler).exception(message)
			# self.aol_handler.exception(message, current_url, page_source)
		pass


	def check_login_status(self):
		return self.aol_handler.check_login_status()


	# LogIn function for AOL Account
	def login_to_aol(self):
		is_login_page = self.perform_action("login")
		if is_login_page and self.aol_handler.is_user_logged_in():
			self.verify_account()
		is_logged_in = self.check_login_status()
		if is_logged_in:
			self.yahoo_handler._log_("::::: AOL - Log In - Success")
		else:
			self.yahoo_handler._log_("::::: AOL - Log In - Failed")
		return is_logged_in


	# LogOut function for AOL Account
	def logout_from_aol(self):
		self.driver.get(self.aol_handler.logout_url)
		is_logged_out = self.perform_action("logout")
		if is_logged_out:
			self.yahoo_handler._log_("::::: AOL - Log In - Success")
		else:
			self.yahoo_handler._log_("::::: AOL - Log In - Failed")
		return is_logged_out


	def sync_account(self):
		if not self.aol_handler.is_user_logged_in():
			self.aol_handler.warning("Need to Login to AOL before syncing contacts")
			self.login_to_aol()
		is_account_synced = self.sync_contacts()
		if is_account_synced:
			self.yahoo_handler._log_("::::: Yahoo - Sync Account - Success")
		else:
			self.yahoo_handler._log_("::::: Yahoo - Sync Account - Failed")
		return is_account_synced


	def sync_contacts(self):
		self.driver.get(self.aol_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ember63"]/a'):
			try:
				return self.aol_handler.normal_sync_aol_account()
			except Exception as e:
				# log exception
				message = "\n Sync AOL contacts - Failed \n"+str(e)
				super(AOLHandler, self.aol_handler).exception(message)
				# self.aol_handler.exception(message, current_url, page_source)
				return False
		else:
			if self.aol_handler.is_user_logged_in():
				message = "Unable to identify AOL Sync Page"
				super(AOLHandler, self.aol_handler).exception(message)
				# self.aol_handler.exception(message, current_url, page_source)
				return False


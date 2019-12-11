import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from aolHandler import AOLHandler
from common_functions import *

class AOL():
	"""docstring for AOL"""
	def __init__(self, exporter):
		super(AOL, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.aol_handler = AOLHandler(self.driver, self.logger, exporter.get_credentials('aol'))
		# clear browser cookies
		exporter.delete_all_cookies('aol')


	def perform_action(self, action, data=[]):
		# AOL - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.aol_handler.warning("Already Logged In to AOL")
			else:
				self.driver.get(self.aol_handler.login_url)
				self.login()
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		elif action == "sync-account":
			if not self.is_user_logged_in():
				self.aol_handler.warning("Need to Login to AOL before syncing contacts")
				self.login_to_aol()
			self.sync_contacts()
		# AOL - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.aol_handler.warning("Need to Login before logging out from Yahoo")
			else:
				self.logout()


	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		# try:
		# 	# remove previous loggedin AOL accounts
		# 	self.aol_handler.remove_previous_loggedin_yahoo_accounts()
		# except Exception as e:
		# 	pass
		is_loggedin = False
		try:
			# check if login was successful
			self.driver.get("https://login.aol.com/account/personalinfo")
			self.driver.find_element_by_id('login-username')
			is_loggedin = False
		except Exception as e:
			is_loggedin = True
			pass
		return is_loggedin


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
				except Exception as e:
					retry = self.aol_handler.exception(e, 'login')
					if retry:
						self.login_to_aol()
			else:
				message = "Unable to Identify AOL Login Page"
				super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
				pass
		else:
			self.aol_handler.exit_process("No AOL accounts available")


	def logout(self):
		self.driver.get(self.aol_handler.logout_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ybarAccountMenu"]'):
			try:
				self.aol_handler.normal_aol_logout()
			except Exception as e:
				message = 'Log out failed '+str(e)
				super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
				pass
		else:
			message = "Unable to Identify AOL Logout Page"
			super(AOLHandler, self.aol_handler).exception(message, current_url, page_source)
			pass


	def verify_account(self):
		# self.aol_handler.verify_account()
		username = self.aol_handler.credentials[self.aol_handler.aol_cred_index]['username']
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if not self.is_user_logged_in():
			message = "Unable to identify AOL account verification Page"
			# super(AOLHandler, self.aol_handler).exception(message)
			retry = self.aol_handler.exception(message, current_url, page_source)
			if retry:
				self.login_to_aol()
		pass


	def check_login_status(self):
		self.aol_handler.check_login_status()


	# LogIn function for AOL Account
	def login_to_aol(self):
		self.perform_action("login")
		self.perform_action("verify-account")
		self.perform_action("check-login")


	# LogOut function for AOL Account
	def logout_from_aol(self):
		self.driver.get(self.aol_handler.logout_url)
		self.perform_action("logout")


	def sync_account(self):
		self.perform_action("sync-account")


	def sync_contacts(self):
		self.driver.get(self.aol_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ember63"]/a'):
			try:
				self.aol_handler.normal_sync_aol_account()
			except Exception as e:
				# log exception
				message = "\n Sync AOL contacts - Failed \n"+str(e)
				# super(AOLHandler, self.aol_handler).exception(message)
				retry = self.aol_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_aol()
					self.sync_account()
			pass
		else:
			if self.is_user_logged_in():
				message = "Unable to identify AOL Sync Page"
				# super(AOLHandler, self.aol_handler).exception(message)
				retry = self.aol_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_aol()
					self.sync_account()


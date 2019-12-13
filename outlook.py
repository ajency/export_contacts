import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from outlookHandler import OutLookHandler
from common_functions import *

class OutLook():
	"""docstring for OutLook"""
	def __init__(self, exporter):
		super(OutLook, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.outlook_handler = OutLookHandler(self.driver, self.logger, self.socketio, self.screenshot, exporter.get_credentials('outlook'))
		# clear browser cookies
		# exporter.delete_all_cookies('outlook')


	def perform_action(self, action, data=[]):
		# OutLook - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.outlook_handler.warning("Already Logged In to OutLook")
			else:
				self.driver.get(self.outlook_handler.login_url)
				self.login()
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		elif action == "sync-account":
			if not self.is_user_logged_in():
				self.outlook_handler.warning("Need to Login to OutLook before syncing contacts")
				self.login_to_outlook()
			self.sync_contacts()
		# OutLook - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.outlook_handler.warning("Need to Login before logging out from OutLook")
			else:
				self.logout()


	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		is_loggedin = False
		try:
			# check if login was successful
			self.driver.get("https://account.microsoft.com/")
			self.driver.find_element_by_id('mectrl_body_signOut')
			is_loggedin = True
		except Exception as e:
			is_loggedin = False
			pass
		return is_loggedin


	def login(self):
		# self.outlook_handler.login(action_url)
		if self.outlook_handler.outlook_cred_index < len(self.outlook_handler.credentials):
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['username']
			password = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['password']
			if search_element_by_id(self.driver, 'i0116'):
				try:
					self.outlook_handler.normal_outlook_login(username, password)
				except Exception as e:
					retry = self.outlook_handler.exception(e, current_url, page_source)
					if retry:
						self.login_to_outlook()
			else:
				message = "Unable to Identify OutLook Login Page"
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				pass
		else:
			self.outlook_handler.exit_process("No OutLook accounts available")


	def logout(self):
		# self.outlook_handler.logout(action_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_id(self.driver, 'mectrl_body_signOut'):
			try:
				self.outlook_handler.normal_outlook_logout()
			except Exception as e:
				message = str(e)
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				pass
		else:
			message = "Unable to Identify OutLook Logout Page"
			super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
			pass


	def verify_account(self):
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		username = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['username']
		if not self.is_user_logged_in():
			message = "Unable to identify OutLook account verification Page"
			# super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
			retry = self.outlook_handler.exception(message, current_url, page_source)
			if retry:
				self.login_to_outlook()
		pass


	def check_login_status(self):
		self.outlook_handler.check_login_status()


	# LogIn function for OutLook Account
	def login_to_outlook(self):
		self.perform_action("login")
		self.perform_action("verify-account")
		self.perform_action("check-login")


	# LogOut function for OutLook Account
	def logout_from_outlook(self):
		self.driver.get(self.outlook_handler.logout_url)
		self.perform_action("logout")


	def sync_account(self):
		self.perform_action("sync-account")


	def sync_contacts(self):
		self.driver.get(self.outlook_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ember58"]/a'):
			try:
				self.outlook_handler.normal_sync_outlook_account()
			except Exception as e:
				# log exception
				message = "\n Sync OutLook contacts - Failed \n"+str(e)
				# super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				retry = self.outlook_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_outlook()
					self.sync_account()
			pass
		else:
			if self.is_user_logged_in():
				message = "Unable to identify OutLook Sync Page"
				# super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				retry = self.outlook_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_outlook()
					self.sync_account()
			else:
				self.login_to_outlook()


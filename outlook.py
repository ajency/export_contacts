import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from outlookHandler import OutLookHandler
from settings import *
from common_functions import *

class OutLook():
	"""docstring for OutLook"""
	def __init__(self, exporter):
		super(OutLook, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.credentials = exporter.get_credentials('outlook')
		self.credentials = OUTLOOK_CREDENTIALS
		self.outlook_handler = OutLookHandler(self.driver, self.logger, self.socketio, self.screenshot, self.credentials)
		# clear browser cookies
		# exporter.delete_all_cookies('outlook')


	def perform_action(self, action, data=[]):
		# OutLook - Log In code
		if action == "login":
			self.driver.get(self.outlook_handler.check_login_url)
			if self.outlook_handler.is_user_logged_in():
				self.outlook_handler.warning("Already Logged In to OutLook")
				return False
			else:
				self.driver.get(self.outlook_handler.login_url)
				return self.login()
		elif action == "sync-account":
			self.driver.get(self.outlook_handler.check_login_url)
			if not self.outlook_handler.is_user_logged_in():
				self.outlook_handler.warning("Need to Login to OutLook before syncing contacts")
				self.login_to_outlook()
			return self.sync_contacts()
		# OutLook - Log Out code
		elif action == "logout":
			self.driver.get(self.outlook_handler.check_login_url)
			if not self.outlook_handler.is_user_logged_in():
				self.outlook_handler.warning("Need to Login before logging out from OutLook")
				return False
			else:
				return self.logout()



	def login(self):
		# self.outlook_handler.login(action_url)
		if self.outlook_handler.outlook_cred_index < len(self.outlook_handler.credentials):
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['username']
			password = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['password']
			if search_element_by_id(self.driver, 'i0116'):
				try:
					return self.outlook_handler.normal_outlook_login(username, password)
				except Exception as e:
					super(OutLookHandler, self.outlook_handler).exception(e, current_url, page_source)
					# self.outlook_handler.exception(e, current_url, page_source)
					return False
			else:
				message = "Unable to Identify OutLook Login Page"
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				return False
		else:
			self.outlook_handler.exit_process("No OutLook accounts available")
			return False


	def logout(self):
		# self.outlook_handler.logout(action_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_id(self.driver, 'mectrl_body_signOut'):
			try:
				return self.outlook_handler.normal_outlook_logout()
			except Exception as e:
				message = str(e)
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				return False
		else:
			message = "Unable to Identify OutLook Logout Page"
			super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
			return False


	def verify_account(self):
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		username = self.outlook_handler.credentials[self.outlook_handler.outlook_cred_index]['username']
		if not self.outlook_handler.is_user_logged_in():
			message = "Unable to identify OutLook account verification Page"
			super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
			# self.outlook_handler.exception(message, current_url, page_source)
			return False
		return True


	def check_login_status(self):
		return self.outlook_handler.check_login_status()


	# LogIn function for OutLook Account
	def login_to_outlook(self):
		is_login_page = self.perform_action("login")
		if is_login_page and self.outlook_handler.is_user_logged_in():
			self.verify_account()
		is_logged_in = self.check_login_status()
		if is_logged_in:
			self.outlook_handler._log_("step_log: OutLook Login - Success")
		else:
			self.outlook_handler._log_("step_log: OutLook Login - Failed")

		return is_logged_in


	# LogOut function for OutLook Account
	def logout_from_outlook(self):
		self.driver.get(self.outlook_handler.logout_url)
		is_logged_out = self.perform_action("logout")
		if is_logged_out:
			self.outlook_handler._log_("::::: OutLook - Log Out - Success")
		else:
			self.outlook_handler._log_("::::: OutLook - Log Out - Failed")
		return is_logged_out


	def sync_account(self):
		return self.perform_action("sync-account")


	def sync_contacts(self):
		self.driver.get(self.outlook_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath(self.driver, '//*[@id="ember58"]/a'):
			try:
				return self.outlook_handler.normal_sync_outlook_account()
			except Exception as e:
				# log exception
				message = "\n Sync OutLook contacts - Failed \n"+str(e)
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				# self.outlook_handler.exception(message, current_url, page_source)
				return False
		else:
			if self.outlook_handler.is_user_logged_in():
				message = "Unable to identify OutLook Sync Page"
				super(OutLookHandler, self.outlook_handler).exception(message, current_url, page_source)
				# self.outlook_handler.exception(message, current_url, page_source)
				return False


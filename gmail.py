import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from gmailHandler import GmailHandler
from common_functions import *
from settings import *

class Gmail():
	"""docstring for Gmail"""
	def __init__(self, exporter):
		super(Gmail, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.credentials = exporter.get_credentials('gmail')
		self.credentials = GMAIL

		self.gmail_handler = GmailHandler(self.driver, self.logger, self.socketio, self.screenshot, self.credentials)
		# clear browser cookies
		# exporter.delete_all_cookies('gmail')


	def perform_action(self, action, data=[]):
		# Gmail - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.gmail_handler.warning("Already Logged In to Gmail")
			else:
				self.login()
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		elif action == "sync-account":
			if not self.is_user_logged_in():
				self.yahoo_handler.warning("Need to Login to gmail before syncing contacts")
				self.login_to_gmail()
			self.sync_contacts()
		# Gmail - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.gmail_handler.warning("Need to Login before logging out from Gmail")
			else:
				self.logout()


	# check_login_status
	# is_user_logged_in
	def is_user_logged_in(self):
		try:
			# remove previous loggedin gmail accounts
			self.gmail_handler.remove_previous_loggedin_gmail_accounts()
		except Exception as e:
			pass
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


	def login(self):
		# self.gmail_handler.login(action_url)
		if self.gmail_handler.gmail_cred_index < len(self.gmail_handler.credentials):
			# self.driver.get(self.gmail_handler.login_url)
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.gmail_handler.credentials[self.gmail_handler.gmail_cred_index]['username']
			password = self.gmail_handler.credentials[self.gmail_handler.gmail_cred_index]['password']
			if search_element_by_id(self.driver, 'identifierId'):
				try:
					self.gmail_handler.normal_gmail_login(username, password)
				except Exception as e:
					retry = self.gmail_handler.exception(e, current_url, page_source)
					if retry:
						self.login_to_gmail()
			else:
				message = "Unable to Identify Gmail Login Page"
				super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				pass
		else:
			self.gmail_handler.exit_process("No Gmail accounts available")


	def logout(self):
		# self.gmail_handler.logout(action_url)
		try:
			self.gmail_handler.normal_gmail_logout()
		except Exception as e:
			message = str(e)
			super(GmailHandler, self.gmail_handler).exception(message)
			pass


	def verify_account(self):
		# self.gmail_handler.verify_account()
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		username = self.gmail_handler.credentials[self.gmail_handler.gmail_cred_index]['username']
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.gmail_handler.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Gmail Email verification - Failed \n"+str(e)
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.login_to_gmail()
			pass
		elif search_element_by_id(self.driver, "playCaptchaButton"):
			try:
				self.gmail_handler.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Gmail Recaptcha verification - Failed \n"+str(e)
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.login_to_gmail()
			pass
		elif search_element_by_css_selector(self.driver, "li.JDAKTe div.lCoei"):
			try:
				self.gmail_handler.otp_verification(username)
			except Exception as e:
				# log exception
				message = "\n Gmail OTP verification - Failed \n"+str(e)
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.login_to_gmail()
			passs
		else:
			if not self.is_user_logged_in():
				message = "Unable to identify Gmail account verification Page"
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.login_to_gmail()
			pass


	def check_login_status(self):
		self.gmail_handler.check_login_status()


	# LogIn function for Gmail Account
	def login_to_gmail(self):
		self.driver.get(self.gmail_handler.login_url)
		self.perform_action("login")
		self.perform_action("verify-account")
		self.perform_action("check-login")


	# LogOut function for Gmail Account
	def logout_from_gmail(self):
		self.perform_action("logout")


	def sync_account(self):
		self.perform_action("sync-account")


	def sync_contacts(self):
		self.driver.get(self.gmail_handler.import_contacts_url)
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_xpath('//*[@id="ember48"]/a'):
			try:
				self.gmail_handler.normal_sync_gmail_account()
			except Exception as e:
				# log exception
				message = "\n Sync Gmail contacts - Failed \n"+str(e)
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_gmail()
					self.sync_account()
			pass
		else:
			if self.is_user_logged_in():
				message = "Unable to identify Gmail Sync Page"
				# super(GmailHandler, self.gmail_handler).exception(message, current_url, page_source)
				retry = self.gmail_handler.exception(message, current_url, page_source)
				if retry:
					self.logout_from_gmail()
					self.sync_account()
			else:
				self.login_to_gmail()


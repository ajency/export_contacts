import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from gmailHandler import GmailHandler
from common_functions import *

class Gmail():
	"""docstring for Gmail"""
	def __init__(self, exporter):
		super(Gmail, self).__init__()
		self.gmail_cred_index = 0
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.gmail_handler = GmailHandler(self.driver, self.logger, exporter.get_credentials('gmail'))
		self.credentials = exporter.get_credentials('gmail')


	def perform_action(self, action, action_url=""):
		# Gmail - Log In code
		if action == "login":
			if self.is_user_logged_in():
				self.gmail_handler.warning("Already Logged In to Gmail")
			else:
				self.login(action_url)
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		# Gmail - Log Out code
		elif action == "logout":
			if not self.is_user_logged_in():
				self.gmail_handler.warning("Need to Login before logging out from Gmail")
			else:
				self.logout(action_url)


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


	def login(self, action_url):
		self.gmail_handler.login(action_url)


	def logout(self, action_url):
		self.gmail_handler.logout(action_url)


	def verify_account(self):
		self.gmail_handler.verify_account()


	def check_login_status(self):
		self.gmail_handler.check_login_status()


	# LogIn function for Gmail Account
	def login_to_gmail(self):
		self.perform_action("login", "https://accounts.google.com/signin/v2")
		self.perform_action("verify-account")
		self.perform_action("check-login", "https://accounts.google.com")


	# LogOut function for Gmail Account
	def logout_from_gmail(self):
		self.perform_action("logout", "https://www.google.com/accounts/Logout")




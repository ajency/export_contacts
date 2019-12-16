import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from linkedInHandler import LinkedInHandler
# from dbconnector import DbConnector
from common_functions import *
from settings import *
from common_functions import *

class LinkedIn():
	"""docstring for LinkedIn"""
	def __init__(self, exporter):
		super(LinkedIn, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.socketio = exporter.socketio
		self.screenshot = exporter.screenshot
		self.credentials = exporter.get_credentials('linkedin')
		self.credentials = LINKEDIN
		# connector = DbConnector()
		# self.db_connection = connector.connect_db()

		self.linkedin_handler = LinkedInHandler(self.driver, self.logger, self.socketio, self.screenshot, self.credentials)
		# clear browser cookies
		# exporter.delete_all_cookies('linkedin')


	def perform_action(self, action, data=[]):
		# LinkedIn - Log In code
		if action == "login":
			self.driver.get(self.linkedin_handler.check_login_url)
			time.sleep(1)
			if self.linkedin_handler.is_user_logged_in():
				self.linkedin_handler.warning("Already Logged In to LinkedIn")
			else:
				self.driver.get(self.linkedin_handler.login_url)
				self.login()
		elif action == "verify-account":
			if not self.linkedin_handler.is_user_logged_in():
				self.verify_account()
		elif action == "check-login":
			self.check_login_status()
		# LinkedIn - Log Out code
		elif action == "logout":
			if not self.linkedin_handler.is_user_logged_in():
				message = "Need to Login before logging out from LinkedIn"
				self.linkedin_handler.warning(message)
				return False
			else:
				return self.logout()



	def login(self):
		if self.linkedin_handler.linkedin_cred_index < len(self.linkedin_handler.credentials):
			current_url = self.driver.current_url
			page_source = self.driver.page_source
			username = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['username']
			password = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['password']
			if search_element_by_id(self.driver, 'username'):
				try:
					self.linkedin_handler.normal_linkedin_login(username, password)
				except Exception as e:
					# self.linkedin_handler.exception(e, current_url, page_source)
					super(LinkedInHandler, self.linkedin_handler).exception(e, current_url, page_source)
			else:
				message = "Unable to Identify LinkedIn Login Page"
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				pass
		else:
			self.linkedin_handler.exit_process("No LinkedIn accounts available")


	def logout(self):
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		if search_element_by_id(self.driver, 'nav-settings__dropdown-trigger'):
			try:
				self.linkedin_handler.normal_linkedin_logout()
				return True
			except Exception as e:
				message = str(e)
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				pass
		else:
			message = "Unable to Identify LinkedIn Logout Page"
			super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
			# self.linkedin_handler.exception(message, current_url, page_source)
			return False
			pass


	def verify_account(self):
		current_url = self.driver.current_url
		page_source = self.driver.page_source
		username = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['username']
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.linkedin_handler.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Email verification - Failed \n"+str(e)
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				# self.linkedin_handler.exception(message, current_url, page_source)
			pass
		elif search_element_by_id(self.driver, "recaptcha-anchor"):
			try:
				self.linkedin_handler.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Recaptcha verification - Failed \n"+str(e)
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				# self.linkedin_handler.exception(message, current_url, page_source)
			pass
		elif search_element_by_xpath(self.driver, '//*[@id="app__container"]/main/a'):
			try:
				self.linkedin_handler.linkedin_manual_verification(username)
			except Exception as e:
				# log exception
				message = "\n Manual verification - Failed \n"+str(e)
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				# self.linkedin_handler.exception(message, current_url, page_source)
			pass
		else:
			if not self.linkedin_handler.is_user_logged_in():
				message = "Unable to identify linkedIn account verification Page"
				super(LinkedInHandler, self.linkedin_handler).exception(message, current_url, page_source)
				# self.linkedin_handler.exception(message, current_url, page_source)
			pass


	def check_login_status(self):
		self.linkedin_handler.check_login_status()
	

	def remove_synced_accounts(self):
		response = self.linkedin_handler.remove_synced_accounts()
		if response:
			self.linkedin_handler._log_("step_log: Delete previously saved contacts from LinkedIn - Success")
		else:
			self.linkedin_handler._log_("step_log: Delete previously saved contacts from LinkedIn - Failed - "+str(response))


	# LogIn function for LinkedIn Account
	def login_to_linkedin(self):
		self.perform_action("login") 		# redirects to linked import / checks if logged in / if NOT, logs in / Else, warning that it s logged in
		self.perform_action("verify-account") 		# search for verification page [check if logged in else, check verification page]
		self.perform_action("check-login") 				# redirects to linked import / check if user is logged in (success failure message)
		self.driver.get(self.linkedin_handler.check_login_url)
		if self.linkedin_handler.is_user_logged_in():
			self.linkedin_handler._log_("step_log: LinkedIn Login - Success")
		else:
			self.linkedin_handler._log_("step_log: LinkedIn Login - Failed")



	# LogOut function for LinkedIn Account
	def logout_from_linkedin(self):
		self.driver.get(self.linkedin_handler.check_login_url)
		if self.linkedin_handler.is_user_logged_in():
			self.remove_synced_accounts()
		self.driver.get(self.linkedin_handler.logout_url)
		response = self.perform_action("logout")
		if response:
			self.linkedin_handler._log_("step_log: LinkedIn Login - Success")
		else:
			self.linkedin_handler._log_("step_log: LinkedIn Login - Failed")


	def process_retry_login(self, use_diff_cred):
		self.linkedin_handler.continue_with_execution()
		if use_diff_cred.strip().lower() == 'y':
			self.linkedin_handler.linkedin_cred_index += 1

		if self.linkedin_handler.linkedin_cred_index < len(self.linkedin_handler.credentials):
			username = self.linkedin_handler.credentials[self.linkedin_handler.linkedin_cred_index]['username']
			self.linkedin_handler.in_progress("Retrying using "+username+" ...")
			self.perform_action("logout")
			self.login_to_linkedin()
		else:
			self.exit_process("No more LinkedIn accounts available")

	# Export contacts
	def export_contacts(self):
		time.sleep(1)
		self.driver.get(self.linkedin_handler.export_url)
		time.sleep(5)
		# check if user logged in
		if self.linkedin_handler.is_user_logged_in():
			# need to call handler
			self.linkedin_handler.warning("Need to LogIn to LinkedIn with sync contacts for exporting contacts")
			self.linkedin_handler._log_("step_log: LinkedIn Export contacts - Failed")
		else:
			response = self.linkedin_handler.export_contacts()
			self.export_contacts_to_db(response)
			if response:
				self.linkedin_handler._log_("step_log: LinkedIn Export contacts - Success")
			else:
				self.linkedin_handler._log_("step_log: LinkedIn Export contacts - Failed")




	# save contacts to DB
	def export_contacts_to_db(self, contactDataList=[]):
		# save data to DB
		hostname = 'localhost'
		username = 'root123'
		password = 'root123'
		db_name = 'export_contacts'
		table_name = 'contacts'
		try:
			create_db(hostname, db_name, username, password)
			connection = sql_connection(hostname, db_name, username, password)
			# create table 'contacts'
			createTableSql = "CREATE TABLE "+table_name+" (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, email VARCHAR(250) UNIQUE KEY NOT NULL, name VARCHAR(250) NOT NULL, designation VARCHAR(1500) DEFAULT NULL, other_details JSON DEFAULT NULL, updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)"
			execute_custom_sql(connection, createTableSql)
		except Exception as e:
			pass

		for contact in contactDataList or []:
			try:
				mycursor = connection.cursor()
				sql = "INSERT INTO "+table_name+" (email, name, designation, other_details) VALUES (%s, %s, %s, %s)"
				val = (contact[0], contact[1], contact[2], json.dumps({'profile_url':contact[3]}))
				mycursor.execute(sql, val)
				connection.commit()
			except Exception as e:
				print(e)
				# continue




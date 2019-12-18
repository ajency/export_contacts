import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class LinkedInHandler(base_handler):
	"""docstring for LinkedInHandler"""
	def __init__(self, driver, logger, socketio, screenshot, credentials):
		super(LinkedInHandler, self).__init__(driver, logger, socketio, screenshot)
		self.driver = driver
		self.logger = logger
		self.socketio = socketio
		self.linkedin_cred_index = 0
		self.credentials = credentials
		self.continue_execution = True
		self.login_url = "https://www.linkedin.com/login"
		self.logout_url = "https://www.linkedin.com/mynetwork/import-contacts/"
		self.check_login_url = "https://www.linkedin.com/mynetwork/import-contacts/"
		self.import_url = "https://www.linkedin.com/mynetwork/import-contacts/"
		self.export_url = "https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/"
		self.remove_contacts_url = "https://www.linkedin.com/mynetwork/settings/manage-syncing/"


	def exception(self, message, current_url='', page_source=''):
		super(LinkedInHandler, self).exception(message, current_url, page_source)
		# payload = {
		# 	"handler": 'linkedin_exception_handler',
		# 	"message": "Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ",
		# 	"return_to_action": next_step,
		# }
		# json_mylist = json.dumps(mylist, separators=(',', ':'))

		# JS code
		# var obj = JSON.parse('{ "name":"John", "age":30, "city":"New York"}');
		# objectName.propertyName

		# next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		# self.process_exception(next_step, message)
		self.socketio.emit('exception_user_single_request', 'linkedin_exception_handler'+'---'+'Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ')
		self.pause_execution()
		self.wait_until_continue_is_true()

	def process_exception(self, next_step, message=''):
		if next_step.strip().lower() == "x":
			self.exit_process(message)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process()
		else:
			self.continue_process()
			return False


	def retry_process(self):
		self.socketio.emit('exception_user_single_request', 'linkedin_retry_login_handler'+'---'+'Retry using different credentials (y/n)? Default(n) : ')
		# use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
		# self.process_retry(use_diff_cred)
		self.pause_execution()
		self.wait_until_continue_is_true()


	# Normal page load - login 
	def normal_linkedin_login(self, username, password):
		try:
			self.in_progress("Logging into LinkedIn as "+username)
			user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
			user.send_keys(username)
			pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
			pwd.send_keys(password)
			# submit_form
			login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
			login.click()
			try:
				if search_element_by_css_selector(self.driver, "#error-for-password"):
					error_msg = self.driver.find_element_by_css_selector("#error-for-password").text
					# self.exception(error_msg)
					super(LinkedInHandler, self).exception(error_msg)
					return False
			except Exception as e:
				return True
		except Exception as e:
			return False


	def is_user_logged_in(self):
		is_loggedin = False
		try:
			# check if user is loggedin
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
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


	# Normal page load - logout 
	def normal_linkedin_logout(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
		clk.click()
		self.in_progress("Logging out from LinkedIn")
		# Logout
		logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
		logout.click()
		self.success("Logging out from LinkedIn successful")
		return True


	# email verification
	def email_verification(self, username):
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		self.in_progress("Email verification")
		self.socketio.emit('exception_user_single_request', 'linkedin_email_verification_handler'+' --- '+"Please enter the verification code sent to "+username+" inbox: ")
		verify_email.clear()
		# self.pause_execution()
		# self.wait_until_continue_is_true()
		try:
			verification_entered = WebDriverWait(self.driver, 180).until(lambda driver: len(driver.find_element_by_css_selector("#input__email_verification_pin").get_attribute("value")) == 6)
			if verification_entered:
				confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
				self.driver.execute_script("arguments[0].click();", confirm)
				time.sleep(1)
			return True
		except Exception as e:
			return False

	def email_pin_verify(self, user_input):
		self.continue_with_execution()
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		verify_email.send_keys(user_input)
		pass


	# Recaptcha verification
	def recaptcha_verification(self, username):
		not_robot = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
		# not_robot.click()
		super(LinkedInHandler, self).exception("Recaptcha verification")
		return False


	# Restricted verification
	def linkedin_manual_verification(self, username):
		verify = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/a')))
		self.driver.execute_script("arguments[0].click();", verify)
		super(LinkedInHandler, self).exception("LinkedIn manual Identification required")
		return False


	def check_login_status(self):
		username = self.credentials[self.linkedin_cred_index]['username']
		# check if login was successful
		try:
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
			self.driver.execute_script("arguments[0].click();", confirmLogIn)
			# loggedin_as = self.driver.find_element_by_css_selector('#ember463 > div.nav-settings__member.nav-settings__block > div.nav-settings__member-info-container > h3').text
			loggedin_as = self.driver.find_element_by_css_selector('div.nav-settings__member.nav-settings__block > div.nav-settings__member-info-container > h3').text
		except Exception as e:
			loggedin_as = ''

		if self.is_user_logged_in():
			if loggedin_as:
				message = "Logged In into LinkedIn as "+loggedin_as+" successfully"
			else:
				message = "Logged In into LinkedIn successfully"
			# message = "Logged In into LinkedIn as "+username+" successfully"
			self.linkedin_cred_index += 1
			self.success(message)
			return True
		else:
			message = "LinkedIn login for "+username+" failed"
			super(LinkedInHandler, self).exception(message)
			# self.exception(message, 'login')
			return False
			
				


	def export_contacts(self):
		contactList = []
		try:
			WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
		except Exception as e:
			pass

		try:
			time.sleep(5)
			# Total Contacts
			# summary = find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
			summary = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
			totalContacts = int(summary.text.split(" ")[0])
			self.success("Total Contacts : "+str(totalContacts))
			time.sleep(1)
			# scroll to bottom
			prompt = 0
			while prompt<100:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(0.2)
				prompt +=1

			listResults = self.driver.find_elements_by_xpath('//ul[@class="abi-saved-contacts__contact-list"]/li')
			if len(listResults) > 0:
				print("Exporting of contacts is In progress")
				print("____________________________")
				for people in listResults:
					contactDetails = {}
					contactDivId = people.get_attribute('id')

					unwantedTextSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > div > span.contact-summary__name.t-sans.t-16.t-black.t-bold.mr1 > span'
					linkedInNameSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > div > span.contact-summary__name.t-sans.t-16.t-black.t-bold.mr1'
					linkedInDesignationSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > p'
					unwantedText = people.find_element_by_css_selector(unwantedTextSelector).text
					linkedInName = people.find_element_by_css_selector(linkedInNameSelector).text
					linkedInName = linkedInName.replace(unwantedText, '').strip('\n')
					linkedInName = linkedInName.replace(unwantedText, '').strip(' ')
					try:
						linkedInDesignation = people.find_element_by_css_selector(linkedInDesignationSelector).text
					except Exception as e:
						linkedInDesignation = ''
						self.warning(linkedInName+" may not have a designation")

					# open modal to get email & linkedIn Url
					contactClk = self.driver.find_element_by_xpath('//*[@id="'+contactDivId+'"]/div[@class="abi-saved-contacts-row__details"]/button[@class="abi-saved-contacts-row__description"]')
					self.driver.execute_script("arguments[0].click();", contactClk)
					time.sleep(0.2)
					# get details from linkedin
					count = 1
					contactDetailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div'
					linkedContactDetails = self.driver.find_elements_by_xpath(contactDetailSelector)
					# Default email selector
					linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div[1]/p'
					for detail in linkedContactDetails:
						label = detail.find_element_by_xpath('.//label').text
						if label == 'Email address':
							linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div['+str(count)+']/p'
							break
						count += 1

					linkedInUrlSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[1]/div[2]/div/div/span/a'
					linkedInEmail = self.driver.find_element_by_xpath(linkedInEmailSelector).text
					try:
						linkedInUrl = self.driver.find_element_by_xpath(linkedInUrlSelector).get_attribute('href')
						# linkedInUrl = 'https://www.linkedin.com'+linkedInUrl
					except Exception as e:
						linkedInUrl = ''
						self.warning(linkedInName+" may not have a LinkedIn Account")

					# clode modal
					cancelSelector = '//*[@id="artdeco-modal-outlet"]/div/div/button'
					# cancelClk = find_element_by_xpath_with_timeout(self.driver, cancelSelector, [], 10)
					cancelClk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, cancelSelector)))
					self.driver.execute_script("arguments[0].click();", cancelClk)
					contactDetails = [linkedInEmail, linkedInName, linkedInDesignation, linkedInUrl]
					contactList.append(contactDetails)
			return contactList
		except Exception as e:
			super(LinkedInHandler, self).exception("Exception: "+str(e)+"\n Unable to Export contacts")
			return []



	# Remove previous synced accounts
	def remove_synced_accounts(self):
		# Need to re-modify
		self.driver.get(self.remove_contacts_url)
		time.sleep(5)
		try:
			removeAllClk = self.driver.find_element_by_xpath('//*[@id="ember44"]/div[1]/button')
			removeAllClk.click()
			rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button'
			rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
			rmvClk2.click()
		except Exception as e:
			try:
				listResults = self.driver.find_elements_by_xpath('//*[@id="ember42"]/section/ul/div') # //ul[@class="list-style-none.mh5"]/div
				for account in listResults or []:
					rmvClk = account.find_element_by_xpath('.//li/div/button')
					self.driver.execute_script("arguments[0].click();", rmvClk)
					rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button[@class="js-mn-manage-source-confirm"]'
					rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
					self.driver.execute_script("arguments[0].click();", rmvClk2)
			except Exception as e:
				# self.warning("Removal of synced accounts failed")
				pass
			pass
		time.sleep(5)
		self.driver.get(self.export_url)
		time.sleep(1)

		try:
			WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="artdeco-toasts"]/ul/li/div/p/span')))
		except Exception as e:
			pass

		if search_element_by_xpath(self.driver, '//*[@id="artdeco-toasts"]/ul/li/div/p/span'):
			try:
				response = self.driver.find_elements_by_xpath('//*[@id="artdeco-toasts"]/ul/li/div/p/span').text
				self.warning(response)

				rmvClk = account.find_element_by_xpath('//*[@id="artdeco-toasts"]/ul/li/button')
				self.driver.execute_script("arguments[0].click();", rmvClk)
			except Exception as e:
				pass

		try:
			# find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
			self.warning("Unable to remove synced accounts")
			return False
		except Exception as e:
			self.warning("Removal of synced accounts was successful")
			return True
			pass
		time.sleep(1)


	def pause_execution(self):
		# SET False to pause execution
		self.continue_execution = False

	def continue_with_execution(self):
		# SET True to continue execution
		self.continue_execution = True

	def wait_until_continue_is_true(self):
		# wait until self.continue_execution = True
		self.custom_wait_until_continue_is_true()

	def custom_wait_until_continue_is_true(self, waiting_time=120):
		# wait until self.continue_execution = True OR custom waiting time as passed
		waiting_time = int(waiting_time)
		while waiting_time > 0:
			if self.continue_execution:
				# self.custom_wait_until_continue_is_true(0)
				break
			else:
				print('Timer: '+str(waiting_time))
				time.sleep(0.98)
				waiting_time = waiting_time - 1
				self.custom_wait_until_continue_is_true(waiting_time)

		self.continue_execution = True

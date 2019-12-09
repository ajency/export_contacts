import os,sys,time,csv,datetime,platform
from handler import Handler as base_handler
from common_functions import *

class LinkedInHandler(base_handler):
	"""docstring for LinkedInHandler"""
	def __init__(self, driver, logger, credentials):
		super(LinkedInHandler, self).__init__(driver, logger)
		self.driver = driver
		self.logger = logger
		self.linkedin_cred_index = 0
		self.credentials = credentials
		self.login_url = "https://www.linkedin.com/login"
		self.logout_url = "https://www.linkedin.com/mynetwork/import-contacts/"
		self.import_url = "https://www.linkedin.com/mynetwork/import-contacts/"
		self.export_url = "https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/"


	def exception(self, message, retry_method, data=[]):
		next_step = input("Do you want to Retry(r), Continue(c) OR Exit(x)? Default(c): ")
		if next_step.strip().lower() == "x":
			self.exit_process(message)
			return False
		elif next_step.strip().lower() == "r":
			self.retry_process(retry_method, data)
		else:
			self.continue_process()
			return False


	def retry_process(self, retry_action, data=[]):
		if retry_action == 'login':
			use_diff_cred = input("Retry using different credentials (y/n)? Default(n) : ")
			if use_diff_cred.strip().lower() == 'y':
				self.linkedin_cred_index += 1

			if self.linkedin_cred_index < len(self.credentials):
				username = self.credentials[self.linkedin_cred_index]['username']
				password = self.credentials[self.linkedin_cred_index]['password']
				self.in_progress("Retrying using "+username)
				return True
			else:
				self.exit_process("No more LinkedIn accounts available")
				return False
		else:
			self.exit_process("Unknown LinkedIn Retry Method")
		return False



	# Normal page load - login 
	def normal_linkedin_login(self, username, password):
		self.in_progress("Logging into LinkedIn as "+username)
		user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
		user.send_keys(username)
		pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
		pwd.send_keys(password)
		# submit_form
		login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
		login.click()


	# Normal page load - logout 
	def normal_linkedin_logout(self):
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
		clk.click()
		self.in_progress("Logging out from LinkedIn")
		# Logout
		logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
		logout.click()
		self.success("Logging out from LinkedIn successful")




	# email verification
	def email_verification(self, username):
		verify_email = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		self.in_progress("Email verification")
		verify_email.clear()
		user_input = input("Please enter the verification code sent to "+username+" inbox: ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		self.driver.execute_script("arguments[0].click();", confirm)
		pass


	# Recaptcha verification
	def recaptcha_verification(self, username):
		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
		super(LinkedInHandler, self).exception("Recaptcha verification")
		pass


	def check_login_status(self):
		username = self.credentials[self.linkedin_cred_index]['username']
		try:
			# check if login was successful
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
			message = "Logged In into LinkedIn as "+username+" successfully"
			self.linkedin_cred_index += 1
			self.success(message)
		except Exception as e:
			message = "LinkedIn login for "+username+" failed"
			# super(LinkedInHandler, self).exception(message)
			self.exception(message, 'login', self.login_url)


	def export_contacts(self):
		contactList = []
		try:
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
				time.sleep(0.1)
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
			super(LinkedInHandler, self).exception("Exception: "+e+"\n Unable to Export contacts")




	# # Remove previous synced accounts
	# def remove_synced_accounts():
	# 	# Need to re-modify
	# 	self.driver.get("https://www.linkedin.com/mynetwork/settings/manage-syncing/")
	# 	time.sleep(5)
	# 	try:
	# 		removeAllClk = self.driver.find_element_by_xpath('//*[@id="ember44"]/div[1]/button')
	# 		removeAllClk.click()
	# 		rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button'
	# 		rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
	# 		rmvClk2.click()
	# 	except Exception as e:
	# 		print(e)
	# 		try:
	# 			listResults = self.driver.find_elements_by_xpath('//*[@id="ember42"]/section/ul/div') # //ul[@class="list-style-none.mh5"]/div
	# 			for account in listResults or []:
	# 				rmvClk = account.find_element_by_xpath('.//li/div/button')
	# 				self.driver.execute_script("arguments[0].click();", rmvClk)
	# 				rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button[@class="js-mn-manage-source-confirm"]'
	# 				rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
	# 				self.driver.execute_script("arguments[0].click();", rmvClk2)
	# 		except Exception as e:
	# 			print(e)
	# 			print("Removal of synced failed")
	# 			pass
	# 		pass
	# 	time.sleep(1)
	# 	self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
	# 	time.sleep(5)
	# 	try:
	# 		# find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
	# 		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
	# 		print("Unable to remove synced accounts")
	# 	except Exception as e:
	# 		print("Removal of synced accounts was successful")
	# 	time.sleep(1)

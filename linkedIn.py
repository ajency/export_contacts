import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common_functions import *

class LinkedIn():
	"""docstring for LinkedIn"""
	def __init__(self, exporter):
		super(LinkedIn, self).__init__()
		self.linkedin_cred_index = 0
		self.driver = exporter.driver
		self.exporter = exporter
		self.credentials = self.exporter.get_credentials('linkedin')


	def perform_action(self, action, action_url=""):
		# LinkedIn - Log In code
		if action == "login":
			self.login(action_url)
		# LinkedIn - Log Out code
		elif action == "logout":
			self.logout(action_url)
		elif action == "verify-account":
			self.verify_account()
		elif action == "check-login":
			self.is_user_logged_in()


	def login(self, action_url):
		self.driver.get(action_url)
		if self.linkedin_cred_index < len(self.credentials):
			username = self.credentials[self.linkedin_cred_index]['username']
			password = self.credentials[self.linkedin_cred_index]['password']
			
			if search_element_by_id(self.driver, 'username'):
				try:
					self.normal_linkedin_login(username, password)
				except Exception as e:
					message = "\n Exception: "+str(e)+"\n Page Source: \n"+driver.page_source+"\n"
					self.exporter.logger.error(message)
					self.exporter.logger.file_log(message, driver.current_url, "Login Error")
			else:
				# need to call handler
				pass
		else:
			print("no more linkedin accounts")


	def logout(self, action_url):
		self.driver.get(action_url)
		if search_element_by_id(self.driver, 'nav-settings__dropdown-trigger'):
			try:
				self.normal_linkedin_logout()
			except Exception as e:
				# log exception
				message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
				self.exporter.logger.error(message)
				self.exporter.logger.file_log(message, url=self.driver.current_url, type='Log Out - Failed')
				pass
		else:
			# need to call handler
			pass
		
		pass


	def verify_account(self):
		if search_element_by_id(self.driver, 'input__email_verification_pin'):
			try:
				self.email_verification(username)
			except Exception as e:
				# log exception
				message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
				self.exporter.logger.error(message)
				self.exporter.logger.file_log(message, url=self.driver.current_url, type='Email verify - Failed')
			pass
		elif search_element_by_id(self.driver, "recaptcha-anchor"):
			try:
				self.recaptcha_verification(username)
			except Exception as e:
				# log exception
				message = "\n Exception: "+str(e)+"\n Page Source: \n"+self.driver.page_source+"\n"
				self.exporter.logger.error(message)
				self.exporter.logger.file_log(message, url=self.driver.current_url, type='Recaptcha verify - Failed')
			pass
		else:
			# need to call handler
			pass



	# Normal page load - login 
	def normal_linkedin_login(self, username, password):
		self.exporter.logger.info("Logging into LinkedIn as "+username)
		self.exporter.logger.file_log("Logging into LinkedIn as "+username, url=self.driver.current_url, type='')
		user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
		user.send_keys(username)
		# pwd = find_element_by_id_with_timeout(self.driver, 'password', [], 10)
		pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
		pwd.send_keys(password)
		# submit_form
		# login = find_element_by_xpath_with_timeout(self.driver, '//*[@id="app__container"]/main/div/form/div[3]/button', [], 10)
		login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
		login.click()


	# Normal page load - logout 
	def normal_linkedin_logout(self):
		# clk = find_element_by_xpath_with_timeout(self.driver, '//*[@id="nav-settings__dropdown-trigger"]', [], 10)
		clk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
		clk.click()
		self.exporter.logger.info("Logging out from LinkedIn")
		self.exporter.logger.file_log("Logging out from LinkedIn", url=self.driver.current_url, type='')
		# Logout
		# logout = find_element_by_xpath_with_timeout(self.driver, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li', [], 10)
		logout = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
		logout.click()
		self.exporter.logger.info("Logging out from LinkedIn successful")
		self.exporter.logger.file_log("Logging out from LinkedIn successful", url=self.driver.current_url, type='')


	# email verification
	def email_verification(self):
		verify_email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		print("Email verification required")
		verify_email.clear()
		user_input = input("Please enter the verification code sent via mail to "+username+": ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		driver.execute_script("arguments[0].click();", confirm)
		pass


	# Recaptcha verification
	def recaptcha_verification(self):
		WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
		print("Recaptcha verification required")
		pass


	def is_user_logged_in(self):
		username = self.credentials[self.linkedin_cred_index]['username']
		try:
			# check if login was successful
			# confirmLogIn = find_element_by_xpath_with_timeout(self.driver, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon', [], 10)
			confirmLogIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
			message = "LinkedIn login for "+username+" was successful"
			self.exporter.logger.info(message)
			self.linkedin_cred_index += 1
			self.exporter.logger.file_log(message, url=self.driver.current_url, type='Test - success')
		except Exception as e:
			message = "LinkedIn login for "+username+" failed"
			self.exporter.logger.error(message)
			self.exporter.logger.file_log(message, url=self.driver.current_url, type='Test - failed')


	# LogIn function for LinkedIn Account
	def login_to_linkedin(self):
		self.perform_action("login", "https://www.linkedin.com/login")
		self.perform_action("verify-account")
		self.perform_action("check-login", "https://www.linkedin.com/mynetwork/import-contacts/")


	# LogOut function for LinkedIn Account
	def logout_from_linkedin(self):
		self.perform_action("logout", "https://www.linkedin.com/mynetwork/import-contacts/")



	# Export contacts
	def export_contacts(self):
		time.sleep(1)
		self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
		time.sleep(5)

		contactList = []
		# check if user logged in
		try:
			# find_element_by_id_with_timeout(self.driver, 'username', [], 10)
			notLoggedIn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
			print("Exporting of contacts requires logging in into linkedIn")
		except Exception as e:
			pass

		try:
			# Total Contacts
			# summary = find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
			summary = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
			totalContacts = int(summary.text.split(" ")[0])
			print("Total Contacts : "+str(totalContacts))
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
					print(linkedInName+" may not have a designation")

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
					print(linkedInName+" may not have a LinkedIn Account")

				# clode modal
				cancelSelector = '//*[@id="artdeco-modal-outlet"]/div/div/button'
				# cancelClk = find_element_by_xpath_with_timeout(self.driver, cancelSelector, [], 10)
				cancelClk = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, cancelSelector)))
				self.driver.execute_script("arguments[0].click();", cancelClk)
				contactDetails = [linkedInEmail, linkedInName, linkedInDesignation, linkedInUrl]
				contactList.append(contactDetails)
			return contactList
		except Exception as e:
			print(e)
			print("Unable to Export contacts")


	# Remove previous synced accounts
	def remove_synced_accounts():
		# Need to re-modify
		self.driver.get("https://www.linkedin.com/mynetwork/settings/manage-syncing/")
		time.sleep(5)
		try:
			removeAllClk = self.driver.find_element_by_xpath('//*[@id="ember44"]/div[1]/button')
			removeAllClk.click()
			rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button'
			rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
			rmvClk2.click()
		except Exception as e:
			print(e)
			try:
				listResults = self.driver.find_elements_by_xpath('//*[@id="ember42"]/section/ul/div') # //ul[@class="list-style-none.mh5"]/div
				for account in listResults or []:
					rmvClk = account.find_element_by_xpath('.//li/div/button')
					self.driver.execute_script("arguments[0].click();", rmvClk)
					rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button[@class="js-mn-manage-source-confirm"]'
					rmvClk2 = self.driver.find_element_by_xpath(rmvclk2Selector)
					self.driver.execute_script("arguments[0].click();", rmvClk2)
			except Exception as e:
				print(e)
				print("Removal of synced failed")
				pass
			pass
		time.sleep(1)
		self.driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
		time.sleep(5)
		try:
			# find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
			print("Unable to remove synced accounts")
		except Exception as e:
			print("Removal of synced accounts was successful")
		time.sleep(1)



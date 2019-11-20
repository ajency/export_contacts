# # pip install selenium
# # pip install phantomjs
# # Linux chrome browser version - Version 78.0.3904.108
# # https://chromedriver.storage.googleapis.com/index.html?path=78.0.3904.105/

import json
import signal
import logging
import mysql.connector
import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Functions Defined
def create_db(host_name, mydatabase, user_name, password):
	mydb = mysql.connector.connect(
	  host=host_name,
	  user=user_name,
	  passwd=password
	)
	mycursor = mydb.cursor()
	try:
		mycursor.execute("CREATE DATABASE "+mydatabase)
	except Exception as e:
		print(e)
		pass

def sql_connection(host_name, mydatabase, user_name, password):
	mydb = mysql.connector.connect(
	  host=host_name,
	  user=user_name,
	  passwd=password,
	  database=mydatabase
	)
	return mydb

def execute_custom_sql(connection, sql):
	mycursor = connection.cursor()
	mycursor.execute(sql)
	myresult = mycursor.fetchall()

# def insert_into_db_table(connection, table, fields, values):
# 	mycursor = connection.cursor()
# 	field_count = len(fields)-1
# 	sql = "INSERT INTO "+table+" ("+', '.join(fields)+") VALUES (%s, %s)"
# 	# val = ("John", "Highway 21")
# 	val = values
# 	mycursor.execute(sql, val)
# 	mydb.commit()

def update_db_table(connection, table, update_fields, where_condition):
	mycursor = connection.cursor()
	update_fields_str = ''
	where_condition_str = ''
	for field,value in enumerate(update_fields):
		update_fields_str += field+" = '"+value+"', "
	
	for field,value in enumerate(where_condition):
		update_str += " AND "+field+" = "+value

	# remove last comma
	update_fields_str = update_fields_str[:-2]

	sql = "UPDATE "+table+" SET "+update_fields_str+" WHERE 1=1"+where_condition_str
	mycursor.execute(sql)
	mydb.commit()


# Below 2 functions are user input with timeout
def get_user_input(message, default_value=Keys.RETURN):
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(5)
	try:
		user_input = raw_input(message)
	except:
		user_input = default_value
	print('')
	return user_input

def handler():
	print "timeout"


# LogIn function for Gmail Account
def login_to_gmail(driver, username, password):
	print("Logging In into Gmail as "+username)
	try:
		driver.get("https://accounts.google.com/")
		driver.find_element_by_id('identifierId').send_keys(username)
		driver.find_element_by_id("identifierNext").click()
		time.sleep(5)
		pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = driver.find_element_by_id("passwordNext")
		login.click()
	except Exception as e:
		print("Page elements were not found")
		logging.debug("Page elements were not found")
	# driver.save_screenshot("2.png")


# LogOut function for Gmail Account
def logout_from_gmail(driver):
	print("Logging out from Gmail")
	try:
		driver.get("https://accounts.google.com/")
		# Logout drop down
		clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
		clk.click()
		# Logout
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gb_71")))
		logout.click()
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]')))
			removeAccounttClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[3]')))
			removeAccounttClk.click()
			selectClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/ul/li[1]')))
			selectClk.click()
			removeClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[1]/span')))
			removeClk.click()
			time.sleep(3)
			print("Removed the account from browser")
		except Exception as e:
			pass
	except Exception as e:
		print(e)


# LogIn function for LinkedIn Account
def login_to_linkedin(driver, username, password):
	print("Logging In into linkedIn as "+username)
	try:
		driver.get("https://www.linkedin.com/login")
		user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
		user.send_keys(username)
		pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
		pwd.send_keys(password)
		# submit_form
		login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
		login.click()
	except Exception as e:
		print("Page elements were not found")
		logging.debug("Page elements were not found")


# LogOut function for LinkedIn Account
def logout_from_linkedin(driver):
	try:
		remove_synced_accounts(driver)
	except Exception as e:
		print(e)
		print("Unable to remove synced accounts from linkedIn account")

	print("Logging out from linkedIn")
	try:
		driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
		# Logout drop down
		clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
		clk.click()
		# Logout
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
		logout.click()
	except Exception as e:
		print(e)



# Import contacts from Gmail to LinkedIn
def import_contacts(driver, username):
	print("Importing contacts from gmail("+username+")")
	global linkedin_credentials
	driver.get("https://www.linkedin.com/mynetwork/import-contacts/")	
	time.sleep(3)
	clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember48"]/a')))
	clk.click()
	time.sleep(3)
	# Check if any account needs to be selected
	if len(driver.window_handles) > 1:
		time.sleep(5)
		# switch the pop-up window
		driver.switch_to.window(driver.window_handles[1])
		accountSelector = '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[1]'
		account = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, accountSelector)))
		account.click()
		confirmAccount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'submit_approve_access')))
		# confirmAccount.click()
		driver.execute_script("arguments[0].click();", confirmAccount)
		if len(driver.window_handles) > 1:
			#switch back to original window
			time.sleep(0.5)
			try:
				backToPrevWindow = WebDriverWait(driver.window_handles[1], 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="minimal-util-nav"]/ul/li[1]/a')))
				backToPrevWindow.click()
			except Exception as e:
				print("return to LinkedIn")
		else:
			print("Error Occured while Importing Contacts from Gmail Account("+username+")")
		driver.switch_to.window(driver.window_handles[0])
	try:
		time.sleep(3)
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact-select-checkbox"]')))
		print("Contacts imported from Gmail["+username+"] to LinkedIn")
	except Exception as e:
		# print(e)
		print("Error in importing contacts from Gmail["+username+"]")
		continueExec = get_user_input("continue execution with same LinkedIn Account (Default:No)? (y/n) ", 'n')
		if continueExec.strip().lower() == 'n' and nextLinkedInCredIndex < len(linkedin_credentials):
			logout_from_linkedin(driver)
			switch_to_linkedin_account(driver, nextLinkedInCredIndex)
		else:
			print("continuing with same linkedIn account for remaining accounts sync..")



def switch_to_linkedin_account(driver, nextCredIndex=0):
	global gmail_credentials
	global linkedin_credentials
	global nextLinkedInCredIndex
	linkedinUsername = linkedin_credentials[nextCredIndex]['username']
	linkedinPassword = linkedin_credentials[nextCredIndex]['password']
	login_to_linkedin(driver, linkedinUsername, linkedinPassword)
	nextCredIndex += 1
	nextLinkedInCredIndex = nextCredIndex
	try:
		# check if login was successful
		driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
		print("LinkedIn login for "+linkedinUsername+" was successful")
		logging.debug("LinkedIn Log In for "+linkedinUsername+" was successful")
		counter = 0
		while counter < len(gmail_credentials):
			switch_to_gmail_account(driver, counter)
			counter += 1
	except Exception as e:
		print("LinkedIn login for "+linkedinUsername+" failed")
		logging.debug("LinkedIn login for "+linkedinUsername+" failed")
		switch_to_linkedin_account(driver, nextLinkedInCredIndex)


def switch_to_gmail_account(driver, nextCredIndex=0):
	global gmail_credentials
	gmailUsername = gmail_credentials[nextCredIndex]['username']
	gmailPassword = gmail_credentials[nextCredIndex]['password']
	login_to_gmail(driver, gmailUsername, gmailPassword)
	nextCredIndex += 1
	time.sleep(3)
	try:
		# check if login was successful
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
		print("Gmail Log In for "+gmailUsername+" was successful")
		logging.debug("Gmail Log In for "+gmailUsername+" was successful")
		# import_contacts
		import_contacts(driver, gmailUsername)
		logout_from_gmail(driver)
	except Exception as e:
		# print(e)
		print("Gmail login for "+gmailUsername+" failed")
		logging.debug("Gmail login for "+gmailUsername+" failed")


def export_contacts(driver):
	time.sleep(1)
	driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
	time.sleep(5)
	try:
		# Total Contacts
		summary = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
		totalContacts = int(summary.text.split(" ")[0])
		print("Total Contacts : "+str(totalContacts))
		time.sleep(1)
		# scroll to bottom
		prompt = 0
		while prompt<100:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(0.1)
			prompt +=1

		contactList = []
		# listResults = driver.find_elements_by_xpath('//*[@id="ember58"]/ul/li/div[@class="abi-saved-contacts-row__details"]/button/div')
		listResults = driver.find_elements_by_xpath('//ul[@class="abi-saved-contacts__contact-list"]/li')
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
				print(linkedInName+" may not have a designation")
				linkedInDesignation = ''

			# open modal to get email & linkedIn Url
			contactClk = driver.find_element_by_xpath('//*[@id="'+contactDivId+'"]/div[@class="abi-saved-contacts-row__details"]/button[@class="abi-saved-contacts-row__description"]')
			driver.execute_script("arguments[0].click();", contactClk)
			time.sleep(0.2)
			# get details
			count = 1
			contactDetailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div'
			linkedContactDetails = driver.find_elements_by_xpath(contactDetailSelector)
			# Default email selector
			linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div[1]/p'
			for detail in linkedContactDetails:
				label = detail.find_element_by_xpath('.//label').text
				if label == 'Email address':
					linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div['+str(count)+']/p'
					break
				count += 1

			linkedInUrlSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[1]/div[2]/div/div/span/a'
			linkedInEmail = driver.find_element_by_xpath(linkedInEmailSelector).text
			try:
				linkedInUrl = driver.find_element_by_xpath(linkedInUrlSelector).get_attribute('href')
				# linkedInUrl = 'https://www.linkedin.com'+linkedInUrl
			except Exception as e:
				linkedInUrl = ''

			# close modal
			cancelSelector = '//*[@id="artdeco-modal-outlet"]/div/div/button'
			cancelClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cancelSelector)))
			driver.execute_script("arguments[0].click();", cancelClk)
			contactDetails = [linkedInEmail, linkedInName, linkedInDesignation, linkedInUrl]
			contactList.append(contactDetails)
		return contactList
	except Exception as e:
		# print(e)
		print("Unable to Export contacts")


def export_contacts_to_csv(contactDataList):
	# convert array to CSV
	with open('downloads/contact_details'+str(datetime.datetime.now()).replace('.', '_')+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(contactDataList)
	csvFile.close()


def export_contacts_to_db(contactDataList):
	# save data to DB
	hostname = 'localhost'
	username = 'root123'
	password = 'root123'
	db_name = 'python_temp'
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


def remove_synced_accounts(driver):
	driver.get("https://www.linkedin.com/mynetwork/settings/manage-syncing/")
	time.sleep(5)
	listResults = driver.find_elements_by_xpath('//*[@id="ember42"]/section/ul/div') # //ul[@class="list-style-none.mh5"]/div
	try:
		for account in listResults or []:
			rmvClk = account.find_element_by_xpath('.//li/div/button')
			driver.execute_script("arguments[0].click();", rmvClk)
			rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button[@class="js-mn-manage-source-confirm"]'
			rmvClk2 = driver.find_element_by_xpath(rmvclk2Selector)
			driver.execute_script("arguments[0].click();", rmvClk2)
	except Exception as e:
		# print(e)
		pass
	time.sleep(1)
	driver.get("https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/")
	time.sleep(5)
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
		print("Unable to remove synced accounts")
	except Exception as e:
		print("Removal of synced accounts was successful")
	time.sleep(1)




# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')
LOG_FILENAME = 'custom_logs.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

# Program Execution
gmail_credentials = [
	{"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	{"username": "ralph110293@gmail.com", "password": "ajency#123"},
]

linkedin_credentials = [
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	{"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
	{"username": "ralph110293@gmail.com", "password": "ajency#123"},
]

# operating system 
if platform.system().lower() == 'linux':
	driver_path = "assets/linux/chrome_unix_driver"
	# phantomjs_path = "assets/linux/phantomjs"
elif platform.system().lower() == 'windows':
	driver_path = "assets/windows/chrome_win32_driver.exe"
	# phantomjs_path = "assets/windows/phantomjs"
else:
	driver_path = "assets/mac/chrome_mac_driver"
	# phantomjs_path = "assets/mac/phantomjs"


continueExec = get_user_input("Do you want to execute in normal browser mode (Default:No)? (y/n): ")
if continueExec.strip().lower() == 'y':
	# Normal Browser
	driver = webdriver.Chrome(driver_path)
else:
	print("Running in Headless browser mode..")
	# PhanthomJS
	# desired_capability = DesiredCapabilities.PHANTOMJS
	# # User Agent: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
	# desired_capability["phantomjs.page.settings.userAgent"] = (
	# 	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
	# 	)

	# driver = webdriver.PhantomJS(phantomjs_path)
	# driver.set_window_size(1120, 550)

	# Headless Browser
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
	chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options,
	  service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])


nextLinkedInCredIndex = 0
switch_to_linkedin_account(driver, nextLinkedInCredIndex)
contactDataList = export_contacts(driver)
export_contacts_to_db(contactDataList)
logout_from_linkedin(driver)
# End Driver
driver.quit()

contactCSVDataList = contactDataList or []
export_contacts_to_csv([["Email ID", "Contact Name", "Designation", "LinkedIn link"]]+contactCSVDataList)

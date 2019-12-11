import re
import json
import boto3
import pickle
import signal
import socket
import logging
import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

 
# initialize the log settings
logging.basicConfig(filename = 'app.log', level = logging.INFO)

email_credentials = [
	# {"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	{"username": "stinfordpaulie18@yahoo.com", "password": "ajency#123"},		#microsoft outlook & yahoo
	# {"username": "stinfordpaulie18@aol.com", "password": "ajency#123"},			#aol
	# {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},			#gmail
]

linkedin_credentials = [
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	# {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
	# {"username": "ralph110293@gmail.com", "password": "ajency#123"},
]
nextEmailCredIndex = 0
nextLinkedInCredIndex = 0


def lambda_handler(event, context):
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	print("Your Computer Name is:" + hostname)    
	print("Your Computer IP Address is:" + IPAddr) 

	# Program Execution
	driver = initialize_new_driver()
	print("Running in Headless browser mode..")

	executor_url = driver.command_executor._url
	session_id = driver.session_id
	print("Session ID: "+session_id)
	print("Command Executor: "+executor_url)
	go_to_step(driver)
	driver.close()
	sys.exit()

	# initiate_driver = input("To create new instance, enter 'reset' & press enter. ")
	# driver = initialize_driver(initiate_driver)
	# retreive_driver_cookies(driver, "https://accounts.google.com/")
	# switch_to_gmail_account(driver)
	# # save_cookies(driver)

	# # retreive_driver_cookies(driver, "https://www.linkedin.com/")
	# # switch_to_linkedin_account(driver)
	# # save_cookies(driver)

	# # logout_from_linkedin(driver)
	# input("wert")
	# logout_from_gmail(driver)
	# # # import_contacts
	# # import_contacts(driver, gmailUsername)
	# print("Execution Completed")
	# # End Driver
	# # delete_all_cookies(driver)

def go_to_step(driver):
	global nextEmailCredIndex
	global nextLinkedInCredIndex
	print("")
	print("Choose your next step as below:")
	print("A - Login into Gmail")
	print("B - Login into LinkedIn")
	print("C - Logout from LinkedIn")
	print("D - Logout from Gmail")
	print("X - Exit Script (Default)")
	print("__________________________________________________________")
	user_input = input("Enter your step: ")
	method_exec = user_input.strip().upper()
	if method_exec == "A":
		# switch_to_gmail_account(driver)
		switch_to_diff_account(driver, nextEmailCredIndex)
		go_to_step(driver)
	elif method_exec == "B":
		switch_to_linkedin_account(driver, nextLinkedInCredIndex)
		go_to_step(driver)
	elif method_exec == "C":
		logout_from_linkedin(driver)
		go_to_step(driver)
	elif method_exec == "D":
		logout_from_gmail(driver)
		go_to_step(driver)
	elif method_exec == "X":
		driver.close()
		sys.exit()
	else:
		logout_from_gmail(driver)
		logout_from_linkedin(driver)
		driver.close()
		sys.exit()
		# go_to_step(driver)










def add_new_cookie(driver, cookie):
	# Now set the cookie. This one's valid for the entire domain
	driver.add_cookie(cookie)

def delete_cookie(driver, cookie_name):
	driver.delete_cookie(cookie_name)

def delete_all_cookies(driver):
	driver.delete_all_cookies()
	if os.path.exists("cookies.pkl"):
		os.remove("cookies.pkl")
	else:
		print("The cookies file does not exist")

def save_cookies(driver, file_mode='w+'):
	# wb - append to file
	# wb - write to file from start
	try:
		pickle.dump(driver.get_cookies(), open("cookies.pkl", "a+"))
	except Exception as e:
		pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
		pass
	pass


def retreive_driver_cookies(driver, url):
	driver.get(url)
	try:
		cookies = pickle.load(open("cookies.pkl", "rb"))
	except Exception as e:
		fo = open("cookies.pkl", "wb")
		fo.close()
		retreive_driver_cookies(driver, url)
		pass
	for cookie in cookies:
		add_new_cookie(driver, cookie)


def initialize_driver(driver_name):
	if driver_name.upper() == "RESET":
		saveAs = input("Save this new instance as: ")
		if saveAs:
			print("Current instance will be saved as '"+saveAs+"'")
		else:
			print("Current instance will not be saved")
	else:
		openInstance = input("Enter name of previous instance that you want to continue: ")
		# session_id = "9d6e0addbccca60bc50f853b0227cb4a"
		# executor_url = "http://127.0.0.1:47429"
	driver = initialize_new_driver()
	session_id = driver.session_id
	executor_url = driver.command_executor._url
	driver = initialize_remote_driver(session_id, executor_url)
	return driver


# Initialize Remote Driver
def initialize_remote_driver(session_id, executor_url):
	# operating system 
	driver_path = "assets/chrome_driver/chromedriver"
	headless_chromium_path = "/assets/chrome_driver/headless-chromium"

	# Headless Browser
	chrome_options = webdriver.ChromeOptions()

	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
	# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
	chrome_options.add_argument('--single-process')
	chrome_options.binary_location = os.getcwd() + headless_chromium_path

	desired_capabilities = chrome_options.to_capabilities()
	remote_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=desired_capabilities)
	remote_driver.session_id = session_id
	return remote_driver


# Initialize Chrome Driver
def initialize_new_driver():
	# operating system 
	driver_path = "assets/chrome_driver/chromedriver"
	headless_chromium_path = "/assets/chrome_driver/headless-chromium"

	# Headless Browser
	chrome_options = webdriver.ChromeOptions()

	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
	# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
	chrome_options.add_argument('--single-process')
	chrome_options.binary_location = os.getcwd() + headless_chromium_path

	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
	return driver



# Debug Logger
def debug_exception(driver, exception, custom_exception='', content=[]):
	print(exception)
	print(custom_exception)
	logging.info(custom_exception)
	# logging.debug("\n Date& time: "+time.strftime("%b %d %Y %H:%M:%S")+"\n Exception: ")
	# logging.info(exception)
	# logging.debug("\n Custom Exception Message: "+custom_exception+"\n URL: "+driver.current_url+"\n Content: \n"+str(content)+"\n")






def check_login_to_linkedin(driver):
	is_loggedin = False
	try:
		# check if login was successful
		driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
		time.sleep(1)
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
		is_loggedin = True
		return is_loggedin
		# profile_info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-nav-item"]/div'))).get_attribute('innerHTML')
		# if profile_info:
			# is_loggedin = True
	except Exception as e:
		is_loggedin = False
		return is_loggedin
		pass
	return is_loggedin


def check_login_to_gmail(driver):
	is_loggedin = False
	try:
		# check if login was successful
		driver.get("https://accounts.google.com/")
		driver.find_element_by_id('identifierId')
		is_loggedin = False
	except Exception as e:
		is_loggedin = True
		pass
	return is_loggedin



def switch_to_linkedin_account(driver, nextCredIndex=0):
	global linkedin_credentials
	global nextLinkedInCredIndex
	if nextCredIndex >= len(linkedin_credentials):
		nextCredIndex = len(linkedin_credentials)-1
	linkedinUsername = linkedin_credentials[nextCredIndex]['username']
	linkedinPassword = linkedin_credentials[nextCredIndex]['password']
	if check_login_to_linkedin(driver):
		print("Already Logged In to LinkedIn")
		logging.info("Already Logged In to LinkedIn")
	else:
		login_to_linkedin(driver, linkedinUsername, linkedinPassword)
		nextLinkedInCredIndex = nextCredIndex + 1
		time.sleep(0.3)
		try:
			# check if login was successful
			driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
			time.sleep(1)
			confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
			print("LinkedIn login for "+linkedinUsername+" was successful")
			logging.info("LinkedIn login for "+linkedinUsername+" was successful")
		except Exception as e:
			print("LOGIN FAILED")
			print(e)
			print(driver.current_url)
			print("LinkedIn login for "+linkedinUsername+" failed")
			logging.error('Current URL: '+driver.current_url+'\n LinkedIn login for '+linkedinUsername+' failed - ' + str(e))
			# debug_exception(driver, e, "LinkedIn login for "+linkedinUsername+" failed", {'page_html': driver.find_element_by_xpath("//body").get_attribute('innerHTML')})
			pass



def check_for_verification(driver):
	try:
		verify_email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
		verify_email.clear()
		print("Email verification required")
		logging.info("Email verification required for email ID("+username+")")
		user_input = input("Please enter the email verification code sent to the email ID("+username+"): ")
		verify_email.send_keys(user_input)
		confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
		driver.execute_script("arguments[0].click();", confirm)
		pass
	except Exception as e:
		try:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
			print("Recaptcha verification required")
			logging.debug("Recaptcha verification required")
		except Exception as e:
			pass
		pass



# LogIn function for LinkedIn Account
def login_to_linkedin(driver, username, password):
	print("Logging In into linkedIn as "+username)
	try:
		driver.get("https://www.linkedin.com/login")
		user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
		user.clear()
		user.send_keys(username)
		pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
		pwd.clear()
		pwd.send_keys(password)
		# submit_form
		login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
		login.click()
		# check for verification
		check_for_verification(driver)
	except Exception as e:
		print(e)
		print("Page elements were not found")
		print("Current URL : "+driver.current_url)
		logging.error('Current URL: '+driver.current_url+'\n Error - ' + str(e))
		pass


# LogOut function for LinkedIn Account
def logout_from_linkedin(driver):
	if not check_login_to_linkedin(driver):
		print("Need to Login before logging out from LinkedIn")
		logging.info("Need to Login before logging out from LinkedIn")
	else:
		print("Logging out from linkedIn")
		logging.info("Logging out from linkedIn")
		try:
			driver.get("https://www.linkedin.com/notifications/")
			# Logout drop down
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown"]')))
			clk.click()
			# Logout
			logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li/a')))
			logout.click()
			print('LinkedIn logout success')
			logging.info('LinkedIn logout success')
		except Exception as e:
			print(e)
			print(driver.current_url)
			logging.error('Current URL: '+driver.current_url+'\n LinkedIn logout failed - ' + str(e))



# def switch_to_gmail_account(driver, nextCredIndex=0):
# 	global email_credentials
# 	global nextEmailCredIndex
# 	if check_login_to_gmail(driver):
# 		print("Already logged in to Gmail")
# 		logging.info("Already logged in to Gmail")
# 	else:
# 		if nextCredIndex >= len(email_credentials):
# 			nextCredIndex = len(email_credentials)-1
# 		gmailUsername = email_credentials[nextCredIndex]['username']
# 		gmailPassword = email_credentials[nextCredIndex]['password']
# 		login_to_gmail(driver, gmailUsername, gmailPassword)
# 		nextEmailCredIndex = nextCredIndex + 1
# 		time.sleep(3)
# 		try:
# 			# check if login was successful
# 			confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
# 			print("Gmail Log In for "+gmailUsername+" was successful")
# 			logging.info("Gmail Log In for "+gmailUsername+" was successful")
# 		except Exception as e:
# 			print(e)
# 			print(driver.current_url)
# 			print("Gmail login for "+gmailUsername+" failed")
# 			logging.error('Current URL: '+driver.current_url+'\n Gmail login for '+gmailUsername+' failed - ' + str(e))
# 			if nextCredIndex < len(email_credentials):
# 				switch_to_gmail_account(driver, nextCredIndex)
# 			else:
# 				print("No more gmail accounts available")
# 				logging.info("No more gmail accounts available")
		




def switch_to_diff_account(driver, nextCredIndex=0):
	global email_credentials
	global nextEmailCredIndex
	username = email_credentials[nextCredIndex]['username']
	password = email_credentials[nextCredIndex]['password']
	if re.search("yahoo", username):
		try:
			login_to_yahoo(driver, username, password)
			# check if login was successful
			driver.get("https://login.yahoo.com/account/")
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			driver.execute_script("arguments[0].click();", clk)
			time.sleep(1)
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
			print("Yahoo Log In for "+username+" was successful")
		except Exception as e:
			print(e)
			print("Yahoo Login for "+username+" failed")
			logging.debug("Yahoo Login for "+username+" failed")
		try:
			# import_contacts
			# import_contacts(driver, username, "yahoo")
			# contactDataList = export_contacts(driver)
			# export_contacts_to_db(contactDataList)
			logout_from_yahoo(driver)
			# remove_synced_accounts(driver)
		except Exception as e:
			print(e)
			pass
	elif re.search("aol", username):
		try:
			login_to_aol(driver, username, password)
			# check if login was successful
			driver.get("https://login.aol.com/account/")
			# driver.find_element_by_xpath('//*[@id="navigation-menu-user-account"]/div/a[2]')
			print("AOL Log In for "+username+" was successful")
		except Exception as e:
			print(e)
			print("AOL Login for "+username+" failed")
			logging.debug("AOL Login for "+username+" failed")
		try:
			# import_contacts
			# import_contacts(driver, username, "aol")
			# contactDataList = export_contacts(driver)
			# export_contacts_to_db(contactDataList)
			logout_from_aol(driver)
			# remove_synced_accounts(driver)
		except Exception as e:
			print(e)
			pass
	else:
		try:
			login_to_gmail(driver, username, password)
			# check if login was successful
			confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
			print("Gmail Log In for "+username+" was successful")
			logging.debug("Gmail Log In for "+username+" was successful")
		except Exception as e:
			print(e)
			print("Gmail Login for "+username+" failed")
			logging.debug("Gmail Login for "+username+" failed")
		try:
			# import_contacts
			# import_contacts(driver, username, "gmail")
			# contactDataList = export_contacts(driver)
			# export_contacts_to_db(contactDataList)
			logout_from_gmail(driver)
			# remove_synced_accounts(driver)
		except Exception as e:
			print(e)
			pass
	check_for_account_in_outlook(driver, username, password)

# Check if email ID has outlook account
def check_for_account_in_outlook(driver, username, password):
	try:
		login_to_outlook(driver, username, password)
		# check if login was successful
		driver.get("https://account.microsoft.com/")
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mectrl_body_signOut')))
		print("OutLook Log In for "+username+" was successful")
		# # import_contacts
		# import_contacts(driver, username, "outlook")
		# contactDataList = export_contacts(driver)
		# export_contacts_to_db(contactDataList)
		logout_from_outlook(driver)
		# remove_synced_accounts(driver)
	except Exception as e:
		# print(e)
		print("Microsoft Outlook account may not be present for "+username)


# LogIn function for Yahoo Account
def login_to_yahoo(driver, username, password):
	print("Logging In into Yahoo as "+username)
	try:
		driver.get("https://login.yahoo.com/account")
		user = driver.find_element_by_id('login-username')
		user.clear()
		user.send_keys(username)
		# driver.find_element_by_id("persistent").send_keys('y')
		driver.find_element_by_id("login-signin").click()
		time.sleep(5)
		pwd = driver.find_element_by_id("login-passwd")
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = driver.find_element_by_id("login-signin")
		login.click()
		time.sleep(2)
	except Exception as e:
		print(e)
		print("Page elements were not found")
		logging.debug("Page elements were not found")
	# driver.save_screenshot("2.png")


# LogOut function for Yahoo Account
def logout_from_yahoo(driver):
	print("Logging out from Yahoo")
	try:
		driver.get("https://login.yahoo.com/account/")
		# Logout drop down
		# clk = driver.find_element_by_id("ybarAccountMenu")
		clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
		driver.execute_script("arguments[0].click();", clk)
		# Logout
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a[3]')))
		logout.click()
	except Exception as e:
		print(e)


# LogIn function for OutLook Account
def login_to_outlook(driver, username, password):
	try:
		driver.get("https://login.live.com/")
		time.sleep(2)
		user = driver.find_element_by_id('i0116')
		user.clear()
		user.send_keys(username)
		driver.find_element_by_id("idSIButton9").click()
		time.sleep(2)
		try:
			txt = driver.find_element_by_id("usernameError").text
			print(txt)
		except Exception as e:
			print("Logging In into OutLook as "+username)
			pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="i0118"]')))
			pwd.send_keys(password)
			# form submit
			# pwd.send_keys(Keys.RETURN)
			login = driver.find_element_by_id("idSIButton9")
			login.click()
		time.sleep(2)
	except Exception as e:
		print(e)
		print("Page elements were not found")
		logging.debug("Page elements were not found")
	# driver.save_screenshot("2.png")


# LogOut function for Gmail Account
def logout_from_outlook(driver):
	try:
		driver.get("https://account.microsoft.com/")
		time.sleep(2)
		# Logout drop down
		# clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mectrl_headerPicture')))
		clk = driver.find_element_by_id("mectrl_headerPicture")
		clk.click()
		# Logout
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'mectrl_body_signOut')))
		print("loggging out from Microsoft OutLook")
		# logout = driver.find_element_by_id("mectrl_body_signOut")
		logout.click()
		time.sleep(2)
	except Exception as e:
		pass


# LogIn function for AOL Account
def login_to_aol(driver, username, password):
	print("Logging In into AOL as "+username)
	try:
		driver.get("https://login.aol.com/")
		time.sleep(2)
		user = driver.find_element_by_id('login-username')
		user.clear()
		user.send_keys(username)
		driver.find_element_by_id("login-signin").click()
		time.sleep(1)
		try:
			# Not a Robot
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')))
			driver.execute_script("arguments[0].click();", clk)
			# driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[1]').click()
			time.sleep(5)
			driver.find_element_by_xpath('//*[@id="recaptcha-submit"]').click()
			# clk2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "recaptcha-submit")))
			# driver.execute_script("arguments[0].click();", clk2)
		except Exception as e:
			print("Validated: Not a Robot")
			pass
		time.sleep(3)
		pwd = driver.find_element_by_id('login-passwd')
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = driver.find_element_by_id("login-signin")
		login.click()
		time.sleep(2)
	except Exception as e:
		print(e)
		print("Page elements were not found")
		logging.debug("Page elements were not found")
	# driver.save_screenshot("2.png")


# LogOut function for Gmail Account
def logout_from_aol(driver):
	print("Logging out from AOL")
	try:
		driver.get("https://login.aol.com/account/")
		# # Logout drop down
		# # clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ybarAccountMenu')))
		# clk = driver.find_element_by_id("ybarAccountMenu")
		# clk.click()
		# Logout
		# logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a')))
		logout = driver.find_element_by_xpath('//*[@id="navigation-menu-user-account"]/div/a[2]')
		logout.click()
		time.sleep(2)
	except Exception as e:
		print(e)


# LogIn function for Gmail Account
def login_to_gmail(driver, username, password):
	print("Logging In into Gmail as "+username)
	time.sleep(1)
	try:
		driver.get("https://accounts.google.com/signin/v2")
		driver.find_element_by_id('identifierId').send_keys(username)
		driver.find_element_by_id("identifierNext").click()
		time.sleep(5)
		pwd = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
		pwd.send_keys(password)
		# form submit
		# pwd.send_keys(Keys.RETURN)
		login = driver.find_element_by_id("passwordNext")
		login.click()
		try:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
			print("Recaptcha verification required")
			logging.debug("Recaptcha verification required")
			# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
			# print("Email verification required")
			pass
		except Exception as e:
			pass
	except Exception as e:
		logging.error('Current URL: '+driver.current_url+'\n Error - ' + str(e))
		print("Page elements were not found")


# LogOut function for Gmail Account
def logout_from_gmail(driver):
	if not check_login_to_gmail(driver):
		print("Need to Login before logging out from Gmail")
		logging.info("Need to Login before logging out from Gmail")
	else:
		print("Logging out from Gmail")
		logging.info("Logging out from Gmail")
		# try:
		# 	# driver.get("https://accounts.google.com/")
		# 	# # Logout drop down
		# 	# clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
		# 	# clk.click()
		# 	# # Logout
		# 	# logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "gb_71")))
		# 	# logout.click()
		# 	print('Gmail logout success')
		# 	logging.info('Gmail logout success')
		# except Exception as e:
		# 	print(e)
		# 	logging.error('Current URL: '+driver.current_url+'\n Gmail logout failed - ' + str(e))
		driver.get("https://www.google.com/accounts/Logout")
	# remove previously loggedin accounts
	remove_previous_loggedin_gmail_accounts(driver)
		

def remove_previous_loggedin_gmail_accounts(driver):
	try:
		driver.get("http://accounts.google.com/ServiceLogin/signinchooser")
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]')))
		removeAccounttClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[3]')))
		removeAccounttClk.click()
		selectClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/ul/li[1]')))
		selectClk.click()
		# //*[@id="yDmH0d"]/div[5]/div/div[2]/div[3]/div[1]
		removeClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[5]/div/div[2]/div[3]/div[1]')))
		driver.execute_script("arguments[0].click();", removeClk)
		# removeClk.click()
		time.sleep(3)
		print("Removed the account from browser")
	except Exception as e:
		pass





# Import contacts from Gmail to LinkedIn
def import_contacts(driver, username, account_tag):
	print("Importing contacts from account("+username+")")
	global linkedin_credentials
	driver.get("https://www.linkedin.com/mynetwork/import-contacts/")	
	time.sleep(3)

	try:
		if account_tag.strip().lower() == 'aol':
			# AOL = #oauth2-agree
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember63"]/a')))
			clk.click()
			time.sleep(3)
			if len(driver.window_handles) > 1:
				# switch the pop-up window
				driver.switch_to.window(driver.window_handles[1])
				time.sleep(5)
				# Check if any account needs to be selected
				confirmAccount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oauth2-agree')))
				driver.execute_script("arguments[0].click();", confirmAccount)
		elif account_tag.strip().lower() == 'outlook':
			# OutLook = #idBtn_Accept
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember58"]/a')))
			clk.click()
			time.sleep(3)
			if len(driver.window_handles) > 1:
				# switch the pop-up window
				driver.switch_to.window(driver.window_handles[1])
				time.sleep(5)
				# Check if any account needs to be selected
				confirmAccount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'idBtn_Accept')))
				driver.execute_script("arguments[0].click();", confirmAccount)
		elif account_tag.strip().lower() == 'yahoo':
			# yahoo = #oauth2-agree
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember53"]/a')))
			clk.click()
			time.sleep(3)
			if len(driver.window_handles) > 1:
				# switch the pop-up window
				driver.switch_to.window(driver.window_handles[1])
				time.sleep(5)
				# Check if any account needs to be selected
				confirmAccount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'oauth2-agree')))
				driver.execute_script("arguments[0].click();", confirmAccount)
		else:
			clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ember48"]/a')))
			clk.click()
			time.sleep(3)
			if len(driver.window_handles) > 1:
				# switch the pop-up window
				driver.switch_to.window(driver.window_handles[1])
				time.sleep(5)
				# Check if any account needs to be selected
				accountSelector = '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[1]'
				account = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, accountSelector)))
				account.click()
				confirmAccount = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'submit_approve_access')))
				# confirmAccount.click()
				driver.execute_script("arguments[0].click();", confirmAccount)
		
		#switch back to original window
		time.sleep(0.5)
		if len(driver.window_handles) > 1:
			try:
				backToPrevWindow = WebDriverWait(driver.window_handles[1], 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="minimal-util-nav"]/ul/li[1]/a')))
				backToPrevWindow.click()
			except Exception as e:
				if len(driver.window_handles) > 1:
					driver.close()
				print("return to LinkedIn")
	except Exception as e:
		print(e)

	driver.switch_to.window(driver.window_handles[0])

	try:
		time.sleep(3)
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contact-select-checkbox"]')))
		print("Contacts imported from account["+username+"] to LinkedIn")
	except Exception as e:
		print(e)
		print("Error in importing contacts from account["+username+"]") 
		continueExec = get_user_input("continue execution with same LinkedIn Account (Default:No)? (y/n) ", 'n')
		if continueExec.strip().lower() == 'n' and nextLinkedInCredIndex < len(linkedin_credentials):
			logout_from_linkedin(driver)
			select_different_linked_in_account(nextLinkedInCredIndex)
		else:
			print("continuing with same linkedIn account for remaining accounts sync..")


# Remove previous synced gmail accounts
def remove_synced_accounts(driver):
	driver.get("https://www.linkedin.com/mynetwork/settings/manage-syncing/")
	time.sleep(5)
	try:
		removeAllClk = driver.find_element_by_xpath('//*[@id="ember44"]/div[1]/button')
		removeAllClk.click()
		rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button'
		rmvClk2 = driver.find_element_by_xpath(rmvclk2Selector)
		rmvClk2.click()
	except Exception as e:
		print(e)
		try:
			listResults = driver.find_elements_by_xpath('//*[@id="ember42"]/section/ul/div') # //ul[@class="list-style-none.mh5"]/div
			for account in listResults or []:
				rmvClk = account.find_element_by_xpath('.//li/div/button')
				driver.execute_script("arguments[0].click();", rmvClk)
				rmvclk2Selector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/ul/li[2]/button[@class="js-mn-manage-source-confirm"]'
				rmvClk2 = driver.find_element_by_xpath(rmvclk2Selector)
				driver.execute_script("arguments[0].click();", rmvClk2)
		except Exception as e:
			# print(e)
			# print("Removal of synced failed")
			pass
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



def sendMessageToSQSQueue(queue_url, region_name, message_attributes, message_body):
	# User queue-admin
	# Key AKIAWSTJLD4BSX6ABMTC
	# SAK r9r+dnYFkn0ZdQZbiAe28u1g5BNavYVckIgm43F0

	# Create SQS client
	sqs = boto3.client('sqs', region_name=region_name)
	# Send message to SQS queue
	response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=10,
    MessageAttributes=message_attributes,
    MessageBody=message_body,
	)

  # # Example below;
  # MessageAttributes={
  #     'Title': {
  #         'DataType': 'String',
  #         'StringValue': 'The Whistler'
  #     },
  #     'Author': {
  #         'DataType': 'String',
  #         'StringValue': 'John Grisham'
  #     },
  #     'WeeksOn': {
  #         'DataType': 'Number',
  #         'StringValue': '6'
  #     }
  # },
  # MessageBody=(
  #     'Information about current NY Times fiction bestseller for '
  #     'week of 12/11/2016.'
  # )

	print("Sent Message ID: "+response['MessageId'])
	return response['MessageId']


def receiveMessageFromSQSQueue(queue_url, region_name, attributes=["All"], message_attributes=["All"]):
	# Create SQS client
	sqs = boto3.client('sqs', region_name=region_name)
	# Receive message from SQS queue
	response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=attributes,
    MaxNumberOfMessages=1,
    MessageAttributeNames=message_attributes,
    VisibilityTimeout=0,
    WaitTimeSeconds=0
	)

	try:
		messages = response['Messages']
	except Exception as e:
		messages = []
		pass
	return messages


def deleteMessageFromSQSQueue(queue_url, region_name, receipt_handle):
	# Create SQS client
	sqs = boto3.client('sqs', region_name=region_name)
	try:
		# Delete received message from queue
		sqs.delete_message(
		    QueueUrl=queue_url,
		    ReceiptHandle=receipt_handle
		)
		print('Message with handle('+receipt_handle+'), deleted from SQS Queue('+queue_url+')')
	except Exception as e:
		print(e)
		print('Unable to delete message from queue('+queue_url+' : '+receipt_handle+')')




# recaptcha-anchor
# recaptcha-token
# recaptcha-verify-button




lambda_handler(None, None)


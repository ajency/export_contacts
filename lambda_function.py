import json
import boto3
import signal
import socket    
import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


email_credentials = [
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	# {"username": "stinfordpaulie18@yahoo.com", "password": "ajency#123"},		#microsoft outlook & yahoo
	# {"username": "stinfordpaulie18@aol.com", "password": "ajency#123"},			#aol
	# {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},			#gmail
]

linkedin_credentials = [
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	# {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
	# {"username": "ralph110293@gmail.com", "password": "ajency#123"},
]

def lambda_handler(event, context):
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	print("Your Computer Name is:" + hostname)    
	print("Your Computer IP Address is:" + IPAddr) 

	# Program Execution
	driver = initialize_driver()
	print("Running in Headless browser mode..")

	switch_to_gmail_account(driver)
	switch_to_linkedin_account(driver)

	logout_from_linkedin(driver)
	logout_from_gmail(driver)
	# # import_contacts
	# import_contacts(driver, gmailUsername)
	print("Execution Completed")
	# End Driver
	driver.close()
	sys.exit()



# def select_different_linked_in_account(nextLinkedInCredIndex):
# 	driver = initialize_driver()
# 	# driver = webdriver.Chrome(executable_path=driver_path)
# 	hostname = socket.gethostname()
# 	IPAddr = socket.gethostbyname(hostname)
# 	print("Your Computer Name is:" + hostname)    
# 	print("Your Computer IP Address is:" + IPAddr) 
# 	# Program Execution
# 	print("Running in Headless browser mode..")

# 	switch_to_linkedin_account(driver)
# 	switch_to_gmail_account(driver)

# 	logout_from_linkedin(driver)
# 	logout_from_gmail(driver)


# Initialize Driver & login into LinkedIn
def initialize_driver():
	global driver
	# operating system 
	driver_path = "assets/chrome_driver/chromedriver"
	headless_chromium_path = "/assets/chrome_driver/headless-chromium"

	# PROXY = "127.0.1.1:8000"
	# PROXY = "88.157.149.250:8080"

	# Headless Browser
	chrome_options = webdriver.ChromeOptions()

	# chrome_options.add_argument('--proxy-server=%s' % PROXY)

	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
	# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
	chrome_options.add_argument('--single-process')
	chrome_options.binary_location = os.getcwd() + headless_chromium_path

	# return webdriver.Chrome(executable_path=driver_path)
	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
	return driver






def switch_to_linkedin_account(driver, nextCredIndex=0):
	global email_credentials
	global linkedin_credentials
	global nextEmailCredIndex
	global nextLinkedInCredIndex
	linkedinUsername = linkedin_credentials[nextCredIndex]['username']
	linkedinPassword = linkedin_credentials[nextCredIndex]['password']

	login_to_linkedin(driver, linkedinUsername, linkedinPassword)
	nextLinkedInCredIndex = nextCredIndex + 1
	isLinkedInLoggedIn = False
	time.sleep(0.3)
	try:
		# check if login was successful
		driver.get("https://www.linkedin.com/mynetwork/import-contacts/")
		time.sleep(1)
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
		print("LinkedIn login for "+linkedinUsername+" was successful")
		isLinkedInLoggedIn = True
	except Exception as e:
		print("LOGIN FAILED")
		print(e)
		print(driver.current_url)
		print("LinkedIn login for "+linkedinUsername+" failed")
		isLinkedInLoggedIn = False
		if nextLinkedInCredIndex < len(linkedin_credentials):
			switch_to_linkedin_account(driver, nextLinkedInCredIndex)
			# select_different_linked_in_account(nextLinkedInCredIndex)
		else:
			print("No more linkedIn accounts available")
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
		try:
			verify_email = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
			print("Email verification required")
			verify_email.clear()
			user_input = raw_input("Please enter the email verification code sent to the email ID")
			verify_email.send_keys(user_input)
			confirm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'email-pin-submit-button')))
			driver.execute_script("arguments[0].click();", confirm)
			pass
		except Exception as e:
			try:
				WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
				print("Recaptcha verification required")
				pass
			except Exception as e:
				print("Logged In")
				pass
			pass
	except Exception as e:
		print(e)
		print("Current URL : "+driver.current_url)
		payload = {
			"driver": driver,
			"exception": e,
			"redirected_url": driver.current_url,
			"request_data": {
				"linkedinUsername": username,
				"linkedinPassword": password,
			},
		}
		print("Page elements were not found")
		pass


# LogOut function for LinkedIn Account
def logout_from_linkedin(driver):
	print("Logging out from linkedIn")
	try:
		driver.get("https://www.linkedin.com/notifications/")
		# Logout drop down
		clk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown"]')))
		clk.click()
		# Logout
		logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li/a')))
		logout.click()
	except Exception as e:
		print("LOGOUT EXCEPTION")
		print(e)
		print(driver.current_url)



def switch_to_gmail_account(driver, nextCredIndex=0):
	global email_credentials
	gmailUsername = email_credentials[nextCredIndex]['username']
	gmailPassword = email_credentials[nextCredIndex]['password']
	login_to_gmail(driver, gmailUsername, gmailPassword)
	nextCredIndex += 1
	time.sleep(3)
	try:
		# check if login was successful
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div/div[2]/div/a')))
		print("Gmail Log In for "+gmailUsername+" was successful")
	except Exception as e:
		print(e)
		print(driver.current_url)
		print("Gmail login for "+gmailUsername+" failed")
		if nextCredIndex < len(email_credentials):
			switch_to_gmail_account(driver, nextCredIndex)
		else:
			print("No more gmail accounts available")
		


# LogIn function for Gmail Account
def login_to_gmail(driver, username, password):
	print("Logging In into Gmail as "+username)
	time.sleep(1)
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
		try:
			WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'recaptcha-anchor')))
			print("Recaptcha verification required")
			# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'input__email_verification_pin')))
			# print("Email verification required")
			pass
		except Exception as e:
			pass
	except Exception as e:
		print("Page elements were not found")
		


# recaptcha-anchor
# recaptcha-token
# recaptcha-verify-button



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
		# try:
		# 	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]')))
		# 	removeAccounttClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[3]')))
		# 	removeAccounttClk.click()
		# 	selectClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/ul/li[1]')))
		# 	selectClk.click()
		# 	removeClk = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[1]/span')))
		# 	removeClk.click()
		# 	time.sleep(3)
		# 	print("Remove the account from browser")
		# except Exception as e:
		# 	pass
	except Exception as e:
		print(e)




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




#span attr('email') security-noreply@linkedin.com
# class="h7 bg ie"
# //*[@id=":d3"]/div[1]/table/tbody/tr/td/center/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[3]/td/p/strong
lambda_handler(None, None)
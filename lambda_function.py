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


nextEmailCredIndex = 0
nextLinkedInCredIndex = 0
email_credentials = [
	{"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	{"username": "stinfordpaulie18@yahoo.com", "password": "ajency#123"},		#microsoft outlook & yahoo
	{"username": "stinfordpaulie18@aol.com", "password": "ajency#123"},			#aol
	{"username": "alina.jose1102@gmail.com", "password": "ajency#123"},			#gmail
]

linkedin_credentials = [
	# {"username": "pnitin3103@gmail.com", "password": "ajency#123"},
	# {"username": "alina.jose1102@gmail.com", "password": "ajency#123"},
	{"username": "ralph110293@gmail.com", "password": "ajency#123"},
]

def lambda_handler(event, context):
	global email_credentials
	global linkedin_credentials
	global nextLinkedInCredIndex

	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	print("Your Computer Name is:" + hostname)    
	print("Your Computer IP Address is:" + IPAddr) 
	# Program Execution
	print("Running in Headless browser mode..")
	select_different_linked_in_account(nextLinkedInCredIndex)

	print("Reading message from Queue..")
	print(receiveMessageFromSQSQueue("https://sqs.us-east-1.amazonaws.com/452266237699/process-queue", "us-east-1"))

	print("Execution Completed")
	sys.exit()



# Initialize Driver & login into LinkedIn
def select_different_linked_in_account(nextLinkedInCredIndex):
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

	# chrome_options.add_argument('--window-size=1280x1696')
	# chrome_options.add_argument('--user-data-dir=/tmp/user-data')
	# chrome_options.add_argument('--hide-scrollbars')
	# chrome_options.add_argument('--enable-logging')
	# chrome_options.add_argument('--log-level=0')
	# chrome_options.add_argument('--v=99')
	# chrome_options.add_argument('--data-path=/tmp/data-path')
	# chrome_options.add_argument('--ignore-certificate-errors')
	# chrome_options.add_argument('--homedir=/tmp')
	# chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')

	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
	# driver = webdriver.Chrome(executable_path=driver_path)

	switch_to_linkedin_account(driver, nextLinkedInCredIndex)
	logout_from_linkedin(driver)




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
		time.sleep(2)
		confirmLogIn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]/div/li-icon')))
		print("LinkedIn login for "+linkedinUsername+" was successful")
		isLinkedInLoggedIn = True
	except Exception as e:
		print("LOGIN FAILED")
		print(e)
		print(driver.current_url)
		print("LinkedIn login for "+linkedinUsername+" failed")
		isLinkedInLoggedIn = False
		payload = {
			"driver": driver,
			"exception": e,
			"redirected_url": driver.current_url,
			"request_data": {
				"linkedinUsername": linkedinUsername,
				"linkedinPassword": linkedinPassword,
			},
		}
		if nextLinkedInCredIndex < len(linkedin_credentials):
			select_different_linked_in_account(nextLinkedInCredIndex)
		else:
			print("No more linkedIn accounts available")

	try:
		while isLinkedInLoggedIn and nextEmailCredIndex < len(email_credentials):
			print(email_credentials[nextEmailCredIndex]['username'])
			# switch_to_diff_account(driver, nextEmailCredIndex)
			nextEmailCredIndex += 1
	except Exception as e:
		print(driver.current_url)
		print(e)
		payload = {
			"driver": driver,
			"exception": e,
			"redirected_url": driver.current_url,
			"request_data": {
				"emailUsername": email_credentials[nextEmailCredIndex]['username'],
				"emailPassword": email_credentials[nextEmailCredIndex]['password'],
				"linkedinUsername": linkedinUsername,
				"linkedinPassword": linkedinPassword,
			},
		}
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
		print(driver.current_url)
		logged_in = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'nav-settings__dropdown-trigger')))
		print("LOGIN SUCCESS - no error")
	except Exception as e:
		print("LOGIN EXCEPTION")
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



# def debugger(driver):
# 	print(driver.current_url)
# 	driver.save_screenshot("screenshot_temp.png")
# 	s3 = boto3.client('s3')
# 	s3.create_bucket(Bucket='testbuckethp3pytest')
# 	# s3.upload_file('screenshot_temp.png', 'testbuckethp3pytest', 'screenshot_temp.png')
# 	s3.Bucket('exportlinkedincontacts').put_object(Key='screenshot.png', Body=driver.save_screenshot("screenshot_temp.png"))


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
		payload = {
			"driver": driver,
			"exception": e,
			"redirected_url": driver.current_url,
			"request_data": [],
		}
		print("LOGOUT EXCEPTION")
		print(e)
		print(driver.current_url)
	# End Driver
	driver.close()



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





lambda_handler(None, None)
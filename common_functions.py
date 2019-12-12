import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def initialize_driver():
	# operating system [Linux]
	driver_path = "assets/chrome_driver/chromedriver"
	headless_chromium_path = "/assets/chrome_driver/headless-chromium"

	# Headless Browser
	chrome_options = webdriver.ChromeOptions()

	# PROXY = "127.0.1.1:8000"
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

	chrome_options.add_argument('--window-size=1280x1696')
	chrome_options.add_argument('--user-data-dir=/tmp/user-data')
	chrome_options.add_argument('--hide-scrollbars')
	chrome_options.add_argument('--enable-logging')
	chrome_options.add_argument('--log-level=0')
	chrome_options.add_argument('--v=99')
	chrome_options.add_argument('--data-path=/tmp/data-path')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--homedir=/tmp')
	chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')

	driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
	return driver


def find_element_by_id_with_timeout(driver, element_path, request_data=[], timeout=0):
	payload = {
		"driver": driver,
		"success": True,
		"exception": "",
		"current_url": driver.current_url,
		"request_data": request_data,
	}
	try:
		if timeout > 0:
			elementFound = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element_path)))
		else:
			elementFound = driver.find_elements_by_id(element_path)
		payload.exception = "Element for path "+element_path+" was found",
	except Exception as e:
		elementFound = None
		payload.success = False,
		payload.exception = e.message or "Element for path "+element_path+" not found",
		pass
	log(payload)
	return [elementFound, payload]


def find_element_by_xpath_with_timeout(driver, element_path, request_data=[], timeout=0):
	payload = {
		"driver": driver,
		"success": True,
		"exception": "",
		"current_url": driver.current_url,
		"request_data": request_data,
	}
	try:
		if timeout > 0:
			elementFound = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_path)))
		else:
			elementFound = driver.find_elements_by_xpath(element_path)
		payload.exception = "Element for path "+element_path+" was found",
	except Exception as e:
		elementFound = None
		payload.success = False,
		payload.exception = e.message or "Element for path "+element_path+" not found",
		pass
	log(payload)
	return [elementFound, payload]



def log(log_data):
	# payload = {
	# 	"driver": driver,
	# 	"exception": e.message,
	# 	"current_url": driver.current_url,
	# 	"request_data": [],
	# }
	print(log_data)
	pass
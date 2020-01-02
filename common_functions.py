import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

max_waiting_time = 240		# time in seconds (approx.)

def search_element_by_xpath(driver, element_path):
	try:
		elementFound = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element_path)))
		return True
	except Exception as e:
		return False

def search_element_by_id(driver, element_path):
	try:
		elementFound = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_path)))
		return True
	except Exception as e:
		return False


def search_element_by_css_selector(driver, selector):
	try:
		elementFound = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
		return True
	except Exception as e:
		return False


def search_element_by_css_selector(driver, element_path):
	try:
		elementFound = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_path)))
		return True
	except Exception as e:
		return False

def pause_execution(element_object):
	# SET False to pause execution
	element_object.continue_execution = False

def continue_execution(element_object):
	# SET True to continue execution
	element_object.continue_execution = True

def wait_until_continue_is_true(element_object):
	# wait until element_object.continue_execution = True
	custom_wait_until_continue_is_true(element_object, max_waiting_time)

def custom_wait_until_continue_is_true(element_object, waiting_time):
	# wait until element_object.continue_execution = True OR custom waiting time as passed
	waiting_time = int(waiting_time)
	while not element_object.continue_execution or waiting_time > 0:
		time.sleep(0.98)
		waiting_time = waiting_time - 1
		custom_wait_until_continue_is_true(element_object, waiting_time)
		pass
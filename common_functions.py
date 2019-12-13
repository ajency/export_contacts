import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

max_waiting_time = 240

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


def search_element_by_css_selector(driver, element_path):
	try:
		elementFound = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_path)))
		return True
	except Exception as e:
		return False

# custom execution halt
def custom_pause_execution(element_object):
	element_object.continue_execution = False

def custom_continue_execution(element_object):
	element_object.continue_execution = True

def custom_wait_until_continue_is_true(element_object):
	wait_until_element(element_object, max_waiting_time)

def wait_until_element(element_object, waiting_time):
	waiting_time = int(waiting_time)
	while not element_object.continue_execution or waiting_time > 0:
		time.sleep(1)
		waiting_time = waiting_time - 1
		wait_until_element(element_object, waiting_time)
		pass
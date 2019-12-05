import os,sys,time,csv,datetime,platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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


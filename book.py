# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO,send, emit
import socket
import time
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

#from pyvirtualdisplay import Display

from settings import USER_AGENT_LIST
import random
import json

from PIL import Image
from pytesseract import image_to_string
import re

import cv2

import urllib.request,io

# display = Display(visible=0, size=(1024, 768))
# display.start()

wdriver = ""
username = "rabiwebpro"
password = "kanoon3"

original_image_path = "/srv/http/ENV3/flask_websockets/banner.png"

train_no = "13104"
from_station = "JIAGANJ - JJG"
to_station = "SEALDAH - SDAH"
journey_date = "17-10-2017"
ticket_class = "2S"
ticket_quota = "GN"
ticket_type = "E_TICKET"


def getChromeDriver(headless=True):
    user_agent = random.choice(USER_AGENT_LIST)
    #driver_path = app.root_path+'/chromedriver'
    driver_path = '/srv/http/ENV3/flask_websockets/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--no-referrers')
    #options.add_argument('--user-agent={user_agent}')
    options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")
    #options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def getFirefoxDriver():
    user_agent = random.choice(USER_AGENT_LIST)
    driver_path = '/srv/http/ENV3/flask_websockets/geckodriver'

    # binary = FirefoxBinary('/usr/lib/firefox/firefox')
    # driver = webdriver.Firefox(executable_path=driver_path,firefox_binary=binary)

    caps = webdriver.DesiredCapabilities.FIREFOX
    caps["marionette"] = False
    driver = webdriver.Firefox(capabilities=caps)

    #driver = webdriver.Firefox(executable_path=driver_path)
    driver.wait = WebDriverWait(driver, 15)
    return driver


def login(driver):
    #alternate captcha id: nlpCaptchaImg (308/150) ##
    #alternate2, id: captchadiv
    login_captcha_img = driver.wait.until(EC.presence_of_element_located((By.ID, "captchaImg")))
    login_captcha_src = login_captcha_img.get_attribute("src")

    #new_cap = driver.find_element_by_id("cimage")
    # loc  = new_cap.location
    # size = new_cap.size
    # left  = loc['x']
    # top   = loc['y']
    # width = size['width']
    # height = size['height']
    # box = (int(left), int(top), int(left+width), int(top+height))
    # screenshot = driver.get_screenshot_as_base64()
    # newcaptcha_img = Image.open(io.BytesIO(base64.b64decode(screenshot)))
    # area = newcaptcha_img.crop(box)
    # area.save("banner_final.png",quality=100)

    original_image_data = io.BytesIO(urllib.request.urlopen(login_captcha_src).read())
    img1 = Image.open(original_image_data)
    img1 = img1.resize((616,40),Image.ANTIALIAS)
    img1.save("banner.png",quality=100)


    img = cv2.imread(original_image_path, 0)
    ret, thresh = cv2.threshold(img, 10, 255, cv2.THRESH_OTSU)
    cv2.imwrite("./banner_final.png", thresh)

    extracted_txt = image_to_string(Image.open("/srv/http/ENV3/flask_websockets/banner_final.png"))
    captcha_part = extracted_txt.split(":",1)[1]
    captcha = re.sub(' ','',captcha_part).upper()
    #print(captcha.upper())
    #captcha = "MJYsdfUTH"

    username_input = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".loginUserId")))
    password_input = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".loginPassword")))
    captcha_input = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nlpAnswer")))
    username_input.send_keys(username)
    password_input.send_keys(password)
    captcha_input.send_keys(captcha)

    # display.stop()

    time.sleep(1)
    driver.find_element_by_id("loginbutton").click()


    try:
        quick_book_tab = driver.wait.until(EC.presence_of_element_located((By.ID, "quickbookTab:header:inactive")))
        quick_book_tab.click()
    except:
        errorokbtn = driver.find_element_by_id('loginerrorpanelok')
        if errorokbtn.is_displayed():
            errorokbtn.click()
            login(driver)
        else:
            pass
    #
    #
    #
    # train_no_input = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:trainNUmber")))
    # train_no_input.send_keys(train_no)
    #
    # #time.sleep(3)
    #
    # from_station_input = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:fromStation")))
    # from_station_input.send_keys(from_station)
    #
    # #time.sleep(3)
    #
    # to_station_input = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:toStation")))
    # to_station_input.send_keys(to_station)
    #
    # journey_date_input = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:qbJrnyDateInputDate")))
    # journey_date_input.send_keys(journey_date)
    #
    # #time.sleep(3)
    #
    # ticket_class_select = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:class")))
    # Select(ticket_class_select).select_by_value(ticket_class)
    #
    # #time.sleep(3)
    #
    # ticket_quota_select = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:quota")))
    # Select(ticket_quota_select).select_by_value(ticket_quota)
    #
    # #time.sleep(3)
    #
    # ticket_type_select = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:ticketType")))
    # Select(ticket_type_select).select_by_value(ticket_type)
    #
    # #time.sleep(5)
    #
    # quick_book_submit = driver.wait.until(EC.presence_of_element_located((By.ID, "qbform:quickBookSubmit")))
    # quick_book_submit.click()




if __name__ == '__main__':
    hostname = "http://irctc.co.in"
    driver = getChromeDriver(False)
    #driver = getFirefoxDriver()
    driver.get(hostname)
    login(driver)

from logger import CustomLogger
from screenshot import Screenshot
from os import environ
from credential_parser import CredentialParser

from sequence import get_gamail_login_sequences


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from settings import USER_AGENT_LIST, GMAIL_CREDENTIALS
import random
from pathlib import Path
import time

class Exporter():
    def __init__(self, env, auto, headless, socketio):
        self.env = env
        self.data_source = environ.get('EXPORTER_DATA_SOURCE')
        self.auto = auto
        logger = CustomLogger()
        self.logger = logger
        self.driver = self.initiate_web_driver(headless)
        self.current_gmail_index = 0
        self.socketio = socketio
        self.session_id = time.strftime("%Y%m%d-%H%M%S")
        self.screenshot = Screenshot(self.session_id, self.driver)

    def initiate_web_driver(self, headless=True):
        import platform
        if platform.system() == 'Darwin':
            self.logger.info("Operating System is Mac")
            driver_path = Path('.') / 'webdriver/mac/chromedriver'
        else:
            self.logger.info("Operating System is Linux")
            driver_path = Path('.') / 'webdriver/linux/chromedriver'

        user_agent = random.choice(USER_AGENT_LIST)
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument('--no-referrers')
        options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")

        if headless:
            self.logger.info("Initializing web driver in headless mode true")
            options.add_argument('--headless')
            options.add_argument('--user-agent={'+user_agent+'}')

        driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)
        driver.wait = WebDriverWait(driver, 10)
        return driver

    def close_web_driver(self):
        self.driver.quit()

    def sequence_login_linkedIn(self):
        self.logger.info("LinkedIn login operation started for " + self.env)
        self.linkedIn_credentials = self.get_credentials('linkedin')
        print(self.linkedIn_credentials)

    def sequence_login_gmail(self):
        self.logger.info("Gmail login operation started for " + self.env)
        self.gmail_credentials = self.get_credentials('gmail')
        if len(self.gmail_credentials) > 0:
            current_index = self.current_gmail_index
            if self.current_gmail_index > 0:
                ++current_index

            if current_index < len(self.gmail_credentials):
                self.current_gmail_index = current_index
                gmail_cred = self.gmail_credentials[current_index]
                hostname = "https://gmail.com"
                #hostname = 'https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#identifier'
                self.driver.get(hostname)
                username = gmail_cred.get('username')
                password = gmail_cred.get('password')
                self.socketio.emit('action', 'Logging in to gmail with user '+username)
                username_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
                username_input.send_keys(username)
                next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CwaK9")))
                next_btn.click()
                time.sleep(3)

                password_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
                password_input.send_keys(password)
                password_next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CwaK9")))
                password_next_btn.click()
                time.sleep(5)

                # is_too_many_attempt = self.driver.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, ".uMiyC")))
                # if is_too_many_attempt:
                #     self.screenshot.capture("gmail_login_too_many_attempt")
                #     self.socketio.emit('action', 'Failed login to gmail...too many attempt')

                otp_verification_present = self.driver.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
                if otp_verification_present:
                    mobile_verificaiton_button = self.driver.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
                    if mobile_verificaiton_button:
                        self.socketio.emit('action', 'Clicking on mobile verification link')
                        mobile_verificaiton_button.click()
                        self.socketio.emit('gmail_otp_verification', 'Enter the OTP: ')
                else:
                    if self.verify_gmail_logged_in():
                        self.socketio.emit('action', 'Successfully logged in to gmail')
                    else:
                        self.socketio.emit('action', 'Unable to login to gmail...')



                # if self.verify_gmail_logged_in():
                #     self.socketio.emit('action', 'Successfully logged in to gmail')
                # else:
                #     try:
                #         mobile_verificaiton_button = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
                #         if mobile_verificaiton_button:
                #             self.socketio.emit('action', 'Clicking on mobile verification link')
                #             mobile_verificaiton_button.click()
                #             self.socketio.emit('gmail_otp_verification', 'Enter the OTP: ')
                #     except TimeoutException:
                #         self.socketio.emit('action', 'Unable to login to gmail...')



    def sequence_logout_linkedIn(self):
        self.logger.info("LinkedIn logged out")

    def sequence_logout_gmail(self):
        self.logger.info("Gmail logged out")

    def sequence_exit(self):
        self.logger.info("Exit script")


    def gmail_otp_login(self, otp):
        otp_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
        otp_input.send_keys(otp)
        next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#idvPreregisteredPhoneNext")))
        next_btn.click()
        time.sleep(1)
        if self.verify_gmail_logged_in():
            self.socketio.emit('action', 'Successfully logged in to gmail after otp verification')
        else:
            self.socketio.emit('action', 'Unable to login to gmail...')


    def verify_gmail_logged_in(self):
        self.logger.info("Checking if gmail logged in")
        self.socketio.emit('action', 'Verifying gmail login...')
        time.sleep(1)
        try:
            gmail_inbox_logo = self.driver.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "a[title='Inbox']")))
            if gmail_inbox_logo:
                return True
            else:
                self.screenshot.capture("gmail_login_unknown_screen")
                return False
        except TimeoutException:
            self.screenshot.capture("gmail_login_unknown_screen")
            return False



    def get_credentials(self,key):
        if key == 'gmail':
            return GMAIL_CREDENTIALS
        else:
            return []

        # if self.data_source == 'file':
        #     self.logger.info("Data source is file")
        #     conf_parser = CredentialParser(self.logger)
        #     return conf_parser.parse_config(key)
        # else:
        #     return []





import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from linkedInHandler import LinkedInHandler
from common_functions import *
from settings import *


class LinkedInHandle():
    """docstring for LinkedIn"""

    def __init__(self, executor):
        super(LinkedInHandle, self).__init__()
        self.driver = executor.driver
        self.logger = executor.logger
        self.socketio = executor.socketio
        self.screenshot = executor.screenshot
        self.account = executor.account

        self.login_url = "https://www.linkedin.com/login"
        self.logout_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.check_login_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.import_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.export_url = "https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/"

    def login(self):
        self.driver.get(self.login_url)
        credentials = self.account.get('linkedIn')
        username = credentials.get('username')
        password = credentials.get('password')
        if search_element_by_id(self.driver, 'username'):
            try:
                user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
                user.send_keys(username)
                pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
                pwd.send_keys(password)
                # submit_form
                login = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
                login.click()
                time.sleep(5)

                if search_element_by_css_selector(self.driver, "#error-for-password"):
                    error_msg = self.driver.find_element_by_css_selector("#error-for-password").text
                    self.socketio.emit('action', error_msg)
                else:
                    return True

            except Exception as e:
                return False
        else:
            return False

    def logout(self):
        try:
            self.driver.get(self.logout_url)
            clk = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
            clk.click()
            time.sleep(2)
            # Logout
            logout = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
            logout.click()
            time.sleep(2)
            return True
        except:
            return False
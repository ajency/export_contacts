import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from linkedInHandler import LinkedInHandler
from common_functions import *
from settings import *


class YahooHandle():
    """docstring for Yahoo"""

    def __init__(self, executor):
        super(YahooHandle, self).__init__()
        self.driver = executor.driver
        self.logger = executor.logger
        self.socketio = executor.socketio
        self.screenshot = executor.screenshot
        self.account = executor.account

        self.login_url = "https://login.yahoo.com/account/"
        self.logout_url = "https://login.yahoo.com/account/"
        self.check_login_url = "https://login.yahoo.com/account/"

    def login(self, email):
        self.driver.get(self.login_url)
        username = email.get('username')
        password = email.get('password')
        if search_element_by_id(self.driver, 'login-username'):
            try:
                user = self.driver.find_element_by_id('login-username')
                user.clear()
                user.send_keys(username)
                time.sleep(1)
                self.driver.find_element_by_id("login-signin").click()
                time.sleep(2)
                pwd = self.driver.find_element_by_id("login-passwd")
                pwd.send_keys(password)
                time.sleep(1)
                login = self.driver.find_element_by_id("login-signin")
                login.click()
                time.sleep(2)
                return True
            except:
                return False
        else:
            return False

    def logout(self):
        try:
            self.driver.get(self.logout_url)
            clk = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
            self.driver.execute_script("arguments[0].click();", clk)
            time.sleep(1)
            # Logout
            logout = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenuBody"]/a[3]')))
            logout.click()
            time.sleep(1)
            return True
        except:
            return False
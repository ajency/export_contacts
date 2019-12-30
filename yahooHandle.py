import time
from selenium.common.exceptions import TimeoutException
from common_functions import *


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
                if self.is_logged_in():
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

    def logout(self, source):
        try:
            self.driver.get(self.logout_url)
            clk = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ybarAccountMenu"]')))
            self.driver.execute_script("arguments[0].click();", clk)
            time.sleep(3)
            # Logout
            if source == 'yahoo':
                logout_selector = '//*[@id="ybarAccountMenuBody"]/a[3]'
            if source == 'aol':
                logout_selector = '//*[@id="ybarAccountMenuBody"]/a'
            logout = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, logout_selector)))
            #logout.click()
            self.driver.execute_script("arguments[0].click();", logout)
            time.sleep(1)
            return True
        except:
            return False

    def is_logged_in(self):
        try:
            p_info_title = self.driver.wait.until(
                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#group-personal-title")))
            if p_info_title:
                return True
            else:
                return False
        except TimeoutException:
            return False


    def confirm_import(self):
        if len(self.driver.window_handles) > 1:
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                agree_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "oauth2-agree")))
                agree_btn.click()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return True
            except:
                return False
        else:
            return False

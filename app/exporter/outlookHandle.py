import time
from selenium.common.exceptions import TimeoutException
from .common_functions import *


class OutlookHandle():
    """docstring for Outlook"""

    def __init__(self, executor):
        super(OutlookHandle, self).__init__()
        self.driver = executor.driver
        self.logger = executor.logger
        self.socketio = executor.socketio
        self.screenshot = executor.screenshot
        self.account = executor.account

        self.login_url = "https://login.live.com/login.srf"
        self.accounts_url = "https://account.microsoft.com/"

    def login(self, email):
        self.driver.get(self.login_url)
        username = email.get('username')
        password = email.get('password')

        username_input = self.driver.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        username_input.send_keys(username)

        try:
            next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']")))
            #next_btn.click()
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(5)
        except TimeoutException:
            self.socketio.emit('action', 'Error locating the next button after putting username')
            return False

        password_input = self.driver.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys(password)

        try:
            signin_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']")))
            #signin_btn.click()
            self.driver.execute_script("arguments[0].click();", signin_btn)
            time.sleep(5)
        except TimeoutException:
            self.socketio.emit('action', 'Error locating the sign in button after putting password')
            return False

        if self.is_logged_in():
            return True
        else:
            return False



    def submit_phone_verification_otp(self, otp):
        otp_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
        otp_input.send_keys(otp)



    def logout(self):
        if 'outlook' not in self.driver.current_url:
            self.driver.get(self.login_url)
            time.sleep(3)
        self.driver.delete_all_cookies()
        time.sleep(3)
        return True

    def is_logged_in(self):
        try:
            profile_info = self.driver.wait.until(
                EC.visibility_of_any_elements_located((By.ID, "loaded-home-banner-profile-section")))
            if profile_info:
                return True
            else:
                return False
        except TimeoutException:
            return False


    def confirm_import(self):
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(5)

            if search_element_by_css_selector(self.driver, '#iShowSkip'):
                skip_link = self.driver.find_element_by_css_selector('#iShowSkip')
                skip_link.click()
                time.sleep(3)

            try:
                submit_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "idBtn_Accept")))
                # submit_btn.click()
                self.driver.execute_script("arguments[0].click();", submit_btn)
                self.driver.switch_to.window(self.driver.window_handles[0])
                return True
            except Exception as ex:
                print(ex)
                return False
        else:
            return False

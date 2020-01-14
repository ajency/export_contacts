import time
from selenium.common.exceptions import TimeoutException
from .common_functions import *
import json
from flask_socketio import emit


class GmailHandle():
    """docstring for Yahoo"""

    def __init__(self, executor):
        super(GmailHandle, self).__init__()
        self.driver = executor.driver
        self.logger = executor.logger
        self.screenshot = executor.screenshot
        self.account = executor.account

        self.login_url = "https://accounts.google.com/ServiceLogin"
        self.logout_url = "https://accounts.google.com/Logout"

    def login(self, email):
        self.driver.get(self.login_url)
        username = email.get('username')
        password = email.get('password')

        username_input = self.driver.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        username_input.send_keys(username)

        try:
            next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CwaK9")))
            next_btn.click()
            time.sleep(5)
        except TimeoutException:
            emit('action', 'Error locating the next button after putting username')
            return False

        password_input = self.driver.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys(password)

        try:
            password_next_btn = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".CwaK9")))
            password_next_btn.click()
            time.sleep(5)
        except TimeoutException:
            emit('action', 'Error locating the next button after putting password')
            return False

        if self.is_logged_in():
            return True

        try:
            otp_verification_present = WebDriverWait(self.driver, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
            if otp_verification_present:
                mobile_verificaiton_button = self.driver.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.JDAKTe div.lCoei")))
                if mobile_verificaiton_button:
                    emit('action', 'Clicking on mobile verification link')
                    mobile_verificaiton_button.click()

                    otp_payload = {
                        'input_type': 'otp',
                        'handler': 'gmail',
                        'key': 'phone_verification_otp',
                        'message': 'Gmail Phone Verification OTP'
                    }
                    emit('prompt_user', json.dumps(otp_payload))

                    try:
                        otp_entered = WebDriverWait(self.driver, 200).until(lambda driver: len(
                            driver.find_element_by_css_selector("input[type='tel']").get_attribute("value")) == 6)
                        if otp_entered:
                            next_btn = self.driver.wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "#idvPreregisteredPhoneNext")))
                            next_btn.click()
                            time.sleep(3)
                            if self.is_logged_in():
                                return True
                    except:
                        return False
        except TimeoutException:
            return False



    def submit_phone_verification_otp(self, otp):
        otp_input = self.driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel']")))
        otp_input.send_keys(otp)



    def logout(self):
        try:
            self.driver.get(self.logout_url)
            time.sleep(5)
            return True
        except:
            return False

    def is_logged_in(self):
        try:
            p_info_title = self.driver.wait.until(
                EC.visibility_of_any_elements_located((By.XPATH, '//a[@href="personal-info"]')))
            if p_info_title:
                return True
            else:
                return False
        except TimeoutException:
            return False


    def confirm_import(self, email):
        if len(self.driver.window_handles) > 1:
            username = email.get('username')
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(3)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                account_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-identifier='"+username+"']")))
                #account_btn.click()
                self.driver.execute_script("arguments[0].click();", account_btn)

                time.sleep(5)
                agree_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.ID, "submit_approve_access")))
                #agree_btn.click()
                self.driver.execute_script("arguments[0].click();", agree_btn)


                self.driver.switch_to.window(self.driver.window_handles[0])
                return True
            except Exception as ex:
                print(ex)
                return False
        else:
            emit('action', "No confirm window found!")
            return False

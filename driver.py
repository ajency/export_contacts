import os,sys,time,datetime,platform,random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from logger import CustomLogger
from settings import *

class Driver():
    """docstring for Driver"""
    def __init__(self, headless_mode=True):
        super(Driver, self).__init__()


    def get_driver_path(self):
        # operating system 
        path = os.getcwd()+"/webdriver/linux/chromedriver"
        # operating system [Linux]
        if platform.system().lower() == 'Darwin':
            path = os.getcwd()+"/webdriver/mac/chromedriver"
        else:
            path = os.getcwd()+"/webdriver/linux/chromedriver"

        return path

    # def get_headless_browser_binary_file_path(self):
    #     # operating system 
    #     path = os.getcwd()+"/assets/chrome_driver/headless-chromium"
    #     # operating system [Linux]
    #     if platform.system().lower() == 'linux':
    #         path = os.getcwd()+"/assets/chrome_driver/headless-chromium"

    #     return path

    def initialize_chrome_driver(self, headless_mode, user_agent=''):

        driver_path = self.get_driver_path()
        # headless_chromium_path = self.get_headless_browser_binary_file_path()
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--no-referrers')
            chrome_options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")

            if not user_agent:
                user_agent = random.choice(USER_AGENT_LIST)                

            if headless_mode:
                # Headless Browser mode
                CustomLogger.info("Initializing web driver in headless mode true")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                # chrome_options.add_argument('--window-size=1920,1080')
                # chrome_options.add_argument('--single-process')
                chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
                chrome_options.add_argument('--user-agent={'+user_agent+'}')


            self.user_agent = user_agent
            self.headless_mode = headless_mode

            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
            driver.wait = WebDriverWait(driver, 10)
            return driver
        except Exception as e:
            CustomLogger.error(str(e))
            sys.exit()

    def close(self):
        self.driver.close()


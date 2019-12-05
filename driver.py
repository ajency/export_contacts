import os,sys,time,datetime,platform
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from logger import CustomLogger
# from common import *

class Driver():
    """docstring for Driver"""
    def __init__(self, headless_mode=True):
        super(Driver, self).__init__()


    def get_driver_path(self):
        # operating system 
        path = "assets/chrome_driver/chromedriver"
        # operating system [Linux]
        if platform.system().lower() == 'linux':
            path = "assets/chrome_driver/chromedriver"

        return path

    def get_headless_browser_binary_file_path(self):
        # operating system 
        path = "/assets/chrome_driver/headless-chromium"
        # operating system [Linux]
        if platform.system().lower() == 'linux':
            path = "/assets/chrome_driver/headless-chromium"

        return path

    def initialize_chrome_driver(self, headless_mode):

        driver_path = self.get_driver_path()
        headless_chromium_path = self.get_headless_browser_binary_file_path()
        try:
            chrome_options = webdriver.ChromeOptions()

            if headless_mode:
                # Headless Browser mode
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors. 
                # chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
                chrome_options.add_argument('--single-process')
                chrome_options.binary_location = os.getcwd() + headless_chromium_path

            chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
            chrome_options.add_argument('--window-size=1280x1696')
            chrome_options.add_argument('--user-data-dir=/tmp/user-data')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--enable-logging')
            chrome_options.add_argument('--log-level=0')
            chrome_options.add_argument('--v=99')
            chrome_options.add_argument('--data-path=/tmp/data-path')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--homedir=/tmp')
            chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')

            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

            return driver
        except Exception as e:
            CustomLogger.error(e)
            sys.exit()

    def close(self):
        self.driver.close()


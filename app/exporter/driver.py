import os,sys,platform,random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType

class Driver():
    """docstring for Driver"""
    def __init__(self, socketio):
        super(Driver, self).__init__()
        self.socketio = socketio


    def get_driver_path(self):
        if platform.system().lower() == 'darwin':
            path = os.getcwd()+"/webdriver/mac/chromedriver"
        else:
            path = os.getcwd()+"/webdriver/linux/chromedriver"

        print(path)

        return path

    def initialize_chrome_driver(self, headless_mode, proxy_list=[], user_agent=''):

        driver_path = self.get_driver_path()
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--no-referrers')
            chrome_options.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")
            chrome_options.add_argument("--start-maximized")

            if len(proxy_list) > 0:
                prox = random.choice(proxy_list)
                if self.socketio is not None:
                    self.socketio.emit('action', 'Web driver initialized with proxy ' + prox)
                proxy = Proxy()
                proxy.proxyType = ProxyType.MANUAL
                proxy.autodetect = False
                proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = prox
                chrome_options.Proxy = proxy
                chrome_options.add_argument("ignore-certificate-errors")

            #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'

            if headless_mode:
                # Headless Browser mode
                print("Initializing web driver in headless mode true")
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--user-agent={'+user_agent+'}')


            self.user_agent = user_agent
            self.headless_mode = headless_mode

            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
            driver.wait = WebDriverWait(driver, 10)
            return driver
        except Exception as e:
            print(str(e))
            sys.exit()

    def close(self):
        self.driver.close()


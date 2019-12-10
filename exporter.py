from logger import CustomLogger
from driver import Driver
from executor import Executor
from os import environ
from credential_parser import CredentialParser
from common_functions import *

class Exporter():
    def __init__(self, env, auto):
        self.env = environ.get('EXPORTER_ENVIRONMENT')
        self.data_source = environ.get('EXPORTER_DATA_SOURCE')
        self.auto = auto
        logger = CustomLogger()
        self.logger = logger
        self.web_driver = Driver()


    def start(self):

        self.logger.info("Operation started for "+self.env)
        self.gmail_credentials = self.get_credentials('gmail')

        ## to persist the log
        # self.logger.log("This is more logging message another",{
        #     'url': "some url",
        #     'type': "some type",
        #     'data': "some data"
        # })

        # initialize driver
        self.driver = self.web_driver.initialize_chrome_driver(headless_mode=True)
        # clear browser cookies
        self.delete_all_cookies()
        # initialize executor
        self.executor = Executor(self)
        # type and sequence of execution
        self.executor.get_execution_sequence(self.auto)

        # driver close
        self.driver.close()

        ##to close the log file once everything is done
        self.logger.close_logger()

    def get_credentials(self,key):
        if self.data_source == 'file':
            # self.logger.info("Data source is file")
            conf_parser = CredentialParser(self.logger)
            return conf_parser.parse_config(key)
        else:
            return []


    def delete_all_cookies(self):
        # new driver instance for linkedIn
        self.driver.get("https://www.linkedin.com/")
        self.driver.delete_all_cookies()
        # new driver instance for gmail
        self.driver.get("https://accounts.google.com/")
        self.driver.delete_all_cookies()
        # new driver instance for yahoo
        self.driver.get("https://login.yahoo.com/")
        self.driver.delete_all_cookies()
        # new driver instance for AOL
        self.driver.get("https://login.aol.com/account/")
        self.driver.delete_all_cookies()
        # new driver instance for outlook
        self.driver.get("https://account.microsoft.com/")
        self.driver.delete_all_cookies()

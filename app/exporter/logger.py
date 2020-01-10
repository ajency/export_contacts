#!/usr/bin/env python

from termcolor import colored
import datetime
import time
from os import environ

class CustomLogger():

    def __init__(self):
        self.info_color = 'green'
        self.warning_color = 'yellow'
        self.error_color = 'red'
        self.session_id = time.strftime("%Y%m%d-%H%M%S")

    def close_logger(self):
        if environ.get('LOGGER_BACKEND') == 'local':
            self.logger.close()

    def info(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("INFO::" + timestampstring, 'white', 'on_green'),colored(message, self.info_color))

    def error(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("ERROR::" + timestampstring, 'white', 'on_red'),colored(message, self.error_color))

    def warning(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("WARNING::" + timestampstring, 'white', 'on_yellow'),colored(message, self.warning_color))
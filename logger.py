#!/usr/bin/env python

from termcolor import colored
import datetime

class CustomLogger():

    info_color = 'green'
    warning_color = 'yellow'
    error_color = 'red'

    def info(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("INFO::" + timestampstring, 'white', 'on_green'),colored(message, self.info_color))

    def error(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("ERROR::" + timestampstring, 'white', 'on_red'),colored(message, self.error_color))

    def warning(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("WARNING::" + timestampstring, 'white', 'on_yellow'),colored(message, self.warning_color))
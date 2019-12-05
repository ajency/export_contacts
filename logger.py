#!/usr/bin/env python

from termcolor import colored
import datetime
import time
import os
from pathlib import Path

class CustomLogger():

    info_color = 'green'
    warning_color = 'yellow'
    error_color = 'red'

    def create_logger_file(self):
        self.session_id = time.strftime("%Y%m%d-%H%M%S")
        log_path = 'logs/'+time.strftime("%Y%m%d")
        Path(log_path).mkdir(parents=True, exist_ok=True)
        filename = log_path+"/"+self.session_id + '.txt'

        if os.path.exists(filename):
            append_write = 'a'
        else:
            append_write = 'w'
        self.log_file = open(filename,append_write)

    def close_logger_file(self):
        self.log_file.close()

    def file_log(self, message, url=None, type=None):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        log_content = timestampstring+": "
        if url is not None:
            log_content+="URL: "+url+" "
        if type is not None:
            log_content+="Type: "+type
        log_content+=" ::: "+message
        self.log_file.write(log_content+"\n")


    def info(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("INFO::" + timestampstring, 'white', 'on_green'),colored(message, self.info_color))

    def error(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("ERROR::" + timestampstring, 'white', 'on_red'),colored(message, self.error_color))

    def warning(self,message):
        timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
        print(colored("WARNING::" + timestampstring, 'white', 'on_yellow'),colored(message, self.warning_color))
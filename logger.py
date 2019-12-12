#!/usr/bin/env python

from termcolor import colored
import datetime
import time
import os
from pathlib import Path

import logging
import timber
from os import environ

class CustomLogger():

    def __init__(self):
        self.info_color = 'green'
        self.warning_color = 'yellow'
        self.error_color = 'red'
        self.session_id = time.strftime("%Y%m%d-%H%M%S")

        if environ.get('LOGGER_BACKEND') == 'timber':
            self.logger = self.timber_logger()
        else:
            self.logger = self.local_logger()


    def timber_logger(self):
        environment = environ.get('EXPORTER_ENVIRONMENT')
        timber_source_id = environ.get('TIMBER_SOURCE_ID_' + environment)
        timber_api_key = environ.get('TIMBER_API_KEY_' + environment)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        context = timber.TimberContext()
        timber_handler = timber.TimberHandler(source_id=timber_source_id, api_key=timber_api_key, buffer_capacity=3, flush_interval=10, drop_extra_events=False, context=context)
        logger.addHandler(timber_handler)
        return logger

    def local_logger(self):
        log_path = 'logs/' + time.strftime("%Y%m%d")
        Path(log_path).mkdir(parents=True, exist_ok=True)
        filename = log_path+"/"+self.session_id + '.txt'
        self.file_path = filename
        self.info("Local Log File Path: "+filename)

        if os.path.exists(filename):
            append_write = 'a'
        else:
            append_write = 'w'
        return open(filename, append_write)

    def log(self, message, context):
        if environ.get('LOGGER_BACKEND') == 'timber':
            with timber.context(session={'id': self.session_id}):
                print(context)
                self.logger.info(message, extra=context)
        else:
            timestampstring = datetime.datetime.now().strftime("%H:%M:%S")
            log_content = timestampstring + ": "
            if 'url' in context:
                log_content += "URL: " + context['url'] + " "
            if 'type' in context:
                log_content += "Type: " + context['type']
            if 'data' in context:
                log_content += " Data: " + context['data']
            log_content += " ::: " + str(message)
            self.logger.write(log_content + "\n")

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
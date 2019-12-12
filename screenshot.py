#!/usr/bin/env python

from termcolor import colored
import datetime
import time
import os
from pathlib import Path

import logging
import timber
from os import environ

class Screenshot():

    def __init__(self, session_id, driver):
        self.session_id = session_id
        self.driver = driver

    def capture(self, key):
        log_path = 'driver_screenshots/' + self.session_id
        Path(log_path).mkdir(parents=True, exist_ok=True)
        filename = log_path + "/" + key + '.png'
        self.driver.save_screenshot(filename)
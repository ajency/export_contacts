#!/usr/bin/env python
from pathlib import Path
import os

class Screenshot():

    def __init__(self, session_id, driver):
        self.session_id = session_id
        self.driver = driver

    def capture(self, key):
        #log_path = 'static/driver_screenshots/' + self.session_id
        log_path = os.getcwd() + "/app/base/static/driver_screenshots/" + self.session_id
        Path(log_path).mkdir(parents=True, exist_ok=True)
        filename = log_path + "/" + key + '.png'
        self.driver.save_screenshot(filename)
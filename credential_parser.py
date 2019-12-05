#!/usr/bin/env python
import sys
from pathlib import Path
import json

class CredentialParser():
    def __init__(self, logger):
        self.config_path = Path('.') / 'credentials.json'
        self.logger = logger

    def parse_config(self, key):
        try:
            with open(self.config_path) as f:
                data = json.load(f)
                if key in data:
                    return data[key]
                else:
                    return []
        except:
            self.logger.error("Error parsing config data")
            sys.exit()
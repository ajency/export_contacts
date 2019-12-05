from logger import CustomLogger
from os import environ
from credential_parser import CredentialParser

class Exporter():
    def __init__(self, env, auto):
        self.env = environ.get('EXPORTER_ENVIRONMENT')
        self.data_source = environ.get('EXPORTER_DATA_SOURCE')
        self.auto = auto
        self.logger = CustomLogger()

    def start(self):
        self.logger.info("Operation started for "+self.env)
        self.gmail_credentials = self.get_credentials('gmail')
        print(self.gmail_credentials)

    def get_credentials(self,key):
        if self.data_source == 'file':
            self.logger.info("Data source is file")
            conf_parser = CredentialParser(self.logger)
            return conf_parser.parse_config(key)
        else:
            return {}





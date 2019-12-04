from logger import CustomLogger
from os import environ

class Exporter():
    def __init__(self, env, auto):
        self.env = environ.get('EXPORTER_ENVIRONMENT')
        self.data_source = environ.get('EXPORTER_DATA_SOURCE')
        self.auto = auto
        self.logger = CustomLogger()

    def start(self):
        self.logger.info("Operation started for "+self.env)

    def get_credentials(self):
        if self.data_source == 'file':
            self.logger.info("Data source is file")




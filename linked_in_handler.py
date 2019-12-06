from credential_parser import CredentialParser

class LinkedInHandler():
    def __init__(self, logger):
        self.logger = logger


    def start(self):
        self.logger.info("Operation started for "+self.env)
        self.gmail_credentials = self.get_credentials('gmail')
        print(self.gmail_credentials)

        ## to persist the log
        self.logger.file_log("This is test message","test url","testing")

        ##to close the log file once everything is done
        self.logger.close_logger_file()

    def get_credentials(self,key):
        if self.data_source == 'file':
            self.logger.info("Data source is file")
            conf_parser = CredentialParser(self.logger)
            return conf_parser.parse_config(key)
        else:
            return []





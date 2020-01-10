from .logger import CustomLogger
from .driver import Driver
from .screenshot import Screenshot
from .common_functions import *
from .linkedInHandle import LinkedInHandle
from .yahooHandle import YahooHandle
from .aolHandle import AolHandle
from .gmailHandle import GmailHandle
from .outlookHandle import OutlookHandle
import time

class Executor():
    def __init__(self, env, auto, headless, socketio, proxy_list, account):
        self.env = env
        self.auto = auto
        self.socketio = socketio
        self.logger = CustomLogger()
        # initialize driver
        self.web_driver = Driver(self.socketio)
        self.driver = self.web_driver.initialize_chrome_driver(headless, proxy_list)
        # initialize screnshot session
        self.session_id = time.strftime("%Y%m%d-%H%M%S")
        self.screenshot = Screenshot(self.session_id, self.driver)
        self.account = account
        self.linkedInHandle = LinkedInHandle(self)
        self.yahooHandle = YahooHandle(self)
        self.aolHandle = AolHandle(self)
        self.gmailHandle = GmailHandle(self)
        self.outlookHandle = OutlookHandle(self)




    def step_linkedIn_login(self):
        self.socketio.emit("action", "Step: linkedIn_login")
        if self.linkedInHandle.login():
            self.socketio.emit('action', 'Login to Linked in Successfull!')
            return True
        else:
            self.screenshot.capture('linkedIn_login_error')
            self.socketio.emit('action', 'Error linkedIn login. Check screenshots for details.')
            return False

    def step_email_operation(self, sequences):
        self.socketio.emit("action", "Step: email_operation")
        total_email_count = 0
        failed_email_count = 0
        emails = self.account.get('email')
        for email_provider in emails:

            last_provider = False
            if email_provider == sorted(emails.keys())[-1]:
                last_provider = True

            provider = self.account.get('email').get(email_provider)
            self.logger.info("==== Email operation started for provider " + email_provider)
            for email_account in provider:

                last_entry = False
                if email_account == provider[len(provider)-1] and last_provider:
                    print("last operation!! for email "+ email_account.get('username'))
                    last_entry = True

                total_email_count += 1
                self.logger.info("==== Email sequences with user " + email_account.get('username'))
                for sequence in sequences:
                    key_name = str(sequence) + "_" + email_provider + "_" + email_account.get('username').replace('.','').replace('@', '')
                    self.socketio.emit('tree_progress', key_name)
                    is_success = getattr(self, 'step_' + sequence)(email_provider, email_account, last_entry)
                    if is_success:
                        self.socketio.emit('tree_success', key_name)
                    else:
                        getattr(self, 'step_email_logout')(email_provider, email_account, last_entry)
                        self.socketio.emit('tree_failed', key_name)
                        failed_email_count += 1
                        self.socketio.emit('action','Error performing '+sequence+' for email id: '+email_account.get('username')+'. Skipping....')
                        break
        if total_email_count == failed_email_count:
            self.socketio.emit('action', 'Error email operation, all email failed.')
            return False
        else:
            self.socketio.emit('action', 'Email operation successfull!')
            return True

    def step_linkedIn_logout(self):
        self.socketio.emit("action", "Step: linkedIn_logout")
        if self.linkedInHandle.logout():
            self.socketio.emit('action', 'Linked in logout successfull!')
            return True
        else:
            self.screenshot.capture('linkedIn_logout_error')
            self.socketio.emit('action', 'Error logging out from linkedIn. Check screenshots for details.')
            return False



    def step_email_login(self, provider, email, last_entry):
        self.socketio.emit("action", "Step: email_login")
        self.socketio.emit('action','Performing email login with id '+email.get('username'))
        return getattr(self, 'email_login_' + provider)(email)

    def step_import_contacts(self, provider, email, last_entry):
        self.socketio.emit("action", "Step: import_contacts")
        if self.linkedInHandle.import_contacts(provider, email):
            self.socketio.emit('action', 'Import contacts successful for '+provider+' with email: '+email.get('username'))
            return True
        else:
            self.screenshot.capture('import_contacts_error_'+email.get('username'))
            self.socketio.emit('action', 'Import contacts failed for '+provider+' with email: '+email.get('username'))
            return False

    def step_export_contacts(self, provider, email, last_entry):
        self.socketio.emit("action", "Step: export_contacts")
        if self.linkedInHandle.export_contacts(email):
            self.socketio.emit('action', 'Export contacts successful for ' + provider + ' with email: ' + email.get('username'))
            return True
        else:
            self.screenshot.capture('export_contacts_error_' + email.get('username'))
            self.socketio.emit('action', 'Export contacts failed for ' + provider + ' with email: ' + email.get('username'))
            return False

    def step_delete_contacts(self, provider, email, last_entry):
        self.socketio.emit("action", "Step: delete_contacts")
        if self.linkedInHandle.delete_contacts(last_entry):
            self.socketio.emit('action', 'Delete contacts successful for ' + provider + ' with email: ' + email.get('username'))
            time.sleep(10)
            return True
        else:
            self.screenshot.capture('delete_contacts_error_' + email.get('username'))
            self.socketio.emit('action', 'Delete contacts failed for ' + provider + ' with email: ' + email.get('username'))
            return False

    def step_email_logout(self, provider, email, last_entry):
        self.socketio.emit("action", "Step: email_logout")
        return getattr(self, 'email_logout_' + provider)()





    def email_login_gmail(self,email):
        self.logger.info("==== logging in to gmail account " + email.get('username'))
        if self.gmailHandle.login(email):
            self.socketio.emit('action', 'Login to gmail successful!')
            return True
        else:
            self.screenshot.capture('gmail_login_error_' + email.get('username'))
            self.socketio.emit('action', 'Error gmail login. Check screenshots for details.')
            return False

    def email_login_yahoo(self,email):
        self.logger.info("==== logging in to yahoo account " + email.get('username'))
        if self.yahooHandle.login(email, 'yahoo'):
            self.socketio.emit('action', 'Login to yahoo successful!')
            return True
        else:
            self.screenshot.capture('yahoo_login_error_'+email.get('username'))
            self.socketio.emit('action', 'Error yahoo login. Check screenshots for details.')
            return False

    def email_login_aol(self,email):
        self.logger.info("==== logging in to aol account " + email.get('username'))
        if self.aolHandle.login(email, 'aol'):
            self.socketio.emit('action', 'Login to aol successful!')
            return True
        else:
            self.screenshot.capture('aol_login_error_' + email.get('username'))
            self.socketio.emit('action', 'Error aol login. Check screenshots for details.')
            return False

    def email_login_outlook(self,email):
        self.logger.info("==== logging in to outlook account " + email.get('username'))
        if self.outlookHandle.login(email):
            self.socketio.emit('action', 'Login to outlook successful!')
            return True
        else:
            self.screenshot.capture('outlook_login_error_' + email.get('username'))
            self.socketio.emit('action', 'Error outlook login. Check screenshots for details.')
            return False

    def email_logout_gmail(self):
        self.logger.info("==== logging out from gmail account ===")
        if self.gmailHandle.logout():
            self.socketio.emit('action', 'Gmail logout successful!')
            return True
        else:
            self.screenshot.capture('gmail_logout_error')
            self.socketio.emit('action', 'Error logging out from gmail. Check screenshots for details.')
            return False

    def email_logout_yahoo(self):
        self.logger.info("==== logging out from yahoo account ===")
        if self.yahooHandle.logout():
            self.socketio.emit('action', 'Yahoo logout successful!')
            return True
        else:
            self.screenshot.capture('yahoo_logout_error')
            self.socketio.emit('action', 'Error logging out from yahoo. Check screenshots for details.')
            return False

    def email_logout_aol(self):
        self.logger.info("==== logging out from aol account ===")
        if self.aolHandle.logout():
            self.socketio.emit('action', 'AOL logout successful!')
            return True
        else:
            self.screenshot.capture('aol_logout_error')
            self.socketio.emit('action', 'Error logging out from aol. Check screenshots for details.')
            return False

    def email_logout_outlook(self):
        self.logger.info("==== logging out from outlook account ===")
        if self.outlookHandle.logout():
            self.socketio.emit('action', 'Outlook logout successful!')
            return True
        else:
            self.screenshot.capture('outlook_logout_error')
            self.socketio.emit('action', 'Error logging out from outlook. Check screenshots for details.')
            return False
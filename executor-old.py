import numpy
import os, sys, time, datetime, platform
from handler import Handler
from logger import CustomLogger
from aol import AOL
from gmail import Gmail
from yahoo import Yahoo
from outlook import OutLook
from linkedIn import LinkedIn
from common_functions import *
from settings import *


class Executor():
    """docstring for Executor"""

    def __init__(self, exporter):
        super(Executor, self).__init__()
        self.driver = exporter.driver
        self.logger = exporter.logger
        self.socketio = exporter.socketio
        self.screenshot = exporter.screenshot
        self.handler = Handler(self.driver, self.logger, self.socketio, self.screenshot)
        self.linkedin = LinkedIn(exporter)
        self.gmail = Gmail(exporter)
        self.aol = AOL(exporter)
        self.yahoo = Yahoo(exporter)
        self.outlook = OutLook(exporter)
        self.account = exporter.account

    def get_execution_sequence(self, auto_execution_mode=True):
        execution_sequence = AUTO_EXECUTION_SEQUENCE
        if not auto_execution_mode:
            execution_sequence = self.get_user_defined_execution_sequence()
            return execution_sequence

    def execute_sequence(self, execution_sequence):
        sequence = execution_sequence.split()
        for step in sequence:
            my_step = int(str(step).strip())
            if my_step == 0:
                self.step_zero_exit()
            elif my_step == 1:
                self.step_one()
            elif my_step == 2:
                self.step_two()
            elif my_step == 3:
                self.step_three()
            elif my_step == 4:
                self.step_four()
            elif my_step == 5:
                self.step_five()
            elif my_step == 6:
                self.step_six()
            elif my_step == 7:
                self.step_seven()
            elif my_step == 8:
                self.step_eight()
            elif my_step == 9:
                self.step_nine()
            elif my_step == 10:
                self.step_ten()
            elif my_step == 11:
                self.step_eleven()
            elif my_step == 12:
                self.step_twelve()
            elif my_step == 13:
                self.step_thirteen()
            elif my_step == 14:
                self.step_fourteen()
            elif my_step == 15:
                self.step_fifteen()
            else:
                self.invalid_step(my_step)
            pass

    def get_user_defined_execution_sequence(self):
        print("Steps: ")
        print(" 1.  LinkedIn - Login")
        print(" 2.  LinkedIn - Logout")
        print(" 3.  Gmail - Login")
        print(" 4.  Gmail - Logout")
        print(" 5.  Yahoo - Login")
        print(" 6.  Yahoo - Logout")
        print(" 7.  AOL - Login")
        print(" 8.  AOL - Logout")
        print(" 9.  OutLook LogIn")
        print(" 10.  OutLook LogOut")
        print(" 11.  Gmail - Sync Account")
        print(" 12.  Yahoo - Sync Account")
        print(" 13.  AOL - Sync Account")
        print(" 14.  OutLook - Sync Account")
        # print(" 15.  Export Contacts")

        print("")
        print(" 0.  Exits the Script")
        print("__________________________________________________________")
        sequence = input(
            "Enter manual execution sequence seperated by <space> between each step (Example: 1 2 3) \n Enter your sequence: ")
        if sequence:
            return sequence
        else:
            get_user_defined_execution_sequence()
            pass

    def step_zero_exit(self):
        print("Step 0 - Exiting the script")
        # self.linkedin.linkedin_handler.exit_process("Step 0 - Exiting the script")
        sys.exit()

    def step_linkedIn_login(self):
        print("Step: linkedIn_login")
        self.linkedin.login_to_linkedin()
        pass

    def step_two(self):
        print("step 2")
        self.linkedin.logout_from_linkedin()
        pass

    def step_three(self):
        print("step 3")
        self.gmail.login_to_gmail()
        pass

    def step_four(self):
        print("step 4")
        self.gmail.logout_from_gmail()
        pass

    def step_five(self):
        print("step 5")
        self.yahoo.login_to_yahoo()
        pass

    def step_six(self):
        print("step 6")
        self.yahoo.logout_from_yahoo()
        pass

    def step_seven(self):
        print("step 7")
        self.aol.login_to_aol()
        pass

    def step_eight(self):
        print("step 8")
        self.aol.logout_from_aol()
        pass

    def step_nine(self):
        print("step 9")
        self.outlook.login_to_outlook()
        pass

    def step_ten(self):
        print("step 10")
        self.outlook.logout_from_outlook()
        pass

    def step_eleven(self):
        print("step 11")
        self.sync_gmail_account()
        pass

    def step_twelve(self):
        print("step 12")
        self.sync_yahoo_account()
        pass

    def step_thirteen(self):
        print("step 13")
        self.sync_aol_account()
        pass

    def step_fourteen(self):
        print("step 14")
        self.sync_outlook_account()
        pass

    def step_fifteen(self):
        print("step 15")
        # self.linkedin.export_contacts()
        pass

    def invalid_step(self, step=''):
        message = "Step (" + str(step) + ") is an invalid step"
        # print(message)
        self.logger.info(message)
        pass

    def sync_gmail_account(self):
        if not self.linkedin.is_user_logged_in():
            self.handler.warning("Need to login into LinkedIn to sync")
            self.linkedin.login_to_linkedin()
        self.gmail.sync_account()

    def sync_yahoo_account(self):
        if not self.linkedin.is_user_logged_in():
            self.handler.warning("Need to login into LinkedIn to sync")
            self.linkedin.login_to_linkedin()
        self.yahoo.sync_account()

    def sync_aol_account(self):
        if not self.linkedin.is_user_logged_in():
            self.handler.warning("Need to login into LinkedIn to sync")
            self.linkedin.login_to_linkedin()
        self.aol.sync_account()

    def sync_outlook_account(self):
        if not self.linkedin.is_user_logged_in():
            self.handler.warning("Need to login into LinkedIn to sync")
            self.linkedin.login_to_linkedin()
        self.outlook.sync_account()










    def step_linkedIn_login(self):
        print("Step: linkedIn_login")
        #return self.linkedin.login_to_linkedin()
        return True

    def step_email_operation(self, sequences):
        self.logger.info("Step: email_operation")
        total_email_count = 0
        failed_email_count = 0
        for email_provider in self.account.get('email'):
            provider = self.account.get('email').get(email_provider)
            self.logger.info("==== Email operation started for provider " + email_provider)
            for email_account in provider:
                total_email_count += 1
                self.logger.info("==== Email sequences with user " + email_account.get('username'))
                for sequence in sequences:
                    is_success = getattr(self, 'step_' + sequence)(email_provider, email_account)
                    if not is_success:
                        failed_email_count += 1
                        self.socketio.emit('action','Error performing '+sequence+' for email id: '+email_account.get('username')+'. Skipping....')
                        break
        if total_email_count == failed_email_count:
            return False
        else:
            return True

    def step_linkedIn_logout(self):
        self.logger.info("Step: linkedIn_login")
        #return self.linkedin.logout_from_linkedin()
        return True



    def step_email_login(self, provider, email):
        self.logger.info("Step: email_login")
        self.socketio.emit('action','Performing email login with id '+email.get('username'))
        return getattr(self, 'email_login_' + provider)(email)

    def step_import_contacts(self, provider, email):
        self.logger.info("Step: import_contacts")
        return getattr(self, 'import_contacts_from_' + provider)()

    def step_export_contacts(self, provider, email):
        self.logger.info("Step: export_contacts")
        #return self.linkedin.export_contacts()
        return True

    def step_delete_contacts(self, provider, email):
        self.logger.info("Step: delete_contacts")
        return True

    def step_email_logout(self, provider, email):
        self.logger.info("Step: email_logout")
        return getattr(self, 'email_logout_' + provider)()





    def email_login_gmail(self,email):
        self.logger.info("==== logging in to gmail account " + email.get('username'))
        return False

    def email_login_aol(self,email):
        self.logger.info("==== logging in to aol account " + email.get('username'))
        return True

    def email_login_outlook(self,email):
        self.logger.info("==== logging in to outlook account " + email.get('username'))
        return True


    def import_contacts_from_gmail(self):
        self.logger.info("==== Importing contacts from gamil ===")
        return False

    def import_contacts_from_aol(self):
        self.logger.info("==== Importing contacts from aol ===")
        return True

    def import_contacts_from_outlook(self):
        self.logger.info("==== Importing contacts from outlook ===")
        return True


    def email_logout_gmail(self):
        self.logger.info("==== logging out from gmail account ===")
        return True

    def email_logout_aol(self):
        self.logger.info("==== logging out from aol account ===")
        return True

    def email_logout_outlook(self):
        self.logger.info("==== logging out from outlook account ===")
        return True
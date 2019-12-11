# import numpy 
import os,sys,time,datetime,platform
from handler import Handler
from logger import CustomLogger
from aol import AOL
from gmail import Gmail
from yahoo import Yahoo
from outlook import OutLook
from linkedIn import LinkedIn
from common_functions import *
from config import *

class Executor():
	"""docstring for Executor"""
	def __init__(self, exporter):
		super(Executor, self).__init__()
		self.driver = exporter.driver
		self.logger = exporter.logger
		self.handler = Handler(self.driver, self.logger)
		self.aol = AOL(exporter)
		self.gmail = Gmail(exporter)
		self.yahoo = Yahoo(exporter)
		self.outlook = OutLook(exporter)
		self.linkedin = LinkedIn(exporter)


	def get_execution_sequence(self, auto_execution_mode=True):
		execution_sequence = auto_execution_sequence
		if not auto_execution_mode:
			execution_sequence = self.get_user_defined_execution_sequence()
		self.logger.info("Execution sequence: "+str(execution_sequence))
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
		print(" 7.  Gmail - Sync Account")
		print(" 8.  Yahoo - Sync Account")
		print(" 9.  AOL - Login")
		print(" 10.  AOL - Logout")
		print(" 11.  AOL - Sync Account")

		print("")
		print(" 0.  Exits the Script")
		print("__________________________________________________________")
		sequence = input("Enter manual execution sequence seperated by <space> between each step (Example: 1 2 3) \n Enter your sequence: ")
		if sequence:
			return sequence
		else:
			get_user_defined_execution_sequence()
			pass

	def step_zero_exit(self):
		print("Step 0 - Exiting the script")
		# self.linkedin.linkedin_handler.exit_process("Step 0 - Exiting the script")
		sys.exit()

	def step_one(self):
		print("step 1")
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
		self.driver.get(self.yahoo.yahoo_handler.login_url)
		self.yahoo.login_to_yahoo()
		pass

	def step_six(self):
		print("step 6")
		self.driver.get(self.yahoo.yahoo_handler.logout_url)
		self.yahoo.logout_from_yahoo()
		pass

	def step_seven(self):
		print("step 7")
		self.sync_gmail_account()
		pass

	def step_eight(self):
		print("step 8")
		self.sync_yahoo_account()
		pass

	def step_nine(self):
		print("step 9")
		self.aol.login_to_aol()
		pass

	def step_ten(self):
		print("step 10")
		self.aol.logout_from_aol()
		pass

	def step_eleven(self):
		print("step 11")
		self.sync_aol_account()
		pass

	def step_twelve(self):
		print("step 12")
	#	self.logger.file_log(message, url=None, type=None)
		pass

	def step_thirteen(self):
		print("step 13")
	#	self.logger.file_log(message, url=None, type=None)
		pass

	def step_fourteen(self):
		print("step 14")
		self.sync_outlook_account()
		pass

	def step_fifteen(self):
		print("step 15")
		self.linkedin.export_contacts()
		pass



	def invalid_step(self, step=''):
		message = "Step ("+str(step)+") is an invalid step"
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



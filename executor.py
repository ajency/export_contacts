import numpy 
import os,sys,time,datetime,platform
from logger import CustomLogger

class Executor():
	"""docstring for Executor"""
	def __init__(self):
		super(Executor, self).__init__()
		# self.arg = arg


	def execute_func(self, method_name):
		return getattr(self, str(method_name))


	def get_execution_sequence(self, auto_execution_mode=True):
		execution_sequence = "1 2"
		if not auto_execution_mode:
			execution_sequence = self.get_user_defined_execution_sequence()
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
			# elif my_step == 5: 
			# 	self.step_five()
			# elif my_step == 6: 
			# 	self.step_six()
			# elif my_step == 7: 
			# 	self.step_seven()
			# elif my_step == 8: 
			# 	self.step_eight()
			# elif my_step == 9: 
			# 	self.step_nine()
			# elif my_step == 10:
			# 	self.step_ten()
			# elif my_step == 11:
			# 	self.step_eleven()
			# elif my_step == 12:
			# 	self.step_twelve()
			else:
				self.invalid_step(my_step)
			pass




	def get_user_defined_execution_sequence(self):
		print("Steps: ")
		print(" 1 - Login into Gmail")
		print(" 2 - Login into LinkedIn")
		print(" 3 - Logout from LinkedIn")
		print(" 4 - Logout from Gmail")
		print("")
		print(" 0 - Exits the Script")
		print("__________________________________________________________")
		sequence = input("Enter manual execution sequence seperated by <space> between each step, \n Example: 1 3 2  \n Enter your sequence: ")
		if sequence:
			return sequence
		else:
			get_user_defined_execution_sequence()
			pass

	def step_zero_exit(self):
		print("Step 0 - Exiting the script")
		sys.exit()

	def step_one(self):
		print("step_one")
		pass

	def step_two(self):
		print("step_two")
		pass

	def step_three(self):
		print("step_three")
		pass

	def step_four(self):
		print("step_four")
		pass

	# def step_five(self):
	# 	print("invalid_step")
	# 	pass

	# def step_six(self):
	# 	print("invalid_step")
	# 	pass

	# def step_seven(self):
	# 	print("invalid_step")
	# 	pass

	# def step_eight(self):
	# 	print("invalid_step")
	# 	pass

	# def step_nine(self):
	# 	print("invalid_step")
	# 	pass

	# def step_ten(self):
	# 	print("invalid_step")
	# 	pass

	# def step_eleven(self):
	# 	print("invalid_step")
	# 	pass

	# def step_twelve(self):
	# 	print("invalid_step")
	# 	pass

	def invalid_step(self, step=''):
		message = "Step ("+str(step)+") is an invalid step"
		print(message)
		# CustomLogger.warning(message)
		pass
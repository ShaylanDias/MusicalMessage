import applescript
from time import sleep

class AutoTextMac:

	send_message ='''
		set targetService to 1st service whose service type = iMessage
		set targetBuddy to buddy "{number}" of targetService
		send "{message}" to targetBuddy
	'''

	grab_number_script='''
	set theContact to the first person whose name is "{name}"
	set mobile to value of every phone in theContact whose label is "_$!<Mobile>!$_"
	set iphone to value of every phone in theContact whose label is "iPhone"
	set reg to value of every phone in theContact whose label is "Phone"
	set home to value of every phone in theContact whose label is "_$!<Home>!$_"
	return mobile & iphone & reg & home
	'''

	def find_number(self, first_name, last_name):
		"""Finds a phone number in the local address book."""
		x = applescript.tell.app('Address Book', self.grab_number_script.format(name=first_name + ' ' + last_name), background=False)
		print(x)
		print(x.out)
		if x.err:
			raise ValueError("Applescript Failed on name: " + x.err)
		if x.out:
			numbers = x.out
			ind = numbers.find(',')
			if ind == -1:
				return numbers
			else:
				return numbers[:ind]
		else:
			return None

	def message_by_number(self, message, phonenumber, byline=True, delay=0):
		"""Sends a text to the provided phone number. Delay determines time between texts"""
		if byline:
			for line in message.splitlines():
					if len(line) > 0:
						sleep(delay)
						applescript.tell.app('Messages', self.send_message.format(number=phonenumber, message=line), background=False)
		else:
			for blob in message.split():
					applescript.tell.app('Messages', self.send_message.format(number=phonenumber, message=blob), background=False)

	def message_by_name(self, message, first_name, last_name, byline=True, delay=0):
		"""Sends a message to a person by name."""
		try:
			number = self.find_number(first_name, last_name)
			print("Number:", number)
			if not number or len(number) < 8:
				raise ValueError("No number found for that name.")
			self.message_by_number(message, number, byline=byline, delay=delay)
		except ValueError as e:
			print(e)
			return e
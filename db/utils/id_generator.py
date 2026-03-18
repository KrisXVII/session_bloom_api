from datetime import datetime

TODAY = datetime.utcnow().date()

class IDGenerator:
	def __init__(self):
		self.counter = 0
		self.last_date = datetime.utcnow().date()

	def generate_user_uid(self):

		if TODAY > self.last_date:
			self.counter = 0
			self.last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{self.counter:06d}"
		self.counter += 1

		return f"USR_{date_part}{counter_part}"

	def generate_session_uid(self):

		if TODAY > self.last_date:
			self.counter = 0
			self.last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{self.counter:06d}"
		self.counter += 1

		return f"SES_{date_part}{counter_part}"

	def generate_subsession_uid(self):

		if TODAY > self.last_date:
			self.counter = 0
			self.last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{self.counter:06d}"
		self.counter += 1

		return f"SUB_{date_part}{counter_part}"

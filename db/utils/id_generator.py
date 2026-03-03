from datetime import datetime

class IDGenerator:
	def __init__(self):
		self.counter = 0
		self.last_date = datetime.utcnow().date()

	def generate_uid(self):
		today = datetime.utcnow().date()

		# Reset counter if new day
		if today > self.last_date:
			self.counter = 0
			self.last_date = today

		date_part = today.strftime('%y%m%d')
		counter_part = f"{self.counter:06d}"
		self.counter += 1

		return f"USR_{date_part}{counter_part}"
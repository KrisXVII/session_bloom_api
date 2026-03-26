from datetime import datetime, timezone

TODAY = datetime.now(timezone.utc)

class IDGenerator:
	_counter = 0
	_last_date = datetime.now(timezone.utc)

	@classmethod
	def generate_user_uid(cls):

		if TODAY > cls._last_date:
			cls._counter = 0
			cls._last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{cls._counter:06d}"
		cls._counter += 1

		return f"USR_{date_part}{counter_part}"

	@classmethod
	def generate_session_uid(cls):

		if TODAY > cls._last_date:
			cls._counter = 0
			cls._last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{cls._counter:06d}"
		cls._counter += 1

		return f"SES_{date_part}{counter_part}"

	@classmethod
	def generate_subsession_uid(cls):

		if TODAY > cls._last_date:
			cls._counter = 0
			cls._last_date = TODAY

		date_part = TODAY.strftime('%y%m%d')
		counter_part = f"{cls._counter:06d}"
		cls._counter += 1

		return f"SUB_{date_part}{counter_part}"

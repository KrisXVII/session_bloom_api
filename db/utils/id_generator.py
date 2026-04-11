from app.models.counter import Counter

class IDGenerator:

	@classmethod
	def _generate(cls, entity_type, prefix):
		"""Base generation method"""
		counter_method = getattr(Counter, f"generate_{entity_type}_code")
		counter = counter_method()
		next_value = counter.next()
		return f"{prefix}_{next_value}"

	@classmethod
	def generate_user_code(cls):
		return cls._generate('user', 'USR')

	@classmethod
	def generate_session_code(cls):
		return cls._generate('session', 'SES')

	@classmethod
	def generate_subsession_code(cls):
		return cls._generate('subsession', 'SUB')
	
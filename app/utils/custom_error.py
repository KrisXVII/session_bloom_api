
class CustomError(Exception):
	def __init__(self, message, code, details):
		self.message = message
		self.code = code
		self.details = details

	def to_dict(self):
		return self.__dict__

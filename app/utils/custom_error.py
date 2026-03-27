
class CustomError(Exception):
	def __init__(self, message, code, description):
		self.message = message
		self.code = code
		self.description = description

	def to_dict(self):
		return self.__dict__

from app import ap

class BaseSerializer:
	__abstract__ = True

	def to_dict(self):
		return self.__dict__

	@classmethod
	def render(cls, obj):
		return cls(obj).to_dict()

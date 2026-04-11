from app.utils.custom_error import CustomError
from app import ap

class BaseSerializer:
	__abstract__ = True

	def to_dict(self):
		return self.__dict__

	@classmethod
	def render(cls, obj):
		return cls(obj).to_dict(), 200  # construct object with cls(obj) which serializes

	@classmethod
	def render_list(cls, obj_list):
		if type(obj_list) is CustomError:
			return obj_list.to_dict(), 400
		return [cls(obj).to_dict() for obj in obj_list], 200

	@classmethod
	def no_content(cls):
		return "", 204

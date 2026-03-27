from db.base import db
from datetime import datetime, timezone
from app import ap
from app.utils.custom_error import CustomError
class BaseModel(db.Model):
	__abstract__ = True

	created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	@classmethod
	def all(cls):
		try:
			records = [obj.to_dict() for obj in cls.query.all()]
			return records
		except Exception as e:
			ap(e.args)
			raise CustomError("Not found", 400, "Error occurred retrieving records from Database")

	@classmethod
	def get(cls, obj_id):
		record = cls.query.get(obj_id)
		if record is None:
			return CustomError(
				"Not found",
				400,
				f"{cls.__name__} record with ID {obj_id} doesn't exist")
		return record

	def save(self):
		"""Save instance to database"""
		db.session.add(self)
		db.session.commit()
		return self

	@classmethod
	def create(cls, params):
		# needed checks, see what is automatically done with ID on postgres
		try:
			new_instance = cls(params)
			new_instance.save()
			return new_instance.to_dict(), 200
		except Exception as e:
			ap(e)
			raise

	def delete(self):
		"""Delete instance from database"""
		db.session.delete(self)
		db.session.commit()

	def to_dict(self):
		result = {}
		for column in self.__table__.columns:
			value = getattr(self, column.name)
			if isinstance(value, datetime):
				value = value.isoformat()
			result[column.name] = value
		return result

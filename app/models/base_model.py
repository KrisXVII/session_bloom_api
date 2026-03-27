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
			records = cls.query.all()
			return records
		except Exception as e:
			return CustomError(
				message=type(e).__name__,
				code=400,
				details=str(e))

	@classmethod
	def get(cls, obj_id):
		record = db.session.get(cls, obj_id)
		if record is None:
			return CustomError(
				message="Not found",
				code=400,
				details=f"{cls.__name__} record with ID {obj_id} doesn't exist")
		return record

	def _save(self):
		db.session.add(self)
		db.session.commit()
		return self

	@classmethod
	def create(cls, **kwargs):
		try:
			new_instance = cls(**kwargs)
			new_instance._save()
			return new_instance
		except Exception as e:
			return CustomError(
				message=type(e).__name__,
				code=400,
				details=str(e)
			)

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

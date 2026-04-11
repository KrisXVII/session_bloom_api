
import db.utils.id_generator
from db.base import db
from datetime import datetime, timezone
from app import ap
from app.utils.custom_error import CustomError
import uuid
import enum


class BaseModel(db.Model):
	__abstract__ = True

	created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
	updated_at = db.Column(
		db.DateTime,
		default=lambda: datetime.now(timezone.utc),
		onupdate=lambda: datetime.now(timezone.utc))

	@property
	def id_s(self):
		"""Get primary key as string - works for any model with 'id'"""
		if hasattr(self, 'id'):
			return str(self.id)
		raise CustomError(
			message=f"Missing attribute on instance of {self.__class__.__name__}",
			code=500,
			details=f"{self.__class__.__name__} does not have attribute id"
		)

	@classmethod
	def all(cls):
		try:
			records = cls.query.all()
			return records
		except Exception as e:
			raise CustomError(
				message=type(e).__name__,
				code=500,
				details=str(e))

	@classmethod
	def find(cls, obj_id):
		try:
			obj_id = uuid.UUID(obj_id)
		except (ValueError, TypeError):
			raise CustomError(
				message="Invalid ID format",
				code=400,
				details=f"Bad request: '{obj_id}' is not a valid UUID"
			)
		record = db.session.get(cls, obj_id)
		return record

	@classmethod
	def create(cls, **kwargs):
		new_instance = cls(**kwargs)
		new_instance._save()
		return new_instance

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, value)
		self._save()
		return self

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def to_dict(self):
		result = {}
		for column in self.__table__.columns:
			value = getattr(self, column.name)
			if isinstance(value, uuid.UUID):
				value = str(value)
			elif isinstance(value, datetime):
				value = value.isoformat()
			elif isinstance(value, enum.Enum):
				value = value.value
			result[column.name] = value
		return result

	def _save(self):
		db.session.add(self)
		db.session.commit()
		return self
	
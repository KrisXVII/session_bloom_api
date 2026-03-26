from db.base import db
from datetime import datetime, timezone

class BaseModel(db.Model):
	__abstract__ = True

	created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	@classmethod
	def all(cls):
		return [u.to_dict() for u in cls.query.all()]

	def save(self):
		"""Save instance to database"""
		db.session.add(self)
		db.session.commit()
		return self

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

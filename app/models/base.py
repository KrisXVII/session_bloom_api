from db.base import db
from datetime import datetime, timezone

class BaseModel(db.Model):
	__abstract__ = True

	created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
	updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	@classmethod
	def all(cls):
		return cls.query.all()

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
		"""Convert model to dictionary"""
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

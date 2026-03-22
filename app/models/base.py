from db.base import db
from datetime import datetime
import uuid

class BaseModel(db.Model):
	__abstract__ = True

	id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
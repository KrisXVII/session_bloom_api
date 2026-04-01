from db.base import db
from datetime import datetime
from db.utils.id_generator import IDGenerator

class Session(db.Model):
	__tablename__ = "sessions"

	# 1 to 1, a Session belong only to a User

	id = db.Column(db.String(20), primary_key=True, default=IDGenerator.generate_session_code)
	activity = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.String(20), db.ForeignKey("users.id"))
	user = db.relationship("User", back_populates="sessions", lazy=True)
	subsessions = db.relationship("Subsession", back_populates="session", lazy=True, cascade='all, delete-orphan')
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)

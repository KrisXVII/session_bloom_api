from db.base import db
from db.utils.id_generator import IDGenerator
from app.models.base import BaseModel

class User(BaseModel):
	__tablename__ = 'users'

	# 1 to many, a User can have many sessions

	id = db.Column(db.String(20), primary_key=True, default=IDGenerator.generate_user_uid)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	sessions = db.relationship("Session", back_populates="user", lazy=True)

from db.base import db
from datetime import datetime
from db.utils.id_generator import IDGenerator

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.String(20), primary_key=True, default=IDGenerator.generate_uid)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)

	# Relationships I'll add later
	# sessions = db.relationship('Session', backref='user', lazy=True, cascade='all, delete-orphan')


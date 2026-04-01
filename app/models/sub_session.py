from db.base import db
from datetime import datetime
from db.utils.id_generator import IDGenerator

class Subsession(db.Model):
	__tablename__ = "subsessions"

	id = db.Column(db.String(20), primary_key=True, default=IDGenerator.generate_subsession_code)
	name = db.Column(db.String(50), nullable=False)
	session_id = db.Column(db.String(20), db.ForeignKey("sessions.id"))
	session = db.relationship("Session", back_populates="subsessions")
	duration = db.Column(db.Integer(), nullable=False)
	break_at_end = db.Column(db.Integer(), default=0)
	order_index = db.Column(db.Integer(), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)

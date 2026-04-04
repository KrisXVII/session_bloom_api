from db.base import db
from datetime import datetime
from db.utils.id_generator import IDGenerator
import uuid
from sqlalchemy.dialects.postgresql import UUID
class Subsession(db.Model):
	__tablename__ = "subsessions"

	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	code = db.Column(db.String(20), unique=True, nullable=False)
	name = db.Column(db.String(50), nullable=False)
	session_id = db.Column(db.String(20), db.ForeignKey("sessions.id"))
	session = db.relationship("Session", back_populates="subsessions")
	duration = db.Column(db.Integer(), nullable=False)
	break_at_end = db.Column(db.Integer(), default=0)
	order_index = db.Column(db.Integer(), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)

	def __init__(self, **kwargs):
		if "code" not in kwargs:
			code = IDGenerator.generate_subsession_code()
			kwargs["code"] = code
		super().__init__(**kwargs)

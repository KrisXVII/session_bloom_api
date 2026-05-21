from db.base import db
from datetime import datetime
from db.utils.id_generator import IDGenerator
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app.models.base_model import BaseModel

class Session(BaseModel):
	__tablename__ = "sessions"

	# 1 to 1, a Session belong only to a User

	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	code = db.Column(db.String(20), unique=True, nullable=False)
	activity = db.Column(db.String(50), nullable=False)
	user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
	subsessions = db.relationship("Subsession", back_populates="session", lazy=True, cascade='all, delete-orphan')
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)

	user = db.relationship("User", back_populates="sessions", lazy=True)

	def __init__(self, **kwargs):
		if "code" not in kwargs:
			code = IDGenerator.generate_session_code()
			kwargs["code"] = code
		super().__init__(**kwargs)


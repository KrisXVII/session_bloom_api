from db.base import db
from db.utils.id_generator import IDGenerator
from app.models.base_model import BaseModel
from sqlalchemy import Enum as SQLEnum
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import UserStatus
from app import ap

class User(BaseModel):
	__tablename__ = 'users'

	# 1 to many, a User can have many sessions
	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	code = db.Column(db.String(20), unique=True, nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	status = db.Column(SQLEnum(UserStatus), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)

	sessions = db.relationship("Session", back_populates="user", lazy=True)

	def __init__(self, **kwargs):
		if "code" not in kwargs:
			code = IDGenerator.generate_user_code()
			kwargs["code"] = code
		super().__init__(**kwargs)

	@property
	def is_active(self):
		return self.status == UserStatus.ACTIVE

	@property
	def is_deleted(self):
		return self.status == UserStatus.DELETED

	@property
	def is_pending(self):
		return self.status == UserStatus.PENDING

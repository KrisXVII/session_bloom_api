from marshmallow import fields
from app.models.session import Session
from .user_schema import UserSchema
from ..helpers.schemifier import schemify

SessionSchema = schemify(
	Session,
	custom_fields={
		'user': fields.Nested(UserSchema),  # Reuse your UserSchema!
	}
)
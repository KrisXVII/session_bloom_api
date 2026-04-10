from marshmallow import fields
from app.models.user import User
from ..helpers.schemifier import schemify
from marshmallow_enum import EnumField
from db import UserStatus

UserSchema = schemify(
	User,
	custom_fields={
		'full_name': fields.String(),
		'status': EnumField(UserStatus, by_value=True),
	},
)


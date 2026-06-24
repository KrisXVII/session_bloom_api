from marshmallow import Schema, fields, validate, EXCLUDE

class UserCreateSchema(Schema):
	class Meta:
		unknown = EXCLUDE
	email = fields.Email(required=True)
	first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class UserUpdateSchema(Schema):
	email = fields.Email()
	status = fields.Str(validate=validate.OneOf(["ACTIVE", "DELETED", "PENDING"]))
	first_name = fields.Str(validate=validate.Length(min=1, max=50))
	last_name = fields.Str(validate=validate.Length(min=1, max=50))

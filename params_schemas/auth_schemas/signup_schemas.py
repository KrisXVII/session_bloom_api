from marshmallow import Schema, fields, validate, EXCLUDE

def validate_password(value):
	if not any(c.isupper() for c in value):
		raise validate.ValidationError("Password must contain uppercase")
	if not any(c.isdigit() for c in value):
		raise validate.ValidationError("Password must contain a number")

class IdentitySchema(Schema):
	class Meta:
		unknown = EXCLUDE

	first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	email = fields.Email(required=True)
	password = fields.Str(
		required=True,
		validate=[validate.Length(min=8), validate_password],
		load_only=True
	)

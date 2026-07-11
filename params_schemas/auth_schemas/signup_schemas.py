from marshmallow import Schema, fields, validate, EXCLUDE

class IdentitySchema(Schema):
	class Meta:
		unknown = EXCLUDE

	first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	email = fields.Email(required=True)
	password = fields.Str(
		required=True,
		validate=validate.Length(min=10, max=50),
		load_only=True
	)

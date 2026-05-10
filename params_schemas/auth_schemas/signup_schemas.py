from marshmallow import Schema, fields, validate, validates, ValidationError
import re

class SignupSchema(Schema):
	first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
	email = fields.Email(required=True)
	password = fields.Str(required=True, validate=validate.Length(min=8))

	# password = fields.Str(required=True)
	# @validates('password')
	# def validate_password(self, value):
	# 	if not re.search(r'\d', value):
	# 		raise ValidationError('La password deve contenere almeno un numero')
	# 	if not re.search(r'[A-Z]', value):
	# 		raise ValidationError('La password deve contenere almeno una maiuscola')

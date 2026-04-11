from marshmallow import Schema, fields

class NotFoundSchema(Schema):
	code = fields.Integer(required=True, validate=lambda n: n == 404)
	details = fields.String(required=True)
	message = fields.String(required=True, validate=lambda m: "not found" in m.lower())

class BadRequestSchema(Schema):
	code = fields.Integer(required=True, validate=lambda n: n == 400)
	details = fields.String(required=True)
	message = fields.String(required=True, validate=lambda m: "Bad request" in m.lower())

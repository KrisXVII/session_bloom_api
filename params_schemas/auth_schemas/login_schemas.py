from marshmallow import Schema, fields, validate, EXCLUDE

class LoginParamsSchema:
    class Meta:
        unknown = EXCLUDE

    identifier = fields.Str(required=True)
    password = fields.Str(required=True)
    method = fields.Str(required=True)

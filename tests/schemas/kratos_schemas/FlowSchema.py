from marshmallow import Schema, fields


class FlowSchema(Schema):
	flow_id = fields.String(required=True)

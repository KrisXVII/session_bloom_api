from marshmallow import ValidationError
import pytest, json
from app import ap

def response_fields(records, *fields):
	return [{field: record[field] for field in fields} for record in records]

def list_fields(records, *fields):
	return [{field: getattr(record, field) for field in fields} for record in records]

def assert_valid_schema(response_data, schema_class, many=False):
	"""Global validation helper to use in tests"""
	if not isinstance(response_data, (dict, list)):
		raise TypeError(
			f"Expected dict or list, got {type(response_data)}. "
			f"Did you pass SQLAlchemy objects instead of response.json?"
		)
	schema = schema_class(many=many)
	try:
		schema.load(response_data)
	except ValidationError as e:
		errors = json.dumps(e.messages, indent=2)
		pytest.fail(f"Schema validation failed:\n{errors}")
	return True

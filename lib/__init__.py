from marshmallow import ValidationError
from flask import request, current_app
from app.utils.custom_error import CustomError

def set_params(schema_class, partial=False):
	data = request.get_json()
	current_app.logger.info(data)
	if not data:
		raise CustomError("Bad request", 400, "No data provided")
	try:
		return schema_class(partial=partial).load(data)
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)

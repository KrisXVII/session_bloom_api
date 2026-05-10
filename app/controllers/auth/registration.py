from flask import Blueprint, request
from app import ap
from params_schemas.auth_schemas.signup_schemas import *
from lib.interfaces.kratos_api import KratosAPI
from marshmallow import ValidationError
from app.models.user import User
from app.utils.custom_error import CustomError

registration_bp = Blueprint("registration", __name__)

@registration_bp.route("/sign_up", methods=["POST"])
def sign_up():
	params = _set_signup_params(SignupSchema)
	existing = User.find_by(email=params["email"])

	if existing:
		raise CustomError(
			message="User already exists",
			code=409,
			details="A user with this email already exists"
		)

	kratos_identity = KratosAPI.create_identity(
		first_name = params["first_name"],
		last_name = params["last_name"],
		email=params["email"],
		password=params["password"]
	)

	return kratos_identity



def _set_signup_params(schema_class):
	try:
		return schema_class().load(request.get_json())
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)
from flask import Blueprint, request
from app import ap
from params_schemas.auth_schemas.signup_schemas import *
from lib.interfaces.kratos_api import KratosAPI
from marshmallow import ValidationError
from app.models.user import User, UserStatus
from app.utils.custom_error import CustomError
from app.serializers.user_serializer import UserSerializer

registration_bp = Blueprint("registration", __name__)

@registration_bp.route("/sign_up", methods=["POST"])
def sign_up():
	params = _set_params(IdentitySchema)
	password = params.pop("password")
	existing = User.find_by(email=params["email"])

	if existing:
		raise CustomError(
			message="User already exists",
			code=409,
			details="A user with this email already exists"
		)

	kratos_identity = KratosAPI.create_identity(
		password=password,
		**params
		email=params["email"],
		password=params["password"]
	)

	del params["password"]

	user = User.create(
		kratos_id=kratos_identity["id"],
		status=UserStatus.ACTIVE,
	    **params
	)
	return UserSerializer.render(user)


def _set_signup_params(schema_class):

def _set_params(schema_class, partial=False):
	data = request.get_json()
	if not data:
		raise CustomError("Bad request", 400, "No data provided")
	try:
		return schema_class(partial=partial).load(data)
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)
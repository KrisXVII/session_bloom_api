from flask import Blueprint, request, current_app
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
	)

	user = User.create(
		kratos_id=kratos_identity["id"],
		status=UserStatus.ACTIVE,
	    **params
	)
	return UserSerializer.render(user)

@registration_bp.route("/<user_id>", methods=["PATCH"])
def update_identity(user_id):

	user = User.find(user_id)
	if not user:
		raise CustomError("Not found", 404, f"User with ID {user_id} doesn't exist.")
	kratos_id = user.kratos_id
	params = _set_params(IdentitySchema, partial=True)
	params.pop("password", None) # defense in depth on altered payloads, unknown = EXCLUDE is first layer
	a = KratosAPI.update_identity(kratos_id, params)
	current_app.logger.error(a)
	user.update(**params)
	return UserSerializer.render(user)


def _set_params(schema_class, partial=False):
	data = request.get_json()
	if not data:
		raise CustomError("Bad request", 400, "No data provided")
	try:
		return schema_class(partial=partial).load(data)
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)
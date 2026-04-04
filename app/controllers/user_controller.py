from flask import Blueprint, request
from ..serializers.user_serializer import UserSerializer
from schemas.user_schemas import UserCreateSchema
from app.models.user import User, UserStatus
from app import ap
from app.utils.custom_error import CustomError
from marshmallow import ValidationError

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
	users = User.all()
	return UserSerializer.render_list(users)

@user_bp.route("/", methods=["POST"])
def create_user():
	params = _set_user_params(UserCreateSchema)
	params["status"] = UserStatus.ACTIVE
	user = User.create(**params)
	return UserSerializer.render(user)

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):

	user = User.find(user_id)
	if user is None:
		raise CustomError(
			message=f"Record not found",
			code=404,
			details=f"User object with ID {user_id} does not exist"
		)
	return UserSerializer.render(user)

# @user_bp.route("/<user_id>", methods=["PUT"]) # Update user

# @user_bp.route("/<user_id>", methods=["POST"]) # Soft delete

##### PRIVATE METHODS #####

def _set_user_params(schema_class):
	try:
		return schema_class().load(request.get_json())
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)


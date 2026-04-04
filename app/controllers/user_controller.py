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
	# TODO define strong params to validate and filter received data
	schema = UserCreateSchema()
	try:
		user_params = schema.load(request.get_json())
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)
	user_params = request.get_json()
	user_params["status"] = UserStatus.ACTIVE
	user = User.create(**user_params)
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



from flask import Blueprint, request
from ..serializers.user_serializer import UserSerializer
from ..serializers.base_serializer import BaseSerializer
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema
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
	user = _set_user(user_id)
	return UserSerializer.render(user)

@user_bp.route("/<user_id>", methods=["PUT"])
def update_user(user_id):
	user = _set_user(user_id)
	params = _set_user_params(UserUpdateSchema)
	user.update(**params)
	return UserSerializer.render(user)

@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
	user = _set_user(user_id)
	user.delete()
	return BaseSerializer.no_content()

##### PRIVATE METHODS #####

def _set_user(user_id):
	user_instance = User.find(user_id)
	if not user_instance:
		raise CustomError(
			message=f"Record not found",
			code=404,
			details=f"User object with ID {user_id} does not exist"
		)
	return user_instance


def _set_user_params(schema_class):
	try:
		return schema_class().load(request.get_json())
	except ValidationError as err:
		raise CustomError("Validation error", 400, err.messages)

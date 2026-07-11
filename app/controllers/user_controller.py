from flask import Blueprint, request
from ..serializers.user_serializer import UserSerializer
from params_schemas.user_schemas import *
from app.models.user import User
from app import ap
from app.utils.custom_error import CustomError
from marshmallow import ValidationError

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
# @swag_from('../swagger/paths/users.yml#create_user')
def get_users():
	users = User.all()
	return UserSerializer.render_list(users)

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
	return UserSerializer.no_content()

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

from flask import Blueprint, request
from ..serializers.user_serializer import UserSerializer
from app.models.user import User
from app import ap

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
	users = User.all()
	return UserSerializer.render_list(users)

@user_bp.route("/create_user", methods=["POST"])
def create_user():
	# TODO define strong params to validate and filter received data
	user_params = request.get_json()

	user = User.create(**user_params)
	return UserSerializer.render(user)

@user_bp.route("/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
	user = User.get(user_id)
	return UserSerializer.render(user)

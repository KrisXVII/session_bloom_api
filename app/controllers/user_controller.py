from flask import Blueprint, request, jsonify
from ..serializers.UserSerializer import UserSerializer
from app.models.user import User
from app import ap

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
	users = User.query.all()
	return jsonify([user.to_dict() for user in users])

@user_bp.route("/", methods=["POST"])
def create_user():
	# TODO define strong params to validate received data
	data = request.get_json()

	user = User.create(data)
	return jsonify(user.to_dict()), 200

@user_bp.route("/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
	user = User.query.get(user_id)
	ap(UserSerializer.render(user))
	return jsonify(UserSerializer.render(user)), 200

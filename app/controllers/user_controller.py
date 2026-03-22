from flask import Blueprint, request, jsonify
from app.models.user import User
from app.services.user_service import UserService
# from app.schemas.user_schema import UserSchema

user_bp = Blueprint("user", __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
	users = User.query.all()
	return jsonify([user.to_dict() for user in users])

@user_bp.route("/", methods=["POST"])
def create_user():
	data = request.get_json()

	# errors = UserSchema().validate(data)
	# if errors:
	# 	return jsonify(errors), 400

	user = UserService.create_user(data)
	return jsonify(user.to_dict()), 200

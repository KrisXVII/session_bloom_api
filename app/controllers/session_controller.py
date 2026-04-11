from flask import Blueprint, request
from ..serializers.session_serializer import SessionSerializer
# from params_schemas.session_schemas import *
from app.models.session import Session
from app import ap
from app.utils.custom_error import CustomError
from marshmallow import ValidationError

session_bp = Blueprint("session", __name__)

@session_bp.route("/", methods=["GET"])
def get_sessions():
	sessions = Session.all()
	return SessionSerializer.render_list(sessions)

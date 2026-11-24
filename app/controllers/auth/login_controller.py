from flask import Blueprint
from lib import set_params
from lib.interfaces.kratos_public_api import KratosPublicAPI
from params_schemas.auth_schemas.login_schemas import LoginParamsSchema
from app.serializers.kratos_serializers.session_login_serializer import SessionLoginSerializer

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    params = set_params(LoginParamsSchema)
    flow_id = KratosPublicAPI.create_login_flow(refresh=False)["id"]
    response = KratosPublicAPI.submit_login_flow(
        flow_id=flow_id,
        identifier=params["identifier"],
        password=params["password"],
        method="password"
    )

    return SessionLoginSerializer.render(response)

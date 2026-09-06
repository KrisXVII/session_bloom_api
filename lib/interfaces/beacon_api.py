from lib.api_client import ApiClient
from config.config_env import Config
from datetime import datetime, timezone
from flask import current_app
import traceback
# from app import ap

BEACON_LOCAL = ApiClient(Config.BEACON_LOCAL)


class BeaconApi:

    @classmethod
    def send_event(cls, event, request, posthog_event_id):

        payload = cls._build_event_payload(event, request, posthog_event_id)

        BEACON_LOCAL.post(
            "/api/echoEvent",
            expected=(200,),
            json=payload,
            error_message="Failed to reach Beacon"
        )

    @staticmethod
    def _build_event_payload(event, request, posthog_event_id):
        payload = {
            "error_type": type(event).__name__,
            "method": request.method,
            "route": str(request.url_rule),
            "environment": current_app.config["FLASK_ENV"],
            "message": str(event),
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "frames": [{"file": f.filename, "line": f.lineno, "func": f.name}
                       for f in traceback.extract_tb(event.__traceback__)],
            "posthog_event_id": posthog_event_id,
        }

        return payload

    # service            "session_bloom_api"
    # environment        "development"
    # error_type         "ZeroDivisionError"
    # message            "division by zero"
    # route              "/"
    # method             "GET"
    # frames             [{file, line, func}, ...]
    # occurred_at        "2026-09-06T13:45:05Z"
    # posthog_event_id   "0b654f03-..."
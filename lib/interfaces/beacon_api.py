from lib.api_client import ApiClient
from config.config_env import Config
# from app import ap

BEACON_LOCAL = ApiClient(Config.BEACON_LOCAL)


class BeaconApi:

    @classmethod
    def send_event(cls, event):

        BEACON_LOCAL.post(
            "/api/echoEvent",
            expected=(200,),
            json={"event": event},
            error_message="Failed to reach Beacon"
        )

from app.serializers.base_serializer import BaseSerializer

class SessionLoginSerializer(BaseSerializer):
    def __init__(self, session):
        self.session_token = session["session"]["id"]

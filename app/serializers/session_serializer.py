from app.serializers.base_serializer import BaseSerializer

class SessionSerializer(BaseSerializer):
	def __init__(self, session):
		self.id = str(session.id)
		self.code = session.code
		self.activity = session.activity
		self.user = session.user.to_dict()
		self.subsessions = session.subsessions
		self.created_at = session.created_at.isoformat()
		self.updated_at = session.created_at.isoformat()

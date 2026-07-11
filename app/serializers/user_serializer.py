from app.serializers.base_serializer import BaseSerializer

class UserSerializer(BaseSerializer):
	def __init__(self, user):
		self.id = str(user.id)
		self.kratos_id = user.kratos_id
		self.code = user.code
		self.first_name = user.first_name
		self.last_name = user.last_name
		self.full_name = self.build_name()
		self.email = user.email
		self.status = user.status.value
		self.created_at = user.created_at.isoformat()
		self.updated_at = user.created_at.isoformat()

	def build_name(self):
		return self.first_name + " " + self.last_name

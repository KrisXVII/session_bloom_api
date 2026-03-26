from app.serializers.BaseSerializer import BaseSerializer

class UserSerializer(BaseSerializer):
	def __init__(self, user):
		self.id = user.id
		self.first_name = user.first_name
		self.last_name = user.last_name
		self.full_name = self.build_name()
		self.email = user.email
		self.created_at = user.created_at.isoformat()
		self.updated_at = user.created_at.isoformat()

	def build_name(self):
		return self.first_name + " " + self.last_name



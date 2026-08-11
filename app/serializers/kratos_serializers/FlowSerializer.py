from app.serializers.base_serializer import BaseSerializer

class FlowSerializer(BaseSerializer):
	def __init__(self, flow):
		self.flow_id = flow["id"]
		
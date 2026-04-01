from db.utils.id_generator import IDGenerator
from tests.conftest import focus

class TestIDGenerator:

	def test_simple_generation(self, session):
		user_id = IDGenerator.generate_user_code()
		assert user_id.startswith('USR_')

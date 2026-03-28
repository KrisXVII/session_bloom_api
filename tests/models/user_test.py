from app.models.user import User
from tests.conftest import focus

class TestUserModel:

	def test_create_user(self, db):
		"""Test creating a user"""
		user = User(
			email="test@example.com",
			first_name="John",
			last_name="Doe"
		)
		db.session.add(user)
		db.session.commit()

		assert user.id is not None
		assert user.email == "test@example.com"

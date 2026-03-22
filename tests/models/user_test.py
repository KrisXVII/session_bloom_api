import pytest
from app.models.user import User
from tests.factories.user_factory import UserFactory

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

	# def test_user_to_dict(self, db):
	# 	"""Test user to_dict method"""
	# 	user = UserFactory()
	# 	db.session.add(user)
	# 	db.session.commit()
	#
	# 	user_dict = user.to_dict()
	#
	# 	assert user_dict['id'] == user.id
	# 	assert user_dict['email'] == user.email
	# 	assert 'created_at' in user_dict
	#
	# def test_user_repr(self, db):
	# 	"""Test user string representation"""
	# 	user = User(email="test@example.com", first_name="John", last_name="Doe")
	# 	assert repr(user) == "<User test@example.com>"

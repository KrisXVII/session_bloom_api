import pytest
from app.services.user_service import UserService
from tests.factories.user_factory import UserFactory

class TestUserService:

	def test_create_user(self, db):
		"""Test service creates user"""
		data = {
			"email": "test@example.com",
			"first_name": "John",
			"last_name": "Doe"
		}

		user = UserService.create_user(data)

		assert user.email == "test@example.com"
		assert user.id is not None

	# def test_create_user_duplicate_email(self, db):
	# 	"""Test service rejects duplicate email"""
	# 	user = UserFactory(email="duplicate@example.com")
	# 	db.session.add(user)
	# 	db.session.commit()
	#
	# 	data = {
	# 		"email": "duplicate@example.com",
	# 		"first_name": "Jane",
	# 		"last_name": "Smith"
	# 	}
	#
	# 	with pytest.raises(ValueError, match="Email already exists"):
	# 		UserService.create_user(data)
	#
	# def test_update_user(self, db):
	# 	"""Test service updates user"""
	# 	user = UserFactory(first_name="Original")
	# 	db.session.add(user)
	# 	db.session.commit()
	#
	# 	updated = UserService.update_user(user, {"first_name": "Updated"})
	#
	# 	assert updated.first_name == "Updated"
	#
	# def test_get_user_sessions(self, db):
	# 	"""Test service gets user sessions"""
	# 	user = UserFactory()
	# 	db.session.add(user)
	# 	db.session.commit()
	#
	# 	sessions = UserService.get_user_sessions(user.id)
	# 	assert sessions == []  # Initially empty
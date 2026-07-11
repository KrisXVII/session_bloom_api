import pytest
import uuid
from app.models.user import User
from app.utils.custom_error import CustomError
from db import UserStatus
from tests.factories.user_factory import UserFactory
from app import ap
from ..conftest import focus

class TestBaseModel:

	def test_find_returns_user_by_uuid(self, session):
		"""Test find() returns user when ID exists"""
		user = UserFactory.create()

		found = User.find(user.id_s)
		assert found is not None
		assert found.id_s == user.id_s

	def test_find_returns_none_for_missing(self, session):
		"""Test find() returns None for non-existent ID"""
		non_existent = uuid.uuid4()

		# Also with string
		found = User.find(str(non_existent))
		assert found is None

	def test_find_raises_for_invalid_uuid_format(self, session):
		"""Test find() raises CustomError for invalid UUID format"""
		with pytest.raises(CustomError) as exc:
			User.find("not-a-uuid-at-all")
		assert exc.value.code == 400
		assert "Invalid ID format" in exc.value.message

	def test_all_returns_list(self, session):
		"""Test all() returns list of all users"""
		# Clear existing
		for u in User.all():
			u.delete()

		assert len(User.all()) == 0

		# Create users
		user1 = UserFactory.create()
		user1.update(status=UserStatus.ACTIVE)
		user2 = UserFactory.create()
		user2.update(status=UserStatus.DELETED)


		users = User.all()
		assert len(users) == 2
		assert user1.id_s in [u.id_s for u in users]
		assert user2.id_s in [u.id_s for u in users]

	def test_create_saves_and_returns_instance(self, session):
		"""Test create() saves and returns instance"""
		user = UserFactory.create()

		assert user.id_s is not None
		assert user.created_at is not None

		# Verify saved in DB
		found = User.find(user.id_s)
		assert found is not None
		# assert found.status == 0
		assert found.email == user.email

	def test_update_modifies_and_saves(self, session):
		"""Test update() modifies fields and saves"""
		user = UserFactory.create()

		user.update(first_name="Updated", last_name="Changed")

		assert user.first_name == "Updated"
		assert user.last_name == "Changed"

		# Verify persisted
		found = User.find(user.id_s)
		assert found.first_name == "Updated"
		assert found.last_name == "Changed"

	def test_update_ignores_unknown_fields(self, session):
		"""Test update() ignores fields that don't exist"""
		user = UserFactory.create()

		# This should not raise error
		user.update(nonexistent_field="value", another_fake=123)

	def test_delete_removes_record(self, session):
		"""Test delete() removes record from database"""
		user = UserFactory.create()

		# Verify exists
		assert User.find(user.id_s) is not None

		# Delete
		user.delete()

		# Verify gone
		assert User.find(user.id_s) is None

	def test_to_dict_returns_formatted_dict(self, session):
		"""Test to_dict() returns correctly formatted dictionary"""
		user = UserFactory.create()

		result = user.to_dict()

		assert isinstance(result, dict)
		assert str(result['id']) == str(user.id_s)
		assert result['email'] == user.email
		assert result['first_name'] == user.first_name
		assert result['last_name'] == user.last_name
		assert result['status'] == user.status.value
		assert 'created_at' in result
		assert 'updated_at' in result
		assert isinstance(result['created_at'], str)  # Should be ISO format

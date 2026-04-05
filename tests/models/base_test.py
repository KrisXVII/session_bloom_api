import pytest
import uuid
from app.models.user import User
from app.utils.custom_error import CustomError
from db import UserStatus
from app import ap

class TestBaseModel:

	def test_find_returns_user_by_uuid(self, session):
		"""Test find() returns user when ID exists"""
		user = User.create(
			email="test@example.com",
			first_name="Test",
			last_name="User",
			status=UserStatus.ACTIVE
		)

		found = User.find(str(user.id))
		assert found is not None
		assert found.id == user.id

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
		user1 = User.create(email="test1@example.com", first_name="Test1", last_name="User1", status=UserStatus.ACTIVE)
		user2 = User.create(email="test2@example.com", first_name="Test2", last_name="User2", status=UserStatus.DELETED)

		users = User.all()
		assert len(users) == 2
		assert user1.id in [u.id for u in users]
		assert user2.id in [u.id for u in users]

	def test_create_saves_and_returns_instance(self, session):
		"""Test create() saves and returns instance"""
		user = User.create(
			email="create_test@example.com",
			first_name="Create",
			last_name="Test",
			status=UserStatus.ACTIVE
		)

		assert user.id is not None
		assert user.created_at is not None

		# Verify saved in DB
		found = User.find(str(user.id))
		assert found is not None
		# assert found.status == 0
		assert found.email == "create_test@example.com"

	def test_update_modifies_and_saves(self, session):
		"""Test update() modifies fields and saves"""
		user = User.create(
			email="update_test@example.com",
			first_name="Original",
			last_name="Name",
			status=UserStatus.ACTIVE
		)

		user.update(first_name="Updated", last_name="Changed")

		assert user.first_name == "Updated"
		assert user.last_name == "Changed"

		# Verify persisted
		found = User.find(str(user.id))
		assert found.first_name == "Updated"
		assert found.last_name == "Changed"

	def test_update_ignores_unknown_fields(self, session):
		"""Test update() ignores fields that don't exist"""
		user = User.create(
			email="ignore_test@example.com",
			first_name="Test",
			last_name="User",
			status=UserStatus.ACTIVE
		)

		# This should not raise error
		user.update(nonexistent_field="value", another_fake=123)

		# Original values unchanged
		assert user.first_name == "Test"
		assert user.last_name == "User"

	def test_delete_removes_record(self, session):
		"""Test delete() removes record from database"""
		user = User.create(
			email="delete_test@example.com",
			first_name="Delete",
			last_name="Me",
			status=UserStatus.ACTIVE
		)
		user_id = user.id

		# Verify exists
		assert User.find(str(user_id)) is not None

		# Delete
		user.delete()

		# Verify gone
		assert User.find(str(user_id)) is None

	def test_to_dict_returns_formatted_dict(self, session):
		"""Test to_dict() returns correctly formatted dictionary"""
		user = User.create(
			email="dict_test@example.com",
			first_name="Dict",
			last_name="Test",
			status=UserStatus.ACTIVE
		)

		result = user.to_dict()

		assert isinstance(result, dict)
		assert str(result['id']) == str(user.id)
		assert result['email'] == "dict_test@example.com"
		assert result['first_name'] == "Dict"
		assert result['last_name'] == "Test"
		assert result['status'] == 0
		assert 'created_at' in result
		assert 'updated_at' in result
		assert isinstance(result['created_at'], str)  # Should be ISO format

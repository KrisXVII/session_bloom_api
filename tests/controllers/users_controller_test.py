import uuid

import pytest

from tests.conftest import focus  # Leave here for focus
from ..factories.user_factory import UserFactory
from faker import Faker
from ..helpers import response_fields, list_fields
from app import ap
from app.models.user import User


fake = Faker()


class TestUserController:
	class TestGetUsers:

		@pytest.fixture
		def users(self):
			return UserFactory.create_batch(3)

		def test_get_users(self, client, users):
			"""Test GET /users when no users exist"""
			response = client.get('/users/')
			assert response.status_code == 200
			assert len(response.json) == 3
			assert response_fields(response.json, "code") == list_fields(users, "code")

		def test_get_users_empty(self, client):
			response = client.get('/users/')
			assert response.status_code == 200
			assert response.json == []

	class TestCreateUser:
		def test_create_user(self, client):
			data = {
				"first_name": fake.first_name(),
				"last_name": fake.last_name(),
				"email": fake.email(),
			}

			response = client.post('/users/', json=data)

			assert response.status_code == 200
			assert response.json['first_name'] == data["first_name"]
			assert response.json['last_name'] == data["last_name"]
			assert response.json['email'] == data["email"]

	class TestGetUser:

		@pytest.fixture(autouse=True)
		def create_user(self, db):
			self.user = UserFactory.create()

		def test_get_user(self, client):
			# TODO enter params schema
			response = client.get(f"users/{self.user.id}")
			assert response.status_code == 200
			assert response.json["id"] == str(self.user.id)
			assert response.json["code"] == self.user.code

		# TODO response schema

		def test_record_not_found(self, client):
			# TODO enter params schema
			response = client.get(f"/users/{uuid.uuid4()}")
			assert response.status_code == 404

		# TODO response schema

		def test_invalid_type(self, client):
			response = client.get(f"/users/9999")
			assert response.status_code == 400
			assert response.json["message"] == "Invalid ID format"

	class TestUpdateUser:

		def test_update_user(self, client):
			user = UserFactory.create()
			data = {
				"email": fake.email(),
			}

			response = client.put(f"/users/{user.id}", json=data)

			assert response.status_code == 200
			assert response.json["id"] == str(user.id)
			assert response.json["email"] == data["email"]

		def test_update_non_existent_user(self, client):
			UserFactory.create()
			data = {
				"email": fake.email(),
			}
			wrong_uuid = uuid.uuid4()
			response = client.put(f"/users/{wrong_uuid}", json=data)

			assert response.status_code == 404
			assert response.json["message"] == "Record not found"
			assert response.json["details"] == f"User object with ID {wrong_uuid} does not exist"

	class TestDeleteUser:

		def test_delete_user(self, client):
			user = UserFactory.create()

			response = client.delete(f"/users/{user.id}")

			assert response.status_code == 204
			assert len(User.all()) == 0
			assert response.json is None


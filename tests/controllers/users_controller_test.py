import json

import sqlalchemy.util.queue
from tests.conftest import focus # Leave here for focus
from ..factories.user_factory import UserFactory
from faker import Faker
from ..helpers import response_fields, list_fields
from app import ap
fake = Faker()

class TestUserController:

	class TestGetUsers:
		def test_get_users(self, client):
			users = UserFactory.create_batch(3)
			"""Test GET /users when no users exist"""
			response = client.get('/users/')
			assert response.status_code == 200
			assert len(response.json) == 3
			assert response_fields(response.json, "id") == list_fields(users, "id")

		def test_get_users_empty(self, client):
			response = client.get('/users/')
			assert response.status_code == 200
			assert response.json == []

	@focus
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

		def test_get_user(self, client):
			# TODO enter params schema
			user = UserFactory.create()
			response = client.get(f"users/{user.id}")
			assert response.status_code == 200
			assert response.json["id"] == user.id
			# TODO response schema

		def test_record_not_found(self, client):
			# TODO enter params schema
			UserFactory.create()
			response = client.get(f"users/9999")
			assert response.status_code == 400
			assert response.json["message"] == "Not found"
			assert response.json["details"] == "User record with ID 9999 doesn't exist"
			# TODO response schema

import json
import pytest as p
from tests.conftest import focus
from app.models.user import User
from ..factories.user_factory import UserFactory

class TestUserController:

	def test_get_users_empty(self, client):
		"""Test GET /users when no users exist"""
		response = client.get('/users/')
		assert response.status_code == 200
		assert response.json == []

	def test_create_user(self, client):
		data = {
			"email": "test@example.com",
			"first_name": "John",
			"last_name": "Doe"
		}

		response = client.post('/users/', json=data)
		assert response.status_code == 200

		data = response.json
		assert data['email'] == "test@example.com"
		assert data['first_name'] == "John"

	class TestGetUser:

		def test_get_user(self, client):
			# TODO enter params schema
			user = UserFactory.create()
			response = client.get(f"users/get_user/{user.id}")
			assert response.status_code == 200
			assert response.json["id"] == user.id
			# TODO response schema

		@focus
		def test_not_found(self, client):
			# TODO enter params schema
			user = UserFactory.create()
			response = client.get(f"users/get_user/9999")
			assert response.status_code == 404
			# assert response.json["id"] == user.id
			# TODO response schema

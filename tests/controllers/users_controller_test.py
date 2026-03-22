import json
import pytest
from tests.factories.user_factory import UserFactory

class TestUserController:

	def test_get_users_empty(self, client):
		"""Test GET /users when no users exist"""
		response = client.get('/users/')
		assert response.status_code == 200
		assert response.json == []

	def test_create_user(self, client, db):
		data = {
			"email": "test@example.com",
			"first_name": "John",
			"last_name": "Doe"
		}

		response = client.post('/users/', json=data)
		assert response.status_code == 201

		data = response.json
		assert data['email'] == "test@example.com"
		assert data['first_name'] == "John"

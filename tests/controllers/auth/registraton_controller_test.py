import uuid
from faker import Faker

from tests.factories.user_factory import UserFactory
from tests.helpers import *
from tests.schemas.user_schema import UserSchema
from tests.schemas.error_schemas import *
from app.models.user import User
from tests.conftest import focus
import responses
from app import ap
from tests.stubs.kratos_stubs import KratosStubs

fake = Faker()

class TestRegistrationController:

	class TestCreateUser:

		@responses.activate
		def test_sign_up(self, client):
			KratosStubs.create_identity()

			data = {
				"first_name": fake.first_name(),
				"last_name": fake.last_name(),
				"email": fake.email(),
				"password": fake.password(length=12)
			}

			response = client.post('/auth/sign_up', json=data)
			assert_valid_schema(response.json, UserSchema)

			assert response.json['first_name'] == data["first_name"]
			assert response.json['last_name'] == data["last_name"]
			assert response.json['email'] == data["email"]
			assert response.json["kratos_id"] is not None

	# class TestUpdateUser:
	#
	# 	@focus
	# 	@responses.activate
	# 	def test_patch_identity(self, client):
	# 		user = UserFactory.create()
	# 		data = {
	# 			"first_name": fake.first_name(),
	# 			"last_name": fake.last_name(),
	# 			"email": fake.email(),
	# 			# "password": fake.password(length=12)
	# 		}
	#
	# 		KratosStubs.patch_identity(user.kratos_id)
	#
	# 		response = client.patch(f"/auth/{user.id}", json=data)
	# 		ap(response.json)
	# 		assert_valid_schema(response.json, UserSchema)

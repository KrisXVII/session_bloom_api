from faker import Faker
from tests.factories.user_factory import UserFactory
from tests.helpers import *
from tests.schemas.user_schema import UserSchema
from tests.schemas.kratos_schemas.FlowSchema import FlowSchema
from tests.schemas.error_schemas import *
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
				"password": fake.password(length=10)
			}

			response = client.post('/auth/sign_up', json=data)
			assert_valid_schema(response.json, UserSchema)

			assert response.json['first_name'] == data["first_name"]
			assert response.json['last_name'] == data["last_name"]
			assert response.json['email'] == data["email"]
			assert response.json["kratos_id"] is not None

	class TestUpdateUser:

		@responses.activate
		def test_patch_identity(self, client):
			user = UserFactory.create()
			data = {
				"first_name": fake.first_name(),
				"last_name": fake.last_name(),
				"email": fake.email()
			}

			KratosStubs.patch_identity(user.kratos_id)

			response = client.patch(f"/auth/{user.id}", json=data)

			assert_valid_schema(response.json, UserSchema)
			assert response.json['first_name'] == data["first_name"]
			assert response.json['last_name'] == data["last_name"]
			assert response.json['email'] == data["email"]

	class TestAuthFlow:

		@responses.activate
		def test_create_auth_flow(self, client):
			KratosStubs.get_verification_flow()
			response = client.get("/auth/auth_flow")
			assert_valid_schema(response.json, FlowSchema)
			assert response.status_code == 200
			assert response.json["flow_id"] == "add86485-f2f8-46bb-b480-76bfe36380e3"

		@responses.activate
		def test_send_code(self, client):
			flow_id = str(fake.uuid4())
			email = fake.email()
			KratosStubs.send_verification_code(flow_id)

			response = client.post(
				"/auth/send_verification_code",
				json={"flow_id": flow_id, "email": email},
			)

			assert response.status_code == 204
			request = responses.calls[0].request
			assert f"flow={flow_id}" in request.url
			assert json.loads(request.body)["email"] == email

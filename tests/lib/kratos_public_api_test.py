import responses, json
from faker import Faker
from lib.interfaces.kratos_public_api import KratosPublicAPI
from tests.stubs.kratos_stubs import KratosStubs
from tests.conftest import focus
from app import ap
fake = Faker()

class TestKratosPublicApi:

	@responses.activate
	def test_start_verification_flow(self):
		KratosStubs.get_verification_flow()

		response = KratosPublicAPI.start_verification_flow()
		assert "id" in response

	@responses.activate
	def test_send_verification_code(self):
		flow_id = str(fake.uuid4())
		email = fake.email()
		KratosStubs.send_verification_code(flow_id=flow_id)

		KratosPublicAPI.send_verification_code(flow_id=flow_id, email=email)

		request = responses.calls[0].request
		assert f"flow={flow_id}" in request.url
		assert json.loads(request.body) == {"method": "code", "email": email}

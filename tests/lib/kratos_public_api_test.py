import responses
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

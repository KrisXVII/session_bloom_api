import responses
from faker import Faker
from lib.interfaces.kratos_admin_api import KratosAdminAPI
from tests.stubs.kratos_stubs import KratosStubs
from tests.conftest import focus
from app import ap
fake = Faker()

@focus
class TestKratosAdminApi:

	@responses.activate
	def test_create_identity(self):
		KratosStubs.create_identity()

		result = KratosAdminAPI.create_identity(
			first_name=fake.first_name(),
			last_name=fake.last_name(),
			email=fake.email(),
			password=fake.password(length=10)
		)

		assert result["id"] is not None


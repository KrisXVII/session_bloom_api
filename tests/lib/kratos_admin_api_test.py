import responses
import json
from faker import Faker
from lib.interfaces.kratos_admin_api import KratosAdminAPI
from tests.stubs.kratos_stubs import KratosStubs
from tests.conftest import focus
from app import ap
fake = Faker()

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

	@focus
	@responses.activate
	def test_sends_correct_patch(self, app):
		identity_id = str(fake.uuid4())
		KratosStubs.patch_identity(identity_id=identity_id)

		KratosAdminAPI.update_identity(identity_id, {"first_name": "Jack", "last_name": "Sparrow"})

		assert len(responses.calls) == 1 # exactly one request went out

		request = responses.calls[0].request
		assert request.method == "PATCH"
		assert request.url.endswith(f"/admin/identities/{identity_id}")

		sent = json.loads(request.body) # the body built in the code
		assert {"op": "replace", "path": "/traits/first_name", "value": "Jack"} in sent
		assert {"op": "replace", "path": "/traits/last_name", "value": "Sparrow"} in sent

	
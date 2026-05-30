import responses
from lib.interfaces.kratos_api import KRATOS_ADMIN_URL
import json
import os
from app import ap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json_responses")

class KratosStubs:

	@classmethod
	def create_identity(cls):

		with open(os.path.join(JSON_DIR, "identity_created.json"), "r", encoding="utf-8") as f:
			response_json = json.load(f)

		responses.add(
			responses.POST,
			f"{KRATOS_ADMIN_URL}/admin/identities",
			json=response_json,
			status=201
		)

	@classmethod
	def patch_identity(cls, identity_id):
		with open(os.path.join(JSON_DIR, "identity_updated.json"), "r", encoding="utf-8") as f:
			response_json = json.load(f)

		responses.add(
			responses.PATCH,
			f"{KRATOS_ADMIN_URL}/admin/identities/{identity_id}",
			json=response_json,
			status=201
		)

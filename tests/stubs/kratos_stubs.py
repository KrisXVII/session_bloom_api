import responses
from config.config_env import Config
import json
import os
from app import ap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json_responses")
KRATOS_BASE = Config.KRATOS_ADMIN_URL

class KratosStubs:

	@classmethod
	def create_identity(cls):

		with open(os.path.join(JSON_DIR, "identity_created.json"), "r", encoding="utf-8") as f:
			response_json = json.load(f)

		responses.add(
			responses.POST,
			f"{KRATOS_BASE}/admin/identities",
			json=response_json,
			status=201
		)

	@classmethod
	def patch_identity(cls, identity_id):
		with open(os.path.join(JSON_DIR, "identity_updated.json"), "r", encoding="utf-8") as f:
			response_json = json.load(f)

		responses.add(
			responses.PATCH,
			f"{KRATOS_BASE}/admin/identities/{identity_id}",
			json=response_json,
			status=200
		)

	@classmethod
	def put_identity(cls, identity_id):
		with open(os.path.join(JSON_DIR, "password_identity_updated.json"), "r", encoding="utf-8") as f:
			response_json = json.load(f)

		responses.add(
			responses.PUT,
			f"{KRATOS_BASE}/admin/identities/{identity_id}",
			json=response_json,
			status=200
		)

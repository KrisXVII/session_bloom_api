import requests
from flask import current_app
from app.utils.custom_error import CustomError

KRATOS_ADMIN_URL = "https://kratos:4434"

class KratosAPI:

	@classmethod
	def create_identity(cls, first_name, last_name, email, password):

		data = cls._build_payload(first_name, last_name, email, password)

		try:
			response = requests.post(
				f"{KRATOS_ADMIN_URL}/admin/identities",
				json=data,
				timeout=10
			)

			if response.status_code == 201:
				return response.json()
			else:
				error = response.json()
				current_app.logger.error(f"Kratos error: {error}")
				raise CustomError(
					message="Registration failed",
					code=400,
					details=error.get('message', 'Unknown error from auth service')
				)
		except requests.RequestException as e:
			current_app.logger.error(f"Kratos connection failed: {e}")
			raise CustomError(
				message="Auth service unavailable",
				code=503,
				details="Unable to reach authentication service"
			)


	@classmethod
	def get_identity(cls, identity_id):
		try:
			response = requests.get(
				f"{KRATOS_ADMIN_URL}/admin/identities/{identity_id}",
				timeout=5
			)

			if response.status_code == 200:
				return response.json()
			return None

		except requests.RequestException:
			return None

	@staticmethod
	def _build_payload(first_name, last_name, email, password):
		payload = {
			"schema_id": "default",
			"traits": {
				"email": email,
				"first_name": first_name,
				"last_name": last_name,
			},
			"credentials": {
				"password": {
					"config": {
						"password": password
					}
				}
			}
		}

		return payload

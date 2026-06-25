import requests
from flask import current_app
from app.utils.custom_error import CustomError
from app import ap

KRATOS_PUBLIC_URL = "http://kratos_ory:4433"

class KratosPublicAPI:

	@classmethod
	def start_verification_flow(cls):
		try:
			response = requests.get(
				f"{KRATOS_PUBLIC_URL}/self-service/verification/api",
				headers={"Accept": "application/json"},
				allow_redirects=False,
				timeout=10
			)

			if response.status_code == 200:
				return response.json()
			else:
				error = response.json()
				current_app.logger.error(f"Kratos error: {error}")
				raise CustomError(
					message="Auth flow creation failed",
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
	def send_verification_code(cls, flow_id, email):
		try:
			response = requests.post(
				f"{KRATOS_PUBLIC_URL}/self-service/verification?flow={flow_id}",
				json={
					"method": "code",
					"email": email
				},
				headers={"Accept": "application/json"},
				allow_redirects=False,
				timeout=10
			)

			if response.status_code == 200:
				return response.json()
			else:
				error = response.json()
				current_app.logger.error(f"Kratos error: {error}")
				raise CustomError(
					message="Code issuing failed",
					code=400,
					details=error.get('message', 'Unknown error from auth service')
				)
		except requests.RequestException as e:
			current_app.logger.error(f"Kratos connection failed: {e}")
			raise CustomError(
				message=e,
				code=503,
				details="Unable to reach authentication service"
			)

	@classmethod
	def verify_code(cls, flow_id, code):
		try:
			response = requests.post(
				f"{KRATOS_PUBLIC_URL}/self-service/verification?flow={flow_id}",
				json={
					"method": "code",
					"code": code
				},
				headers={"Accept": "application/json"},
				allow_redirects=False,
				timeout=10
			)

			if response.status_code == 200:
				return response.json()
			else:
				error = response.json()
				current_app.logger.error(f"Kratos error: {error}")
				raise CustomError(
					message="Code verification failed",
					code=400,
					details=error.get('message', 'Unknown error from auth service')
				)
		except requests.RequestException as e:
			current_app.logger.error(f"Kratos connection failed: {e}")
			raise CustomError(
				message=e,
				code=503,
				details="Unable to reach authentication service"
			)

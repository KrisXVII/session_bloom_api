from lib.api_client import ApiClient
from config.config_env import Config
from app import ap

KRATOS_PUBLIC = ApiClient(Config.KRATOS_PUBLIC_URL)

class KratosPublicAPI:

	@classmethod
	def start_verification_flow(cls):

		response = KRATOS_PUBLIC.get(
			"/self-service/verification/api",
			expected=(200,),
			error_message="Auth flow creation failed"
		)

		return response.json()


	@classmethod
	def send_verification_code(cls, flow_id, email):

		response = KRATOS_PUBLIC.post(
			f"/self-service/verification?flow={flow_id}",
			json={
				"method": "code",
				"email": email
			},
			expected=(200,),
			error_message="Code issuing failed.",
			allow_redirects=False,
		)

		return response.json()

	@classmethod
	def verify_code(cls, flow_id, code):

		response = KRATOS_PUBLIC.post(
			f"/self-service/verification?flow={flow_id}",
			json={
				"method": "code",
				"code": code
			},
			expected=(200,),
			error_message="Code verification failed",
			allow_redirects=False
		)

		return response.json()

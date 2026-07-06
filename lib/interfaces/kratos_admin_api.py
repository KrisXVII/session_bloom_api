from lib.api_client import ApiClient
from config.config_env import Config
from app import ap

KRATOS_ADMIN = ApiClient(Config.KRATOS_ADMIN_URL)

class KratosAdminAPI:

	@classmethod
	def create_identity(cls, first_name, last_name, email, password):

		data = cls._build_payload(first_name, last_name, email, password)

		response = KRATOS_ADMIN.post(
			"/admin/identities",
			json=data,
			expected=(201,),
			error_message="Registration failed"
		)
		return response.json()

	@classmethod
	def get_identity(cls, identity_id):

		response = KRATOS_ADMIN.get(
			f"/admin/identities/{identity_id}",
			expected=(200,),
			error_message="Auth service unavailable."
		)

		return response.json()

	@classmethod
	def update_identity(cls, identity_id, update_params):
		data = cls._format_params_tolist(update_params)

		response = KRATOS_ADMIN.patch(
			f"/admin/identities/{identity_id}",
			json=data,
			expected=(200,),
			error_message="Auth service unavailable."
		)

		return response.json()

	# @classmethod
	# def update_password(cls, identity_id, update_params):
	# 	data = cls._build_payload(update_params)
	# 	try:
	# 		response = requests.put(
	# 			f"{KRATOS_ADMIN_URL}/admin/identities/{identity_id}",
	# 			json=data,
	# 			timeout=5
	# 		)
	# 		if response.status_code == 200:
	# 			return response.json()
	# 		return None
	#
	# 	except requests.RequestException as e:
	# 		current_app.logger.error(f"Kratos connection failed: {e}")
	# 		raise CustomError(
	# 			message="Auth service unavailable",
	# 			code=503,
	# 			details="Unable to reach authentication service"
	# 		)

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

	@staticmethod
	def _format_params_tolist(params):
		patch_data = [
			{
				"op": "replace",
				"path": f"/traits/{key}",
				"value": value
			} for key, value in params.items()
		]
		return patch_data

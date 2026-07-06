import requests
from flask import current_app
from app.utils.custom_error import CustomError

class ApiClient:

	def __init__(self, base_url, timeout=10):
		self.base_url = base_url
		self.timeout = timeout
		self.session = requests.Session()

	def get(self, path, **kwargs): return self._request("GET", path, **kwargs)
	def post(self, path, **kwargs): return self._request("POST", path, **kwargs)
	def put(self, path, **kwargs): return self._request("PUT", path, **kwargs)
	def patch(self, path, **kwargs): return self._request("PATCH", path, **kwargs)
	def delete(self, path, **kwargs): return self._request("DELETE", path, **kwargs)

	def _request(self, method, path, expected=(200, 201), error_message="Request failed", **kwargs):
		kwargs.setdefault("timeout", self.timeout)
		headers = kwargs.pop("headers", {})
		headers.setdefault("Accept", "application/json")

		url = f"{self.base_url}{path}"

		try:
			response = self.session.request(method, url, headers=headers, **kwargs)
		except requests.RequestException as e:
			current_app.logger.error(f"{method} {url} failed: {e}")
			raise CustomError("Service unavailable", 503, None)

		if response.status_code in expected:
			return response

		current_app.logger.error(f"{method} {url} -> {response.status_code}: {response.text}")
		raise CustomError(error_message, response.status_code, None)

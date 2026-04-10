import pytest
from app import create_app, log_error, ap
from db.base import db as _db
from marshmallow import ValidationError

focus = pytest.mark.focus

@pytest.fixture(scope='function')
def app():
	app = create_app("testing")

	with app.app_context():
		_db.create_all()
		yield app
		_db.session.remove()
		_db.drop_all()

@pytest.fixture(scope='function')
def client(app):
	return app.test_client()

@pytest.fixture(scope='function')
def db(app):
	with app.app_context():
		yield _db
		_db.session.rollback()  # Clean up after each test

@pytest.fixture(scope='function')
def session(db):
	return db.session

@pytest.fixture
def assert_valid_schema():
	"""Fixture that validates response against a schema"""
	def _assert_valid(response_data, schema_class, many=False):
		if not isinstance(response_data, (dict, list)):
			raise TypeError(
				f"Expected dict or list, got {type(response_data)}. "
				f"Did you pass SQLAlchemy objects instead of response.json?"
			)
		schema = schema_class(many=many)
		try:
			schema.load(response_data)
		except ValidationError as e:
			log_error(e)
			import json
			errors = json.dumps(e.messages, indent=2)
			pytest.fail(f"Schema validation failed:\n{errors}")
		return True
	return _assert_valid

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

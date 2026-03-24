import pytest
from app import create_app
from db.base import db as _db

@pytest.fixture(scope='function')
def app():
	app = create_app("testing")

	with app.app_context():
		_db.create_all()
		yield app
		_db.session.remove()
		_db.drop_all()

@pytest.fixture(scope='function') #TODO check usefulness of this step
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

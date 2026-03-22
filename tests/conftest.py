import pytest
from app import create_app
from db.base import db as _db

@pytest.fixture(scope='session')
def app():
	app = create_app()
	app.config['TESTING'] = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	with app.app_context():
		_db.create_all()
		yield app
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

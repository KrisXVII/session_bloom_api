import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	"""Base configuration"""
	# SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	KRATOS_ADMIN_URL = os.environ['KRATOS_ADMIN_URL']
	KRATOS_PUBLIC_URL = os.environ['KRATOS_PUBLIC_URL']
	POSTHOG_ENDPOINT = os.environ['POSTHOG_ENDPOINT']
	POSTHOG_API_KEY = os.environ['POSTHOG_API_KEY']

class DevelopmentConfig(Config):
	"""Development configuration"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	FLASK_ENV = 'development'
	POSTHOG_ENABLED = True

class TestingConfig(Config):
	"""Testing configuration - uses in-memory SQLite"""
	TESTING = True
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	FLASK_ENV = 'test'
	POSTHOG_ENABLED = False

class ProductionConfig(Config):
	"""Production configuration"""
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
	FLASK_ENV = 'production'
	POSTHOG_ENABLED = True

# Config mapping
config = {
	'development': DevelopmentConfig,
	'test': TestingConfig,
	'testing': TestingConfig,  # alias
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
import os
from flask import Flask
from db.base import db

def create_app(config_name=None):
	app = Flask(__name__)

	if config_name is None:
		config_name = os.getenv("FLASK_ENV", "development")

	from config.config_env import config
	app.config.from_object(config.get(config_name, config['default']))

	db.init_app(app)

	# Register blueprints
	from app.controllers.user_controller import user_bp
	# from app.routes.session_routes import session_bp

	app.register_blueprint(user_bp, url_prefix='/users')
	# app.register_blueprint(session_bp, url_prefix='/sessions')

	@app.route('/')
	def hello_world():
		return 'Hello World!'

	@app.route('/test')
	def test_pipeline():
		return 'Tested!'

	return app

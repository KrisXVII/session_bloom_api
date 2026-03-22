import os
from flask import Flask
from db.base import db
from dotenv import load_dotenv

def create_app():
	app = Flask(__name__)
	load_dotenv()
	env = os.getenv("FLASK_ENV")

	if env == "test":
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
	else:
		app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)

	# Register blueprints
	from app.controllers.user_controller import user_bp
	# from app.routes.session_routes import session_bp

	app.register_blueprint(user_bp, url_prefix='/users')
	# app.register_blueprint(session_bp, url_prefix='/sessions')

	@app.route('/')
	def hello_world():
		return 'Hello World!'

	return app

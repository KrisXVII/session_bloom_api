import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
	app = Flask(__name__)

	env = os.getenv("FLASK_ENV")

	# Register blueprints (like Rails routes.rb)
	# from app.routes.user_routes import user_bp
	# from app.routes.session_routes import session_bp

	# app.register_blueprint(user_bp, url_prefix='/users')
	# app.register_blueprint(session_bp, url_prefix='/sessions')
	# ci comment for test

	@app.route('/')
	def hello_world():
		return 'Hello World!'

	return app

import os, yaml
from flask import Flask
from db.base import db
from rich.console import Console
from rich.pretty import Pretty
from app.utils.custom_error import CustomError
from flasgger import Swagger
from lib.interfaces.posthog_interface import posthog

console = Console()

def ap(obj):
	console.print("\n")
	console.print(Pretty(obj, expand_all=True))

def log_error(obj, style="red"):
	console.print("\n")
	if style and isinstance(obj, str):
		console.print(f"[{style}]{obj}[/{style}]")

def create_app(config_name=None):
	app = Flask(__name__)

	if config_name is None:
		config_name = os.getenv("FLASK_ENV", "development")

	from config.config_env import config
	app.config.from_object(config.get(config_name, config['default']))

	db.init_app(app)

	with open('swagger.yaml', 'r') as f:
		swagger_template = yaml.safe_load(f)

	swagger = Swagger(app, template=swagger_template)

	# Register blueprints
	from app.controllers.user_controller import user_bp
	from app.controllers.session_controller import session_bp
	from app.controllers.auth.registration_controller import registration_bp

	app.register_blueprint(user_bp, url_prefix='/users')
	app.register_blueprint(session_bp, url_prefix='/sessions')
	app.register_blueprint(registration_bp, url_prefix='/auth')

	@app.errorhandler(CustomError)
	def handle_custom_error(e):
		return e.to_dict(), e.code

	@app.errorhandler(Exception)
	def error_to_posthog(e):
		app.logger.exception(e)

		if app.config["POSTHOG_ENABLED"]:
			try:
				posthog.capture_exception(e)
			except Exception:
				app.logger.exception("Failed to forward exception to PostHog")

		return CustomError("Internal server error", 500, None).to_dict(), 500

	@app.route('/')
	def hello_world():
		return 'Hello World!'

	@app.route('/test')
	def test_pipeline():
		test = "testttttt"
		return 'Tested API pipeline aaaaa!'

	return app

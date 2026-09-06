import os, yaml, traceback
from flask import Flask, request
from db.base import db
from rich.console import Console
from rich.pretty import Pretty
from app.utils.custom_error import CustomError
from flasgger import Swagger
from lib.interfaces.posthog_interface import posthog
from lib.interfaces.beacon_api import BeaconApi

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
			try:
				import traceback

				app.logger.info("type      %s", type(e).__name__)
				app.logger.info("str       %r", str(e))
				app.logger.info("repr      %r", repr(e))
				app.logger.info("args      %r", e.args)
				app.logger.info("attrs     %r", [a for a in dir(e) if not a.startswith("_")])
				app.logger.info("dict      %r", getattr(e, "__dict__", None))
				app.logger.info("cause     %r", e.__cause__)
				app.logger.info("context   %r", e.__context__)
				app.logger.info("frames    %r", traceback.extract_tb(e.__traceback__))
				app.logger.info("request   %r", {
					"path": request.path,
					"method": request.method,
					"endpoint": request.endpoint,
					"url": request.url,
					"remote_addr": request.remote_addr,
					"args": dict(request.args),
				})
				BeaconApi.send_event(e)
			except Exception:
				app.logger.exception("Failed to forward exception to Beacon")

		return CustomError("Internal server error", 500, None).to_dict(), 500

	@app.route('/')
	def hello_world():
		div = 1/0
		return 'Hello World!'

	@app.route('/test')
	def test_pipeline():
		test = "testttttt"
		return 'Tested API pipeline aaaaa!'

	return app

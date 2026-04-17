import os, yaml
from flask import Flask
from db.base import db
from rich.console import Console
from rich.pretty import Pretty
from app.utils.custom_error import CustomError
from flasgger import Swagger

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

	app.register_blueprint(user_bp, url_prefix='/users')
	app.register_blueprint(session_bp, url_prefix='/sessions')

	@app.errorhandler(CustomError)
	def handle_custom_error(e):
		return e.to_dict(), e.code

	@app.route('/')
	def hello_world():
		return 'Hello World!'

	@app.route('/test')
	def test_pipeline():
		test = "testttttt"
		return 'Tested API pipeline aaaaa!'

	return app

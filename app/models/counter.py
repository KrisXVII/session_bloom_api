from db.base import db
from app.models.base_model import BaseModel
from app import ap

class Counter(BaseModel):
	__tablename__ = "counters"

	name = db.Column(db.String(50), primary_key=True)
	value = db.Column(db.Integer, default=0, nullable=False)
	description = db.Column(db.String(255))

	@classmethod
	def get_or_create(cls, name, default_value=1, description=None):
		counter = cls.query.filter_by(name=name).first()
		if not counter:
			counter = cls(
				name=name,
				value=default_value,
				description=description or f"Counter for {name}"
			)
			db.session.add(counter)
		return counter

	def next(self):
		self.value += 1
		return self.value

COUNTER_CONFIG = {
	'user': {
		'default': 1068441172,
	},
	'session': {
		'default': 1000000000,
	},
	'subsession': {
		'default': 2000000000,
	}
}

def _create_counter_method(name, config):
	"""Creates a method like user_code, session_code, etc."""
	def method(cls):
		return cls.get_or_create(name, config['default'])
	return classmethod(method)

# Dynamically add methods to Counter class
for name, config in COUNTER_CONFIG.items():
	method_name = f"generate_{name}_code"
	setattr(Counter, method_name, _create_counter_method(name, config))

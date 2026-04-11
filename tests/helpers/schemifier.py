from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

ma = Marshmallow()

class AutoSchemaWithCustom(SQLAlchemyAutoSchema):
	"""Base schema class that supports custom field additions"""

	class Meta:
		include_fk = True
		load_instance = False

	@classmethod
	def schemify(cls, model, **kwargs):
		"""
		Rails-like schemify function that creates a schema from a model
		with optional custom fields.
		"""
		custom_fields = kwargs.get('custom_fields', {})
		exclude_fields = kwargs.get('exclude', [])

		# Create a dynamic schema class
		schema_attrs = {
			'Meta': type('Meta', (), {
				'model': model,
				'exclude': exclude_fields,
				'include_fk': True,
				'load_instance': False
			})
		}

		# Add custom fields to the schema
		schema_attrs.update(custom_fields)

		# Create and return the schema class
		schema_class = type(
			f"{model.__name__}Schema",
			(cls,),
			schema_attrs
		)

		return schema_class

# Initialize params_schemas with your models
def schemify(model, **kwargs):
	return AutoSchemaWithCustom.schemify(model, **kwargs)
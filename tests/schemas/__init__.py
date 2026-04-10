from .session_schema import SessionSchema
from .user_schema import UserSchema

SCHEMAS = {
	'user': UserSchema,
	# 'user_list': UserListSchema,
	'session': SessionSchema,
}

def get_schema(name):
	return SCHEMAS[name]

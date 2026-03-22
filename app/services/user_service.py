from db.base import db
from app.models.user import User

class UserService:

	@staticmethod
	def create_user(data):
		"""Create a new user with business logic"""
		# Check if email exists
		existing = User.query.filter_by(email=data.get('email')).first()
		if existing:
			raise ValueError('Email already exists')

		user = User(
			email=data.get('email'),
			first_name=data.get('first_name'),
			last_name=data.get('last_name')
		)

		user.save()
		return user

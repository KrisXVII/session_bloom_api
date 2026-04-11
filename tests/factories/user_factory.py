import uuid
import factory
from faker import Faker
from app.models.user import User, UserStatus
from datetime import datetime, timezone
from db.base import db
import random

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = User
		sqlalchemy_session = db.session
		sqlalchemy_session_persistence = "commit"

	id = factory.LazyAttribute(lambda _: uuid.uuid4())
	# code = factory.LazyAttribute(lambda _: IDGenerator.generate_user_code()) # model in init handles this
	first_name = factory.LazyAttribute(lambda _: fake.first_name())
	last_name = factory.LazyAttribute(lambda _: fake.last_name())
	email = factory.LazyAttribute(lambda _: fake.email())
	status = factory.LazyAttribute(lambda _: random.choice(list(UserStatus)))
	created_at = factory.LazyAttribute(lambda _: datetime.now(timezone.utc))
	updated_at = factory.LazyAttribute(lambda _: datetime.now(timezone.utc))

	@classmethod
	def create_batch(cls, size, **kwargs):
		return [cls.create(**kwargs) for _ in range(size)]

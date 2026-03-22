import factory
from faker import Faker
from app.models.user import User
from datetime import datetime
import uuid

fake = Faker()

class UserFactory(factory.Factory):
	class Meta:
		model = User

	id = factory.LazyAttribute(lambda _: str(uuid.uuid4()))
	first_name = factory.LazyAttribute(lambda _: fake.first_name())
	last_name = factory.LazyAttribute(lambda _: fake.last_name())
	email = factory.LazyAttribute(lambda _: fake.email())
	created_at = factory.LazyAttribute(lambda _: datetime.utcnow())
	updated_at = factory.LazyAttribute(lambda _: datetime.utcnow())

	@classmethod
	def create_batch(cls, size, **kwargs):
		return [cls.create(**kwargs) for _ in range(size)]

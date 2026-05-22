from app.models.user import User
from app.models.counter import Counter
from tests.factories.user_factory import UserFactory
from tests.conftest import focus
from app import ap
from app.models.user import UserStatus

class TestUserModel:

	def test_create_user(self, db):

		user = UserFactory.create()

		assert user.id is not None
		assert user.email is not None
		assert len(Counter.all()) is not 0

	def test_create_user_with_existing_counter(self, db):

		counter = Counter.create(
			name="user",
			value=1068441172,
			description=f"Counter for user"
		)

		user = UserFactory.create()

		assert user.id is not None
		assert user.email is not None
		assert len(Counter.all()) is not 0
		assert counter.value == 1068441173

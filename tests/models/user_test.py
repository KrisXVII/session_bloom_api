from app.models.user import User
from app.models.counter import Counter
from tests.conftest import focus
from app import ap
from app.models.user import UserStatus

class TestUserModel:

	def test_create_user(self, db):

		user = User.create(
			email="test@example.com",
			first_name="John",
			last_name="Doe",
			status=UserStatus.ACTIVE
		)

		assert user.id is not None
		assert user.email == "test@example.com"
		assert len(Counter.all()) is not 0

	def test_create_user_with_existing_counter(self, db):

		counter = Counter.create(
			name="user",
			value=1068441172,
			description=f"Counter for user"
		)

		user = User.create(
			email="test@example.com",
			first_name="John",
			last_name="Doe",
			status=UserStatus.ACTIVE
		)

		assert user.id is not None
		assert user.email == "test@example.com"
		assert len(Counter.all()) is not 0
		assert counter.value == 1068441173

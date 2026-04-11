from db.utils.id_generator import IDGenerator
from tests.conftest import focus
from app.models.counter import Counter
from app import ap

class TestIDGenerator:

	def test_simple_generation(self, session):
		user_id = IDGenerator.generate_user_code()
		assert user_id.startswith('USR_')

	class TestGetOrCreate:

		def test_creates_new_counter(self, session):
			"""Test that get_or_create creates a new counter when it doesn't exist"""
			counter = Counter.get_or_create('test_counter', 1000, 'Test description')

			assert counter is not None
			assert counter.name == 'test_counter'
			assert counter.value == 1000
			assert counter.description == 'Test description'

		def test_returns_existing_counter(self, session):
			"""Test that get_or_create returns existing counter without recreating"""
			counter1 = Counter.get_or_create('test_counter2', 1000)

			counter2 = Counter.get_or_create('test_counter2', 9999)
			assert counter1.name == counter2.name
			assert counter2.value == 1000
			assert counter1 is counter2

	class TestNext:

		def test_next_increments_value(self, session):
			"""Test that next() increments the counter value"""
			counter = Counter.get_or_create('increment_test', 100)
			assert counter.value == 100

			next_value = counter.next()
			assert next_value == 101
			assert counter.value == 101

			counter.next()
			assert counter.value == 102

	class TestDynamicMethods:

		def test_method_generation(self, session):
			"""Test that dynamic methods like generate_user_code exist"""
			assert hasattr(Counter, 'generate_user_code')
			assert hasattr(Counter, 'generate_session_code')
			assert hasattr(Counter, 'generate_subsession_code')
			assert callable(Counter.generate_user_code)

		def test_return_counter(self, session):
			"""Test that dynamic methods return a Counter instance"""
			counter = Counter.generate_user_code()
			assert isinstance(counter, Counter)
			assert counter.name == 'user'
			assert counter.value == 1068441172

	def test_persistence_across_sessions(self, session, db):
		"""Test that counter values persist in database"""
		# First call
		counter1 = Counter.generate_user_code()
		counter1.next()

		# Clear session to simulate new request
		db.session.expunge_all()

		# Retrieve counter again
		counter2 = Counter.generate_user_code()
		assert counter2.value == 1068441173  # Should have persisted

	def test_counter_with_custom_default(self, session):
		counter = Counter.get_or_create('custom_counter', 999999)
		assert counter.value == 999999

		counter.next()
		assert counter.value == 1000000

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Profile, Match, Base  # Import your SQLAlchemy models

#TO RUN USE: python3 -m unittest db_test.py

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        # Close the session and remove engine
        self.session.close()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_user_profile_relationship(self):
        # Create a user
        user = User(username='test_user', email='test@example.com', password='password')
        self.session.add(user)
        self.session.commit()

        # Create a profile for the user
        profile = Profile(user_id=user.id, firstName='John', lastName='Doe', age=30, gender='Male')
        self.session.add(profile)
        self.session.commit()

        # Retrieve user and check if profile is accessible
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        self.assertIsNotNone(retrieved_user.profile)
        self.assertEqual(retrieved_user.profile.firstName, 'John')
        self.assertEqual(retrieved_user.profile.age, 30)

        # Retrieve profile and check if user is accessible
        retrieved_profile = self.session.query(Profile).filter_by(id=profile.id).first()
        self.assertIsNotNone(retrieved_profile.user)
        self.assertEqual(retrieved_profile.user.username, 'test_user')
    def test_user_matches_relationship(self):
        # Create two users
        user1 = User(username='user1', email='user1@example.com', password='password1')
        user2 = User(username='user2', email='user2@example.com', password='password2')
        self.session.add_all([user1, user2])
        self.session.commit()

        # Match the users together
        match1 = Match(user_id=user1.id, matched_user_id=user2.id, compatibility_score=0.8)
        match2 = Match(user_id=user2.id, matched_user_id=user1.id, compatibility_score=0.8)
        self.session.add_all([match1, match2])
        self.session.commit()

        # Retrieve user1 and check if user2 is in matches
        retrieved_user1 = self.session.query(User).filter_by(id=user1.id).first()
        self.assertEqual(len(retrieved_user1.matches), 1)
        self.assertEqual(retrieved_user1.matches[0].matched_user_id, user2.id)

        # Retrieve user2 and check if user1 is in matches
        retrieved_user2 = self.session.query(User).filter_by(id=user2.id).first()
        self.assertEqual(len(retrieved_user2.matches), 1)
        self.assertEqual(retrieved_user2.matches[0].matched_user_id, user1.id)

if __name__ == '__main__':
    unittest.main()

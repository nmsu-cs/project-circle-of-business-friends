import random
from faker import Faker
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from database import User, Profile, engine
from profile_logic import INTERESTS_LIST
from matching import calc_magnitude, update_matches

fake = Faker()

# Create a session
Session = sessionmaker(bind=engine)
sqlsession = Session()

# Function to generate random interests
def generate_interests():
    num_interests = random.randint(1, len(INTERESTS_LIST))
    rand_interests = random.sample(INTERESTS_LIST, num_interests)
    
    i_dict = defaultdict(int)
    for i in rand_interests:
        i_dict[i] = 1
    return i_dict

# Create 10 users
for _ in range(10):
    username = fake.user_name()
    email = fake.email()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    interests = generate_interests()

    # Create a user
    user = User(username=username, email=email, password=password)

    # Create a profile
    profile = Profile(
        firstName=fake.first_name(),
        lastName=fake.last_name(),
        age=random.randint(18, 65),
        gender=random.choice(['Male', 'Female', 'Other']),
        interests=interests,
        occupation=fake.job(),
        education_level=random.choice(['High School', 'College', 'Graduate School']),
        major=fake.random_element(elements=['Computer Science', 'Engineering', 'Art', 'Music']),
        vmagnitude=calc_magnitude(interests)
    )

    # Add the profile to the user
    user.profile = profile

    # Add the user to the session
    sqlsession.add(user)

# Commit the changes
sqlsession.commit()

users = sqlsession.query(User).all()

for user in users:
    update_matches(sqlsession, user.profile)

# Close the session
sqlsession.close()

print("Users created successfully!")

import random
from faker import Faker
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from database import User, Profile, engine
from profile_logic import INTERESTS_LIST, OCC_LIST,ED_LIST, MAJOR_LIST
from matching import update_matches
from datetime import date

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

    # Create a user
    user = User(username=username, email=email, password=password)
    print(username, email, password)

    interests = generate_interests()
    firstName=fake.first_name()
    lastName=fake.last_name()
    day=random.randint(1, 30)
    month=random.randint(1, 12)
    year=random.randint(1990, 2007)
    gender=random.choice(['Male', 'Female', 'Other'])
    interests=interests
    career_interest=random.choice(OCC_LIST)
    education_level=random.choice(ED_LIST)
    major=random.choice(MAJOR_LIST)

    # Create a profile
    profile = Profile(firstName=firstName, lastName=lastName, dob=date(year, month, day), gender=gender, interests=interests, career_interest=career_interest, education_level=education_level, major=major)
    print(firstName, lastName, (month, day, year), gender, career_interest, education_level, major)
    print("\n")

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

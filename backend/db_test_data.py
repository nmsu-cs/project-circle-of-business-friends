import random
from faker import Faker
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from database import User, Profile, engine
from profile_logic import INTERESTS_LIST, OCC_LIST,ED_LIST, MAJOR_LIST
from matching import update_matches

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
for _ in range(5):
    username = fake.user_name()
    email = fake.email()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    # Create a user
    user = User(username=username, email=email, password=password)
    print(username, email, password)

    interests = generate_interests()
    firstName=fake.first_name(),
    lastName=fake.last_name(),
    age=random.randint(17, 22),
    gender=random.choice(['Male', 'Female', 'Other']),
    interests=interests,
    occupation=random.choice(OCC_LIST),
    education_level=random.choice(ED_LIST),
    major=random.choice(MAJOR_LIST)

    # Create a profile
    profile = Profile(firstName=firstName[0], lastName=lastName[0], age=age[0], gender=gender[0], interests=interests[0], occupation=occupation[0], education_level=education_level[0], major=major)
    print(firstName[0], lastName[0], age[0], gender[0], occupation[0], education_level[0], major)
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

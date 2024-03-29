from flask import Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from database import engine, Profile

profilearray_bp = Blueprint('profilearray_bp', __name__)

# TODO: create way to load actual userids from "Profile" database into user_ids

# placeholder for logic to get userids from "Profile" database
# for now, update user_ids to match what you have in your copy of the database
# (everyone should have userid 1, that's bob)
user_ids = [1]
current_user_ids_index = -1 # first increment sets to 0

def prof_create(userid):
    # connect to database via SQLAlchemy
    Session = sessionmaker(bind=engine)
    SQLsession = Session()

    # takes userid and returns associated data in list
    user = SQLsession.query(Profile).filter_by(user_id = userid).first()
    profiledata = [user.firstName, user.lastName, user.age, user.gender,
                   user.interests, user.occupation, user.education_level,
                    user.major]

    SQLsession.close()
    return profiledata

def get_next_user_id():
    # returns and increments current_user_ids_index each time next_prof() is called
    global current_user_ids_index
    current_user_ids_index = (current_user_ids_index + 1) % len(user_ids)
    return user_ids[current_user_ids_index]

# will call this from home.html
@profilearray_bp.route('/next_profile')
# returns list of prof data in json
def next_prof():
    user_id = get_next_user_id()
    profile_data = prof_create(user_id)
    return jsonify(profile_data)
from sqlalchemy.orm import sessionmaker
from database import engine, Profile

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)
SQLsession = Session()

def prof_create(userid):
    user = SQLsession.query(Profile).filter_by(user_id = userid).first()
    profiledata = [user.firstName, user.lastName, user.age, user.gender,
                   user.interests, user.occupation, user.education_level,
                    user.major]

    SQLsession.close()
    return profiledata
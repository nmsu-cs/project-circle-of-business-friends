from flask import request, session, Blueprint, jsonify
from sqlalchemy.orm import sessionmaker
from database import engine, User, Profile
from datetime import date
import json

signup_bp = Blueprint('signup', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
   
    sqlsession = Session()
    response_object = {'status':'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        print(json.dumps(post_data, indent=2))

        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        firstName = post_data.get('firstName')
        lastName = post_data.get('lastName')
        dob = post_data.get('dob')

        #generate token
        #store in user.vtoken
        #

        try:
            # Check if username already exists
            existing_user = sqlsession.query(User).filter_by(username=username).first()
            if existing_user:
                response_object['status'] = 'error'
                response_object['msg'] = 'Username already in use'
                print(json.dumps(response_object, indent=2))
                return jsonify(response_object)

            # Check if email already exists
            existing_email = sqlsession.query(User).filter_by(email=email).first()
            if existing_email:
                response_object['status'] = 'error'
                response_object['msg'] = 'Email already in use'
                print(json.dumps(response_object, indent=2))
                return jsonify(response_object)

            # Add new user to the database
            new_user = User(username=username, password=password, email=email)
            sqlsession.add(new_user)
            sqlsession.commit()

            user_id = new_user.id

            #Process data for adding
            year, month, day = dob.split('-')
            dob = date(int(year), int(month), int(day))

            new_profile = Profile(user_id=user_id, firstName=firstName, lastName=lastName, dob=dob)
            sqlsession.add(new_profile)
            sqlsession.commit()

            response_object['msg'] = 'User added!'
            response_object['user_id'] = user_id
            return jsonify(response_object)
        except Exception as e:
            sqlsession.rollback()
            response_object['status'] = 'error'
            response_object['msg'] = str(e)
            return jsonify(response_object)
        finally:
            sqlsession.close()

    sqlsession.close()
    return jsonify(response_object)
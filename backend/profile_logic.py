from flask import jsonify, render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, Profile
from collections import defaultdict
from matching import update_matches
import json
from datetime import date

profile_bp = Blueprint('profile', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

#Interest definitions
INTERESTS_LIST = [
    'football',
    'basketball',
    'soccer',
    'art',
    'music',
    'food',
    'bar-hopping',
    'partying',
    'dinner-ing?'
]

MAJOR_LIST = [
    'majorA',
    'majorB',
    'majorC',
    'majorD',
    'majorE',
    'majorF'
]

OCC_LIST = [
    'occA',
    'occB',
    'occC',
    'occD',
    'occE',
    'occF'
]

ED_LIST = [
    'Freshman',
    'Sophomore',
    'Junior',
    'Senior'
]

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():

    sqlsession = Session()
    response_object = {'status':'success'}

    if request.method == "GET":
            user_id = request.args.get('user_id')

            
            if not user_id:
                response_object['status'] = 'error'
                response_object['msg'] = 'user_id param is missing'
                return jsonify(response_object)
            
            try:
                user_id = int(user_id)
                user_profile = sqlsession.query(Profile).filter_by(user_id=user_id).first()

                if user_profile:
                    interests = []
                    age = calculate_age(user_profile.dob)
                    if user_profile.interests:
                        dict = user_profile.interests
                        interests = list(dict.keys())
                    
                    response_object['data'] = {
                        'age': age,
                        'gender': user_profile.gender,
                        'major': user_profile.major,
                        'education_level': user_profile.education_level,
                        'career_interest': user_profile.career_interest,
                        'interests': interests,
                    }
                    return jsonify(response_object)
                
                else:
                    response_object['status'] = 'error'
                    response_object['msg'] = 'Profile not found'
                    return jsonify(response_object)
            
            except ValueError:
                response_object['status'] = 'error'
                response_object['msg'] = 'Invalid user_id'
                return jsonify(response_object)
            
    elif request.method == 'POST':
        post_data = request.get_json()
        
        try:
            user_id = post_data.get('user_id')
            print(json.dumps(post_data, indent=2))

            user_profile = sqlsession.query(Profile).filter_by(user_id=user_id).first()

            gender = post_data.get('gender')
            major = post_data.get('major')
            education_level = post_data.get('education_level')
            career_interest = post_data.get('career_interest')
            interests = post_data.get('interests')

            i_dict = defaultdict(int)
            for i in interests:
                i_dict[i] = 1

            user_profile.gender = gender
            user_profile.interests = i_dict
            user_profile.career_interest = career_interest
            user_profile.education_level = education_level
            user_profile.major = major

            sqlsession.commit()

            res = update_matches(sqlsession, user_profile)
            print(res)

            response_object['status']='success'
            response_object['msg']= 'Profile and matches updated successfully'
            return jsonify(response_object)
        except Exception as e:
            sqlsession.rollback()
            response_object['status'] = 'error'
            response_object['msg'] = str(e)
            return jsonify(response_object)
        finally:
            sqlsession.close()
    
    sqlsession.close()
    response_object['status'] = 'error'
    response_object['msg'] = 'Invalid request method'
    return jsonify(response_object)

def calculate_age(dob):
    today = date.today()
    
    age = today.year - dob.year
    
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    
    return age
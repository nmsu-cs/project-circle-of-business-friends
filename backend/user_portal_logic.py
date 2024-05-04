from flask import jsonify, Blueprint, request
from sqlalchemy.orm import sessionmaker
from database import engine, Profile, User
from matching import get_matches
import json
from collections import defaultdict

user_portal_bp = Blueprint('user_portal', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@user_portal_bp.route('/user_portal')
def user_portal():
    sqlsession = Session()
    response_object = {'status':'success'}

    if request.method == "GET":
            user_id = request.args.get('user_id')

            if not user_id:
                response_object['status'] = 'error'
                response_object['msg'] = 'user_id param is missing'
                return jsonify(response_object)
            
            try:
                user_profile = sqlsession.query(Profile).filter_by(user_id=user_id).first()
                user = sqlsession.query(User).filter_by(id=user_id).first()

                dict = user_profile.interests
                keys = list(dict.keys())

                response_object['data']={
                     "username":user.username,
                     "firstName":user_profile.firstName,
                     "lastName":user_profile.lastName,
                     "major":user_profile.major,
                     "ed_level":user_profile.education_level,
                     "career_interest":user_profile.career_interest,
                     "interests":keys
                }

                return jsonify(response_object)
            
            except ValueError:
                response_object['status'] = 'error'
                response_object['msg'] = 'Invalid user_id'
                return jsonify(response_object)

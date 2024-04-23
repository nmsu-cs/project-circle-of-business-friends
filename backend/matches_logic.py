from flask import jsonify, Blueprint, request
from sqlalchemy.orm import sessionmaker
from database import engine, Profile, User
from matching import get_matches
import json
from collections import defaultdict

matches_bp = Blueprint('matches', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@matches_bp.route('/matches')
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
                top_matches = get_matches(sqlsession, user_id, 5)
                matches, ids = profile_convert(top_matches)
                response_object['matches']=matches

                return jsonify(response_object)
            
            except ValueError:
                response_object['status'] = 'error'
                response_object['msg'] = 'Invalid user_id'
                return jsonify(response_object)
    
def profile_convert(matches):
    ret = defaultdict(list)
    ids = []
    for match, profile in matches:
        ret[match.match_id]=[
            profile.firstName,
            profile.lastName,
            match.compatibility_score
        ]
        ids.append(match.match_id)
    return ret, ids

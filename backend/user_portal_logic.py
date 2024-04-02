from flask import render_template, redirect, url_for, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, Profile, User
from matching import get_matches
import json
from collections import defaultdict

user_portal_bp = Blueprint('user_portal', __name__)

#global variables
CURRENT_INDEX=-1

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@user_portal_bp.route('/user_portal')
def user_portal():
    sqlsession = Session()

    #Check if user is logged in
    if 'user_id' in session:
    
        #Retrieve user
        user_id = session['user_id']
        user_profile = sqlsession.query(Profile).filter_by(user_id=user_id).first()
        user = sqlsession.query(User).filter_by(id=user_id).first()
        username = user.username

        #Retrieve top matches, change last variable to increase display count
        top_matches = get_matches(sqlsession, user_id, 5)

        matches, ids = profile_convert(top_matches)
        matches_json = json.dumps(matches)
        ids_json = json.dumps(ids)
        sqlsession.close()

        return render_template('user_portal.html', user=user_profile, username=username, matches = matches_json, ids=ids_json)
    else:
        return redirect(url_for('login.login'))
    
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

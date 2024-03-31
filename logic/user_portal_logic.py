from flask import render_template, redirect, url_for, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, Profile, User
from matching import get_matches

user_portal_bp = Blueprint('user_portal', __name__)

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

        sqlsession.close()

        return render_template('user_portal.html', user=user_profile, top_matches=top_matches, username=username)
    else:
        return redirect(url_for('login.login'))

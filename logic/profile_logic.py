from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, Profile

profile_bp = Blueprint('profile', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    
    sqlsession = Session()
    user_id = session.get('user_id') 
    messages = []
    
    user = sqlsession.query(Profile).filter_by(user_id=user_id).first()

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        interests = request.form.get('interests')
        occupation = request.form.get('occupation')
        education_level = request.form.get('education_level')
        major = request.form.get('major')

        if user:
            user.age = age
            user.gender = gender
            user.interests = interests
            user.occupation = occupation
            user.education_level = education_level
            user.major = major

            sqlsession.commit()
            flash('Profile updated successfully')
            sqlsession.close()
            return redirect(url_for('user_portal.user_portal'))
        else:
            messages.append('User not found')
    return render_template('profile.html', messages=messages, user=user)

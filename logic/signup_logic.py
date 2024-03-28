from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User, Profile
import re

signup_bp = Blueprint('signup', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    sqlsession = Session()

    # Holds error messages to display
    messages = []

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstName' in request.form and 'lastName' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        # Check if user already exists
        existing_user = sqlsession.query(User).filter_by(email=email).first()

         # Error handling
        if existing_user:
            messages.append('Account already exists')
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            messages.append('Invalid email address')
        if not re.match(r'[A-Za-z0-9]+', username):
            messages.append('Username must only contain characters and numbers')
        if not username or not password or not email or not firstName or not lastName:
            messages.append('Please fill out the form')

        # If there are no errors, proceed with user creation
        if not messages:
            new_user = User(username=username, password=password, email=email)
            sqlsession.add(new_user)
            sqlsession.commit()
            
            user_id = new_user.id
            session['user_id'] = user_id
            
            new_profile = Profile(user_id=user_id, firstName=firstName, lastName = lastName)
            sqlsession.add(new_profile)
            sqlsession.commit()

            flash('Account created successfully! Please complete your profile.')
            return redirect(url_for('profile.profile'))
    sqlsession.close()
    return render_template('signup.html', messages=messages)

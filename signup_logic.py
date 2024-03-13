from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import os
from database import User
import re

# Extract database path
config = configparser.ConfigParser()
config.read('config.ini')

db_path = config['database']['db_path']
db_path = os.path.expandvars(db_path)

app = Flask(__name__)
app.secret_key = '123123'

# Connect to database via SQLAlchemy
engine = create_engine(f'sqlite:///{db_path}', echo=True)
Session = sessionmaker(bind=engine)

# Define sign up route
@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
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
            new_user = User(username=username, password=password, email=email, firstName=firstName, lastName=lastName)
            sqlsession.add(new_user)
            sqlsession.commit()
            
            user_id = new_user.id
            session['user_id'] = user_id
            flash('Account created successfully! Please complete your profile.')
            return redirect(url_for('profile_creation'))
    sqlsession.close()
    return render_template('signup.html', messages=messages)

@app.route('/profile', methods=['GET', 'POST'])
def profile_creation():
    
    sqlsession = Session()
    user_id = session.get('user_id') 
    
    messages = []

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        interests = request.form.get('interests')
        occupation = request.form.get('occupation')
        education_level = request.form.get('education_level')
        major = request.form.get('major')

        user = sqlsession.query(User).filter_by(id=user_id).first()

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
            return redirect(url_for('user_portal'))
        else:
            messages.append('User not found')
    return render_template('profile.html', messages = messages);

@app.route('/user_portal')
def user_portal():
    return "WELCOME"


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
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

# Connect to database via SQLAlchemy
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)

# Test for ability to manipulate database
users = session.query(User).all()

for user in users:
    print(f"{user.id}, {user.username}, {user.password} {user.email}, {user.firstName}, {user.lastName}")

session.close()

# Define sign up route
@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session = Session()
    # Holds error messages to display
    message = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstName' in request.form and 'lastName' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        # Check if user already exists
        existing_user = session.query(User).filter_by(email=email).first()

        # Error handling
        if existing_user:
            message = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            message = 'Username must only contain characters and numbers'
        elif not username or not password or not email or not firstName or not lastName:
            message = 'Please fill out the form'
        else:
            new_user = User(username=username, password=password, email=email, firstName=firstName, lastName=lastName)

            session.add(new_user)
            session.commit()
            return redirect(url_for('signup_success'))
    elif request.method == 'POST':
        message = 'Please fill out the form'
    session.close()
    return render_template('signup.html', msg=message)

@app.route('/signup/success')
def signup_success():
    return 'Sign up successful'

if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User

login_bp = Blueprint('login', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():

    sqlsession = Session()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Retrieve user from database
        user = sqlsession.query(User).filter_by(username=username).first()
        sqlsession.close()

        if user and user.password == password:
            #Store userID in session
            session['user_id']=user.id
            flash('Login successful!')
            return redirect(url_for('user_portal.user_portal'))
        else:
            flash('Invalid username or password. Please try again.')
    return render_template('login.html')
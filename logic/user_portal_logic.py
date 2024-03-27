from flask import render_template, redirect, url_for, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User

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
        user = sqlsession.query(User).filter_by(id=user_id).first()
        sqlsession.close()

        return render_template('user_portal.html', user=user)
    else:
        return redirect(url_for('login.login'))

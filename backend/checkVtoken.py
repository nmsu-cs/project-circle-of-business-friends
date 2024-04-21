from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, Profile
from collections import defaultdict
from matching import update_matches

verify_bp = Blueprint('verify', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@verify_bp.route('/verify', methods=['GET', 'POST'])
def profile():
    
    sqlsession = Session()
    user_id = session.get('user_id') 
    
    user = sqlsession.query(Profile).filter_by(user_id=user_id).first()



    if request.method == 'POST':
        inputToken = request.form.get('vtoken')

    
        if user:
            if user.vtoken == inputToken:
                user.emailAuth = 1
                sqlsession.commit()
                sqlsession.close()
                return redirect(url_for('verify.verify'))
            else:
                flash('Incorrect Verification Code')


    
            return redirect(url_for('user_portal.user_portal'))
        else:
            flash('User not found')
from flask import jsonify, render_template, request, redirect, url_for, flash, session, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User
from collections import defaultdict
from matching import update_matches

verify_bp = Blueprint('verify', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@verify_bp.route('/verify', methods=['GET', 'POST'])
def profile():
    
    print('Profile route accessed')  # debug print

    sqlsession = Session() 

    if request.method == 'POST':
        inputToken = request.form.get('vtoken')
        user_id = request.form.get('user_id')  # get user id from form data

        user = sqlsession.query(User).filter_by(id=user_id).first()  # 'id' to filter
    
        if user:
            if user.vtoken == inputToken:
                user.verifiedEmail = 1
                sqlsession.commit()
                sqlsession.close()
                return jsonify({'status': 'success', 'message': 'Email verified successfully'})
            else:
                sqlsession.close()
                return jsonify({'status': 'error', 'message': 'Incorrect verification code'}), 400
        else:
            sqlsession.close()
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    return render_template('verify.html')

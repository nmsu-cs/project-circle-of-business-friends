from flask import jsonify, request, Blueprint
from sqlalchemy.orm import sessionmaker
from database import engine, User

login_bp = Blueprint('login', __name__)

# Connect to database via SQLAlchemy
Session = sessionmaker(bind=engine)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():

    sqlsession = Session()
    response_object = {'status':'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        try:
            username = post_data.get('username')
            password = post_data.get('password')

            # Retrieve user from database
            user = sqlsession.query(User).filter_by(username=username).first()

            if user and user.password == password:
                response_object['msg'] = 'User found'
                response_object['user_id'] = user.id
                return jsonify(response_object)
            else:
                response_object['status']='error'
                response_object['msg'] = 'Invalid username or password'
                return jsonify(response_object)

        except Exception as e:
            response_object['status'] = 'error'
            response_object['msg'] = 'An error occurred while processing your request'
            return jsonify(response_object)

        finally:
            sqlsession.close()
    sqlsession.close()
    response_object['status'] = 'error'
    response_object['msg'] = 'Invalid request method'
    return jsonify(response_object)
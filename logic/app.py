from flask import Flask
from signup_logic import signup_bp
from login_logic import login_bp
from profile_logic import profile_bp
from user_portal_logic import user_portal_bp
from index_logic import index_bp

app = Flask(__name__, template_folder='../templates')
app.secret_key = '123123'
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(user_portal_bp)
app.register_blueprint(index_bp)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
from flask_cors import CORS

from signup_logic import signup_bp
from login_logic import login_bp
from profile_logic import profile_bp
from user_portal_logic import user_portal_bp
from index_logic import index_bp
from profilearray import profilearray_bp
from logout_logic import logout_bp

app = Flask(__name__, template_folder='../templates', static_folder="../static")
CORS(app, resources={r'/*':{'origins':'*'}})

app.secret_key = '123123'
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(user_portal_bp)
app.register_blueprint(index_bp)
app.register_blueprint(profilearray_bp)
app.register_blueprint(logout_bp)

@app.route("/login")
def login():
    title = "Login"
    return render_template("login.html", title=title)

@app.route("/signup")
def signup():
    title = "Sign Up"
    return render_template("signup.html", title=title)

@app.route("/landing_page")
def landing_page():
    title = "Welcome"
    return render_template("landing_page.html", title=title)

@app.route("/home")
def home():
    title = "Home"
    return render_template("home.html", title=title)





if __name__ == '__main__':
    app.run(debug=False)

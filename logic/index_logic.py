from flask import render_template, Blueprint

index_bp = Blueprint("index", __name__)

@index_bp.route('/')
def landing_page():
    return render_template('landing_page.html')
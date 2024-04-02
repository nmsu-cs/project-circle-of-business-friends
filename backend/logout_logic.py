from flask import redirect, url_for, session, Blueprint, flash

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['POST'])
def logout():
    
    # Clear the session data
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))
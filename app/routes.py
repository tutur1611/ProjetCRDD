from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, send_file, request
from flask_login import login_required, logout_user, current_user
from app.static.logique_routes import login, handle_sign_in, handle_update_profile, handle_edit_user, handle_delete_user, handle_reset_password
from reprises_de_dressage import generate_graph
from app.models import User, Reprise

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()  # Appelle la fonction `login` importée depuis `logique_routes.py`

@main.route('/logout')
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('main.login_route'))

@main.route('/signIn', methods=['GET', 'POST'])
def signIn():
    return handle_sign_in()

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if current_user.role.nom != 'Admin':
        flash("Accès refusé : Vous devez être administrateur pour accéder à cette page.", "danger")
        return redirect(url_for('main.home'))

    users = [user.to_dict() for user in User.query.all()]
    return render_template('admin_panel.html', users=users)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/creation_reprise')
def creation_reprise():
    return render_template('creation_reprise.html')

@main.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    return handle_update_profile()

@main.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    return handle_edit_user(user_id)

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return handle_delete_user(user_id)

@main.route('/admin/reset_password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    return handle_reset_password(user_id)

@main.route('/user_reprises')
@login_required
def user_reprises():
    reprises = Reprise.query.filter_by(user_id=current_user.id).all()
    return render_template('user_reprises.html', reprises=reprises)

@main.route('/generate_graph', methods=['POST'])
def generate_graph_route():
    data = request.json
    figures = data.get('figures', [])
    buf = generate_graph(figures)
    return send_file(buf, mimetype='image/png')
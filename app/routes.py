from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from app import db, bcrypt
from app.models import User, Role, Login, Reprise, Figure
from flask_login import login_required, login_user, logout_user, current_user
from flask import session
from reprises_de_dressage import generate_graph

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_login = Login.query.filter_by(username=username).first()

        if not user_login:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
            return redirect(url_for('main.login'))

        if not bcrypt.check_password_hash(user_login.password, password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for('main.login'))

        user = User.query.get(user_login.idUser)
        session.permanent = True
        login_user(user)
        flash("Connexion réussie !", "success")
        return redirect(url_for('main.home'))

    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('main.login'))

@main.route('/logout_on_close', methods=['POST'])
def logout_on_close():
    if current_user.is_authenticated:
        logout_user()
    return '', 204

@main.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", "info")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('mail')
        username = request.form.get('username')
        password = request.form.get('motDePasse')
        password_confirmation = request.form.get('motDePasseConfirmation')

        if not username:
            flash("Le champ 'Nom d'utilisateur' est obligatoire.", "danger")
            return redirect(url_for('main.signIn'))

        if password != password_confirmation:
            flash("Les mots de passe sont différents.", "danger")
            return redirect(url_for('main.signIn'))

        existing_user = Login.query.filter_by(username=username).first()
        if existing_user:
            flash("Nom d'utilisateur déjà pris.", "danger")
            return redirect(url_for('main.signIn'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user_role = Role.query.filter_by(nom='User').first()
        if not user_role:
            flash("Le rôle 'User' n'existe pas. Veuillez contacter un administrateur.", "danger")
            return redirect(url_for('main.signIn'))

        new_user = User(nom=nom, prenom=prenom, mail=email, username=username, role_id=user_role.id)
        db.session.add(new_user)
        db.session.commit()

        new_login = Login(idUser=new_user.id, username=username, password=hashed_password)
        db.session.add(new_login)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('main.login'))

    return render_template('signIn.html')

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
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('mail')
    username = request.form.get('username')
    langue = request.form.get('langue')
    theme = request.form.get('theme')
    niveau = request.form.get('niveau')

    # Vérifier si le nom d'utilisateur est déjà pris par un autre utilisateur
    existing_user = User.query.filter(User.username == username, User.id != current_user.id).first()
    if existing_user:
        flash("Nom d'utilisateur déjà pris par un autre utilisateur.", "danger")
        return redirect(url_for('main.profile'))

    # Mettre à jour les informations de l'utilisateur
    current_user.nom = nom
    current_user.prenom = prenom
    current_user.mail = mail
    current_user.username = username
    current_user.langue = langue
    current_user.theme = theme
    current_user.niveau = niveau

    db.session.commit()
    flash("Vos informations ont été mises à jour avec succès.", "success")
    return redirect(url_for('main.profile'))

@main.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.nom = request.form.get('nom')
        user.prenom = request.form.get('prenom')
        user.mail = request.form.get('mail')
        user.username = request.form.get('username')
        user.langue = request.form.get('langue')
        user.theme = request.form.get('theme')
        user.niveau = request.form.get('niveau')
        db.session.commit()
        flash("Les informations de l'utilisateur ont été mises à jour avec succès.", "success")
        return redirect(url_for('main.admin_panel'))
    return render_template('edit_user.html', user=user)

@main.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé avec succès.'}), 200

@main.route('/admin/reset_password/<int:user_id>', methods=['POST'])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    temp_password = "new_password123"
    user_login = Login.query.filter_by(idUser=user.id).first()
    user_login.password = bcrypt.generate_password_hash(temp_password).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'Mot de passe réinitialisé avec succès.'}), 200

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
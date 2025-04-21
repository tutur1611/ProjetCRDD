from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, bcrypt
from app.models import User, Role, Login
from flask_login import login_required, login_user, logout_user, current_user

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
            flash("Nom d'utilisateur ou mot de passe incorre ou mot de passect.", "danger")
            return redirect(url_for('main.login'))

        if not bcrypt.check_password_hash(user_login.password, password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for('main.login'))

        user = User.query.get(user_login.idUser)
        login_user(user)
        flash("Connexion réussie !", "success")
        return redirect(url_for('main.home'))

    return render_template('login.html')

@main.route('/logout')
def logout():
    logout_user()
    flash("Vous avez été déconnecter.", "success")
    return redirect(url_for('main.login'))


@main.route('/signIn', methods=['GET', 'POST'])
def signIn():
    # Vérifier si l'utilisateur est déjà connecté
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", "info")
        return redirect(url_for('main.home'))  # Redirige vers la page d'accueil ou une autre page

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('mail')
        username = request.form.get('username')
        password = request.form.get('motDePasse')
        password_confirmation = request.form.get('motDePasseConfirmation')

        # Vérifier que le champ username n'est pas vide
        if not username:
            flash("Le champ 'Nom d'utilisateur' est obligatoire.", "danger")
            return redirect(url_for('main.signIn'))

        # Vérifier que les mots de passe correspondent
        if password != password_confirmation:
            flash("Les mots de passe sont différents", "danger")
            return redirect(url_for('main.signIn'))
        
        # Vérifier si le nom d'utilisateur existe déjà
        existing_user = Login.query.filter_by(username=username).first()
        if existing_user:
            flash("Nom d'utilisateur déjà pris.", "danger")
            return redirect(url_for('main.signIn'))

        # Hacher le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Récupérer le rôle 'User' par défaut
        user_role = Role.query.filter_by(nom='User').first()
        if not user_role:
            flash("Le rôle 'User' n'existe pas. Veuillez contacter un administrateur.", "danger")
            return redirect(url_for('main.signIn'))

        # Créer un nouvel utilisateur
        new_user = User(nom=nom, prenom=prenom, mail=email, username=username, role_id=user_role.id)
        db.session.add(new_user)
        db.session.commit()

        # Créer un identifiant de connexion
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
    # Vérifier si l'utilisateur connecté est un administrateur
    if current_user.role.nom != 'Admin':
        flash("Accès refusé : Vous devez être administrateur pour accéder à cette page.", "danger")
        return redirect(url_for('main.home'))

    # Récupérer tous les utilisateurs de la base de données et les convertir en dictionnaires
    users = [user.to_dict() for user in User.query.all()]
    return render_template('admin_panel.html', users=users)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
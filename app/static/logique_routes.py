from flask import request, redirect, render_template, url_for, flash, jsonify
from app.models import User, Login, Role
from flask_login import login_user, current_user
from app import db, bcrypt

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_login = Login.query.filter_by(username=username).first()

        if not user_login:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
            return redirect(url_for('main.login_route'))

        if not bcrypt.check_password_hash(user_login.password, password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for('main.login_route'))

        user = User.query.get(user_login.idUser)
        if not user:
            flash("Utilisateur introuvable.", "danger")
            return redirect(url_for('main.login_route'))

        login_user(user)
        flash("Connexion réussie !", "success")
        return redirect(url_for('main.home'))

    return render_template('login.html')

def handle_sign_in():
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

        if not nom or not prenom or not email or not username or not password:
            flash("Tous les champs sont obligatoires.", "danger")
            return redirect(url_for('main.sign_in'))

        if password != password_confirmation:
            flash("Les mots de passe sont différents.", "danger")
            return redirect(url_for('main.sign_in'))

        existing_user = Login.query.filter_by(username=username).first()
        if existing_user:
            flash("Nom d'utilisateur déjà pris.", "danger")
            return redirect(url_for('main.sign_in'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user_role = Role.query.filter_by(nom='User').first()
        if not user_role:
            flash("Le rôle 'User' n'existe pas. Veuillez contacter un administrateur.", "danger")
            return redirect(url_for('main.sign_in'))

        new_user = User(nom=nom, prenom=prenom, mail=email, username=username, role_id=user_role.id)
        db.session.add(new_user)
        db.session.commit()

        new_login = Login(idUser=new_user.id, username=username, password=hashed_password)
        db.session.add(new_login)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('main.login_route'))

    return render_template('signIn.html')

def handle_update_profile():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('mail')
    username = request.form.get('username')
    langue = request.form.get('langue')
    theme = request.form.get('theme')
    niveau = request.form.get('niveau')

    if not nom or not prenom or not mail or not username:
        flash("Tous les champs obligatoires doivent être remplis.", "danger")
        return redirect(url_for('main.profile'))

    existing_user = User.query.filter(User.username == username, User.id != current_user.id).first()
    if existing_user:
        flash("Nom d'utilisateur déjà pris par un autre utilisateur.", "danger")
        return redirect(url_for('main.profile'))

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

def handle_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        mail = request.form.get('mail')
        username = request.form.get('username')
        langue = request.form.get('langue')
        theme = request.form.get('theme')
        niveau = request.form.get('niveau')

        if not nom or not prenom or not mail or not username:
            flash("Tous les champs obligatoires doivent être remplis.", "danger")
            return redirect(url_for('main.edit_user', user_id=user_id))

        existing_user = User.query.filter(User.username == username, User.id != user.id).first()
        if existing_user:
            flash("Nom d'utilisateur déjà pris par un autre utilisateur.", "danger")
            return redirect(url_for('main.edit_user', user_id=user_id))

        user.nom = nom
        user.prenom = prenom
        user.mail = mail
        user.username = username
        user.langue = langue
        user.theme = theme
        user.niveau = niveau

        db.session.commit()
        flash("Les informations de l'utilisateur ont été mises à jour avec succès.", "success")
        return redirect(url_for('main.admin_panel'))

    return render_template('edit_user.html', user=user)

def handle_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for('main.admin_panel'))

def handle_reset_password(user_id):
    user = User.query.get_or_404(user_id)
    temp_password = "new_password123"
    user_login = Login.query.filter_by(idUser=user.id).first()
    user_login.password = bcrypt.generate_password_hash(temp_password).decode('utf-8')
    db.session.commit()
    return jsonify({'message': 'Mot de passe réinitialisé avec succès.'}), 200
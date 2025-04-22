from datetime import datetime
from app import db
from flask_login import UserMixin

# Table des rôles
class Role(db.Model):
    __tablename__ = 'role'  # Définition explicite du nom de la table
    id = db.Column(db.Integer, primary_key=True)  # ID unique pour le rôle
    nom = db.Column(db.String(45), nullable=False, unique=True)  # Nom du rôle (ex: 'Admin', 'User')

    # Relation avec la table User
    users = db.relationship('User', back_populates='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.nom}>'

# Table des utilisateurs
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # ID unique pour l'utilisateur
    nom = db.Column(db.String(45), nullable=False)  # Nom de l'utilisateur
    prenom = db.Column(db.String(45), nullable=False)  # Prénom de l'utilisateur
    mail = db.Column(db.String(100), unique=True, nullable=True)  # Email de l'utilisateur
    username = db.Column(db.String(45), unique=True, nullable=False)  # Nom d'utilisateur
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)  # Clé étrangère vers Role
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)  # Date d'inscription
    derniere_connexion = db.Column(db.DateTime, nullable=True)  # Dernière connexion
    langue = db.Column(db.String(20), default='Français')  # Langue préférée
    theme = db.Column(db.String(10), default='Clair')  # Thème préféré
    nombre_connexions = db.Column(db.Integer, default=0)  # Suivi des connexions
    reprises = db.relationship('Reprise', back_populates='user')  # Relation avec les reprises
    niveau = db.Column(db.String(45), unique=True, nullable=True)  # Niveau de l'utilisateur

    # Relation avec la table Role
    role = db.relationship('Role', back_populates='users', lazy=True)
    login = db.relationship('Login', back_populates='user', uselist=False, lazy=True)
    historique = db.relationship('Historique', back_populates='user', lazy=True)
    notifications = db.relationship('Notification', back_populates='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'mail': self.mail,
            'username': self.username,
            'role': {'id': self.role.id, 'nom': self.role.nom} if self.role else None,
            'date_inscription': self.date_inscription,
            'derniere_connexion': self.derniere_connexion,
            'langue': self.langue,
            'theme': self.theme,
            'niveau': self.niveau
        }

    def __repr__(self):
        return f'<User {self.nom} {self.prenom}>'

# Table des identifiants de connexion (login)
class Login(db.Model):
    __tablename__ = 'login'
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Lien vers la table User
    username = db.Column(db.String(45), unique=True, nullable=False)  # Nom d'utilisateur
    password = db.Column(db.String(255), nullable=False)  # Mot de passe (stocké sous forme de hash)

    # Relation vers l'utilisateur
    user = db.relationship('User', back_populates='login')

    def __repr__(self):
        return f'<Login {self.username}>'

# Table des reprises
class Reprise(db.Model):
    __tablename__ = 'reprise'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)  # Nom de la reprise
    description = db.Column(db.Text, nullable=True)  # Description de la reprise
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Créateur de la reprise
    user = db.relationship('User', back_populates='reprises')
    figures = db.relationship('Figure', back_populates='reprise', cascade="all, delete-orphan")  # Figures associées

# Table des figures
class Figure(db.Model):
    __tablename__ = 'figure'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # Type de figure (ex: Volte, Diagonale)
    lettre_depart = db.Column(db.String(1), nullable=False)  # Lettre de départ
    lettre_arrivee = db.Column(db.String(1), nullable=True)  # Lettre d'arrivée (si applicable)
    reprise_id = db.Column(db.Integer, db.ForeignKey('reprise.id'), nullable=False)
    reprise = db.relationship('Reprise', back_populates='figures')

# Table de l'historique
class Historique(db.Model):
    __tablename__ = 'historique'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  # Description de l'action
    date_action = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='historique')

# Table des notifications
class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)  # Contenu de la notification
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='notifications')

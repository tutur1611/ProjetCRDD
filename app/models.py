from datetime import datetime
from app import db
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = 'role'  
    id = db.Column(db.Integer, primary_key=True)  
    nom = db.Column(db.String(45), nullable=False, unique=True)  

    users = db.relationship('User', back_populates='role', lazy=True)

    def __repr__(self):
        return f'<Role {self.nom}>'

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  
    nom = db.Column(db.String(45), nullable=False)  
    prenom = db.Column(db.String(45), nullable=False)  
    mail = db.Column(db.String(100), unique=True, nullable=True)  
    username = db.Column(db.String(45), unique=True, nullable=False)  
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)  
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime, nullable=True)  
    langue = db.Column(db.String(20), default='Français')  
    theme = db.Column(db.String(10), default='Clair')  
    nombre_connexions = db.Column(db.Integer, default=0)  
    reprises = db.relationship('Reprise', back_populates='user')  
    niveau = db.Column(db.String(45), unique=True, nullable=True)  


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

class Login(db.Model):
    __tablename__ = 'login'
    idUser = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  
    username = db.Column(db.String(45), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False)  

    
    user = db.relationship('User', back_populates='login')

    def __repr__(self):
        return f'<Login {self.username}>'

class Reprise(db.Model):
    __tablename__ = 'reprise'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)  
    description = db.Column(db.Text, nullable=True)  
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    user = db.relationship('User', back_populates='reprises')
    figures = db.relationship('Figure', back_populates='reprise', cascade="all, delete-orphan")  

class Figure(db.Model):
    __tablename__ = 'figure'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  
    lettre_depart = db.Column(db.String(1), nullable=False)  
    lettre_arrivee = db.Column(db.String(1), nullable=True)  
    reprise_id = db.Column(db.Integer, db.ForeignKey('reprise.id'), nullable=False)
    reprise = db.relationship('Reprise', back_populates='figures')

class Historique(db.Model):
    __tablename__ = 'historique'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)  
    date_action = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='historique')

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)  
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='notifications')

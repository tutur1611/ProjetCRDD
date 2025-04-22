from app import create_app, db
from app.models import User, Login, Role
from flask_bcrypt import generate_password_hash

app = create_app()

with app.app_context():
    print("Tables détectées par SQLAlchemy :", db.metadata.tables.keys())
    db.create_all()
    print("📁 Base de données créée avec succès.")

with app.app_context():
    # Création des rôles
    admin_role = Role(nom='Admin')
    user_role = Role(nom='User')
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.commit()
    print("✅ Rôles ajoutés avec succès")

    
    admin_user = User(
        nom='Admin',
        prenom='Default',
        mail='admin@example.com',
        username='admin',  # Ajout du champ username
        role_id=admin_role.id
    )
    db.session.add(admin_user)
    db.session.commit()

    admin_login = Login(
        idUser=admin_user.id,
        username='admin',
        password=generate_password_hash('admin123').decode('utf-8')  
    )
    db.session.add(admin_login)
    db.session.commit()

    default_user = User(
        nom='User',
        prenom='Default',
        mail='user@example.com',
        username='user',  # Ajout du champ username
        role_id=user_role.id
    )
    db.session.add(default_user)
    db.session.commit()

    user_login = Login(
        idUser=default_user.id,
        username='user',
        password=generate_password_hash('user123').decode('utf-8') 
    )
    db.session.add(user_login)
    db.session.commit()

    print("✅ Utilisateurs par défaut ajoutés avec succès")

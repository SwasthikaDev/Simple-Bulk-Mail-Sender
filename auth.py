import bcrypt
from models import db, User

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user
    else:
        return None

def register(email, password, confirm_password):
    if password == confirm_password:
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    else:
        return "Passwords do not match"

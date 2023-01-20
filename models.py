from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_id(self):
        return self.id
    
    @property
    def is_authenticated(self):
        return True

    def __repr__(self):
        return f"<User {self.email}>"

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<Recipient {self.name}>"

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150),nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256))
    address = db.Column(db.String(150), nullable=False, unique=False)
    phone = db.Column(db.String(150), nullable=False, unique=False)
    gamepost = db.relationship('gamePost', backref='author', lazy=True)

    def __init__(self,username, email, password, address, phone):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.phone = phone

class gamePost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(150),nullable=False, unique=True)
    description = db.Column(db.String(300), nullable=False, unique=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __init__(self, game, description, user_id):
        self.game = game
        self.description = description
        self.user_id = user_id

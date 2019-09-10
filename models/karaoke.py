from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    profile = db.relationship('Profile', uselist=False, backref='user')
    song = db.relationship('Song', backref='selector')
    token = db.relationship('Token', uselist=False, backref='user')

    def __repr__(self):
        return "<User{}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Profile(db.Model):
    __tablename__='profiles'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255))
    gender = db.Column(db.Boolean, default=0)
    date_of_birth = db.Column(db.DateTime)
    avatar_url = db.Column(db.String)

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    song_id = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    thumbnail = db.Column(db.String, nullable=False)

class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
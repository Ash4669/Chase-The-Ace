# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    firstName = db.Column(db.String(1000), nullable=False)
    lastName = db.Column(db.String(1000), nullable=False)
    chaseTheAceWins = db.Column(db.Integer)

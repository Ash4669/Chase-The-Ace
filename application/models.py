# models.py

from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    firstName = db.Column(db.String(1000))
    lastName = db.Column(db.String(1000))
    chaseTheAceWins = db.Column(db.Integer)

class ChaseTheAce(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roomId = db.Column(db.Integer, unique = True)
    playerId = db.Column(db.String(100), unique = True)
    card = db.Column(db.String(10), unique = True)
    currentPlayer = db.Column(db.Integer)

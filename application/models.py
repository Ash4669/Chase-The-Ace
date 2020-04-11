# models.py

from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    chaseTheAceWins = db.Column(db.Integer)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, unique = True)
    roomId = db.Column(db.Integer, unique = True)
    gameType = db.Column(db.String(20))
    generatedPlayerId = db.Column(db.String(100), unique = True)
    card = db.Column(db.String(10), unique = True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roomId = db.Column(db.Integer, unique = True)
    gameType = db.Column(db.String(20))
    currentPlayer = db.Column(db.String(100))
    host = db.Column(db.Integer)

# models.py

from flask_login import UserMixin
from . import db

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
    userId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)
    generatedPlayerId = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100))
    card = db.Column(db.String(10))
    lives = db.Column(db.Integer)
    outOfGame = db.Column(db.Boolean)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roomId = db.Column(db.Integer, unique = True)
    gameType = db.Column(db.String(20))
    hostPlayerId = db.Column(db.String(100))
    currentPlayerId = db.Column(db.String(100))
    dealerPlayerId = db.Column(db.String(100))
    locked = db.Column(db.Boolean)
    deck = db.Column(db.String(1000))

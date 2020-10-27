# models.py

from flask_login import UserMixin
from . import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(250))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    chaseTheAceWins = db.Column(db.Integer)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    roomId = db.Column(db.Integer)
    generatedPlayerId = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    card = db.Column(db.String(20))
    lives = db.Column(db.Integer)
    outOfGame = db.Column(db.Boolean)
    socketId = db.Column(db.String(50))
#     Need to be careful because shed players could have the same room id. Need gameType parameter.

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomId = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(40))
    gameType = db.Column(db.String(20))
    numberOfLivesSet = db.Column(db.Integer)
    hostPlayerId = db.Column(db.String(100))
    currentPlayerId = db.Column(db.String(100))
    dealerPlayerId = db.Column(db.String(100))
    winningPlayerId = db.Column(db.String(100))
    locked = db.Column(db.Boolean)
    deck = db.Column(db.String(1000))

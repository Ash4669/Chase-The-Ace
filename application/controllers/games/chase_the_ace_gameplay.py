from flask import url_for, session
from __main__ import socketio
from __main__ import send, emit
from __main__ import join_room, leave_room
import random
from flask_login import current_user
import models
from app import db
from classes.Room import Room
from classes.player import Player
from classes.chase_the_ace.action import Action
import string
import json

def generateRoomId():
    return random.randint(1,999)

def generatePlayerId():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

# Initialisation of the game room.
@socketio.on('host game send')
def generate_and_host_redirect():

    # Generate a game id.
    roomId = generateRoomId()

    room = models.Room.query.filter_by(roomId = roomId).first()
    while room != None:
        roomId = generateRoomId()
        room = models.Room.query.filter_by(roomId = roomId).first()

    # Instantiate the Room with the room id as game id and store it within the database.
    newGame = models.Room(roomId = roomId, gameType = 'chase_the_ace', currentPlayer = None, host = None)
    db.session.add(newGame)
    db.session.commit()

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId = roomId)})


# Managing players joining the game.
@socketio.on('join chase the ace')
def on_join():

    # Generating a player id for the player.
    session['playerId'] = generatePlayerId()

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')
    # Need a way to allow players to make up a name on the spot if they're not signed in.

    # Send update to say who joined the room.
    emit('joined chase the ace announcement', playerName + ' has entered the room.', room = roomId)

    playerList = models.Player.query.filter_by(roomId = roomId).first()

    if playerList == None:
        setPlayerHost = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first()
        setPlayerHost.host = playerId
        db.session.commit()
        emit('setHost')

    newPlayer = models.Player(userId = userId, roomId = roomId, generatedPlayerId = playerId, name = playerName, card = None)
    db.session.add(newPlayer)
    db.session.commit()

    # Construct playerNames to send to clients.
    playerList = models.Player.query.filter_by(roomId = roomId).all()
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Join the flask room.
    join_room(roomId)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = roomId)
    emit('receive player id', playerId)

@socketio.on('quit chase the ace')
def on_quit():

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')

    # Remove the player from playerList that matches their player id.
    quittingPlayer = models.Player.query.filter_by(userId = userId, roomId = roomId, generatedPlayerId = playerId, name = playerName).one()
    db.session.delete(quittingPlayer)
    db.session.commit()

    # Construct playerNames to send to clients.
    playerList = models.Player.query.filter_by(roomId = roomId).all()
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = roomId)

    # Leave the flask room.
    leave_room(roomId)


@socketio.on('start game')
def start_game():

    roomId = session.get('roomId')

    # locking the game in the db to not allow others to join mid game.
    room = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first()
    room.locked = True
    db.session.commit()

    # Setting the lives of the players and their out of game statuses.
    playerList = models.Player.query.filter_by(roomId = roomId).all()
    for i in range(len(playerList)):
        playerList[i].lives = 3
        playerList[i].outOfGame = False
    db.session.commit()

    # Dealing the cards to the players.
    Action.dealCards(roomId)

    # Setting the host as the dealer and current player.
    roomHost = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first().host
    room.dealer = roomHost
    room.currentPlayer = roomHost # Setting now and updating after to reuse code.
    db.session.commit()
    emit('setDealer', roomHost, room = roomId)

    # Updating the current player as it cannot be the dealer
    Action.updateCurrentPlayer(roomId)

    # Extracts the playerData and to send a json.
    playerList = models.Player.query.filter_by(roomId = roomId).all()
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = roomId)

    # Giving the current player the choice.
    currentPlayerId = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first().currentPlayer
    emit('give player choice', currentPlayerId, room = roomId)

@socketio.on('stick card')
def stick_card(playerId):

    # incremements the player as their choice doesn't make a change.
    incrementPlayerid(getCurrentPlayer(room))

    # Gets the player list to extract the playerData and send a json.
    playerList = gameInstances[str(room)].playerList

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = room)

    # Setting the new current player
    currentPlayerId = playerList[getCurrentPlayer(room)].id

    # Giving the new current player the choice.
    emit('give player choice', currentPlayerId, room = room)


# Extract methods into a global methods file.

# Check signing in quickly and going straight to a game with the url to check an error, but proabbly wouldn't happen.
def jsonifyPlayerData(playerList, playersJson):
    for i in range(len(playerList)):
        player = playerList[i]
        playerData = {}
        playerData['id'] = player.generatedPlayerId
        playerData['name'] = player.name
        playerData['card'] = player.card
        playerData['lives'] = player.lives
        playerData['outOfGame'] = player.outOfGame
        jsonData = json.dumps(playerData)
        playersJson.append(jsonData)

def incrementPlayerid(currentPlayerNo):
    playerList = gameInstances[str(room)].playerList

    currentPlayerNo += 1


    if currentPlayerNo == len(PlayerList):
        currentPlayerNo = 0

    # Do something with the database

def getCurrentPlayer(room):
    pass
    # Do something with the database

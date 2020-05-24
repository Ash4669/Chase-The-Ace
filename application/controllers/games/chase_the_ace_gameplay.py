from flask import url_for, session
from ... import socketio, send, emit, join_room, leave_room
import random
from flask_login import current_user
from ... import models
from ... import db
from ...classes.chase_the_ace.action import Action
import string
import json

def generateRoomId():
    return random.randint(1,999)

def generatePlayerId():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

# Initialisation of the game room.
@socketio.on('host game send')
def generateAndHostRedirect():

    # Generate a game id.
    roomId = generateRoomId()

    room = getRoom(roomId)
    while room != None:
        roomId = generateRoomId()
        room = getRoom(roomId)

    # Instantiate the Room with the room id as game id and store it within the database.
    newGame = models.Room(roomId = roomId, gameType = 'chase_the_ace', currentPlayerId = None, hostPlayerId = None)
    db.session.add(newGame)
    db.session.commit()

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId = roomId)})


# Managing players joining the game.
@socketio.on('join chase the ace')
def onJoin():

    # Generating a player id for the player.
    session['playerId'] = generatePlayerId()

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')
    # Need a way to allow players to make up a name on the spot if they're not signed in.

    # Send update to say who joined the room.
    emit('receive player id', playerId)
    emit('joined chase the ace announcement', playerName + ' has entered the room.', room = roomId)

    # Setting the host if no players are in the game.
    playerList = getPlayerList(roomId)
    if playerList == []:
        room = getRoom(roomId)
        room.hostPlayerId = playerId
        db.session.commit()

    # Added new player to db.
    newPlayer = models.Player(userId = userId, roomId = roomId, generatedPlayerId = playerId, name = playerName, card = None)
    db.session.add(newPlayer)
    db.session.commit()

    hostId = getGameHostId(roomId)
    emit('setHost', hostId)

    # Construct playerNames to send to clients.
    playerList = getPlayerList(roomId)
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Join the flask room.
    join_room(roomId)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = roomId)

@socketio.on('quit chase the ace')
def onQuit():

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')

    hostId = getGameHostId(roomId)
    if playerId == hostId:
        # Emit the redirect for the client to redirect with javascript.
        emit('close game', {'url': url_for('chase_the_ace.chase_the_ace_index')})

    # Remove the player from playerList that matches their player id.
    quittingPlayer = models.Player.query.filter_by(userId = userId, roomId = roomId, generatedPlayerId = playerId, name = playerName).one()
    db.session.delete(quittingPlayer)
    db.session.commit()

    # Construct playerNames to send to clients.
    playerList = getPlayerList(roomId)
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = roomId)

    # Leave the flask room.
    leave_room(roomId)


@socketio.on('start game')
def startGame():

    roomId = session.get('roomId')

    # locking the game in the db to not allow others to join mid game.
    room = getRoom(roomId)
    room.locked = True
    db.session.commit()

    # Setting the lives of the players and their out of game statuses.
    playerList = getPlayerList(roomId)
    for i in range(len(playerList)):
        playerList[i].lives = 3
        playerList[i].outOfGame = False
    db.session.commit()

    # Dealing the cards to the players.
    Action.dealCards(roomId)

    # Setting the host as the dealer and current player.
    roomHost = getGameHostId(roomId)
    room = getRoom(roomId)
    room.dealerPlayerId = roomHost
    room.currentPlayerId = roomHost # Setting now and updating after to reuse code.
    db.session.commit()
    emit('setDealer', roomHost, room = roomId)

    # Updating the current player as it cannot be the dealer
    Action.updateCurrentPlayer(roomId)

    # Extracts the playerData and to send a json.
    playerList = getPlayerList(roomId)
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = roomId)

    # Giving the current player the choice.
    currentPlayerId = getCurrentPlayerId(roomId)
    emit('give player choice', currentPlayerId, room = roomId)

@socketio.on('stick card')
def stickCard(playerId):

    roomId = session.get('roomId')

    # incremements the player as their choice doesn't make a change.
    Action.updateCurrentPlayer(roomId)

    # Gets the player list to extract the playerData and send a json.
    playerList = getPlayerList(roomId)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = roomId)

    # Giving the new current player the choice.
    currentPlayerId = getCurrentPlayerId(roomId)
    emit('give player choice', currentPlayerId, room = roomId)


@socketio.on('trade card')
def tradeCard():

    roomId = session.get('roomId')

    # Trades cards with the next person in the game.
    Action.tradeCards(roomId)

    # Incremements the player as their choice doesn't make a change.
    Action.updateCurrentPlayer(roomId)

    # Gets the player list to extract the playerData and send a json.
    playerList = getPlayerList(roomId)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = roomId)

    # Giving the new current player the choice.
    currentPlayerId = getCurrentPlayerId(roomId)
    emit('give player choice', currentPlayerId, room = roomId)


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

def getRoom(roomId):
    return models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first()

def getPlayerList(roomId):
    return models.Player.query.filter_by(roomId = roomId).all()

def getGameHostId(roomId):
    return getRoom(roomId).hostPlayerId

def getCurrentPlayerId(roomId):
    return getRoom(roomId).currentPlayerId

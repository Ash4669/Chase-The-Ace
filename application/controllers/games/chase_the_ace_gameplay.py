from flask import url_for, session
from ... import socketio, send, emit, join_room, leave_room
import random
from flask_login import current_user
from ... import models
from ... import db
from ...classes.chase_the_ace.action import Action
from ...classes.chase_the_ace.databaseUtils import DatabaseUtils
import string
import json

dbUtils = DatabaseUtils()

def generateRoomId():
    return random.randint(1, 999)

def generatePlayerId():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

# Initialisation of the game room.
@socketio.on('host game send')
def generateAndHostRedirect():

    # Generate a game id.
    roomId = generateRoomId()

    room = dbUtils.getRoom(roomId)
    while room != None:
        roomId = generateRoomId()
        room = dbUtils.getRoom(roomId)

    # Instantiate the Room with the room id as game id and store it within the database.
    newGame = models.Room(roomId=roomId, gameType='chase_the_ace', currentPlayerId=None, hostPlayerId=None)
    db.session.add(newGame)
    db.session.commit()

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId=roomId)})


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
    emit('joined chase the ace announcement', playerName + ' has entered the room.', room=roomId)

    # Setting the host if no players are in the game.
    playerList = dbUtils.getPlayerList(roomId)
    if playerList == []:
        room = dbUtils.getRoom(roomId)
        room.hostPlayerId = playerId
        db.session.commit()

    # Added new player to db.
    newPlayer = models.Player(userId=userId, roomId=roomId, generatedPlayerId=playerId, name=playerName, card=None)
    db.session.add(newPlayer)
    db.session.commit()

    hostId = dbUtils.getGameHostId(roomId)
    emit('setHost', hostId)

    # Construct playerNames to send to clients.
    playerList = dbUtils.getPlayerList(roomId)
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Join the flask room.
    join_room(roomId)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room=roomId)

@socketio.on('quit chase the ace')
def onQuit():

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')

    hostId = dbUtils.getGameHostId(roomId)
    if playerId == hostId:
        # Emit the redirect for the client to redirect with javascript.
        emit('close game', {'url': url_for('chase_the_ace.chase_the_ace_index')}, room=roomId)

    # Remove the player from playerList that matches their player id.
    quittingPlayer = models.Player.query.filter_by(userId=userId, roomId=roomId, generatedPlayerId=playerId, name=playerName).one()
    db.session.delete(quittingPlayer)
    db.session.commit()

    # Construct playerNames to send to clients.
    playerList = dbUtils.getPlayerList(roomId)
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room=roomId)

    # Leave the flask room.
    leave_room(roomId)


@socketio.on('start game')
def startGame():

    roomId = session.get('roomId')

    if dbUtils.getRoom(roomId).locked != True:
        # locking the game in the db to not allow others to join mid game.
        room = dbUtils.getRoom(roomId)
        room.locked = True
        db.session.commit()

        # Setting the lives of the players and their out of game statuses.
        playerList = dbUtils.getPlayerList(roomId)
        for i in range(len(playerList)):
            playerList[i].lives = 3
            playerList[i].outOfGame = False
        db.session.commit()

        # Setting the host as the dealer and current player.
        roomHost = dbUtils.getGameHostId(roomId)
        room = dbUtils.getRoom(roomId)
        room.dealerPlayerId = roomHost
        room.currentPlayerId = roomHost
        db.session.commit()
        currentDealer = dbUtils.getDealerId(roomId)
        emit('setDealer', currentDealer, room = roomId)

    # Dealing the cards to the players.
    Action.dealCards(roomId)

    # Updating the current player as it cannot be the dealer
    Action.updateCurrentPlayer(roomId)

    # Extracts the playerData and to send a json.
    playerList = dbUtils.getPlayerList(roomId)
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = roomId)
    emit('update player lives', playersJson, room = roomId)

    # Giving the current player the choice.
    currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    emit('give player choice', currentPlayerId, room = roomId)

@socketio.on('stick card')
def stickCard():

    roomId = session.get('roomId')
    currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    dealerId = dbUtils.getDealerId(roomId)

    # increments the player as their choice doesn't make a change.
    Action.updateCurrentPlayer(roomId)

    # Gets the player list to extract the playerData and send a json.
    playerList = dbUtils.getPlayerList(roomId)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room=roomId)

    updatedCurrentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    if currentPlayerId == dealerId:
        # Dealer just stuck so end round.
        emit('reveal cards and trigger results', playersJson, room=roomId)

        endRound(roomId)
    else:
        # Giving the new current player the choice.
        emit('give player choice', updatedCurrentPlayerId, room=roomId)

@socketio.on('trade card')
def tradeCard():

    roomId = session.get('roomId')

    # Trades cards with the next person in the game.
    Action.tradeCards(roomId)

    # Increments the player as their choice doesn't make a change.
    Action.updateCurrentPlayer(roomId)

    # Gets the player list to extract the playerData and send a json.
    playerList = dbUtils.getPlayerList(roomId)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room=roomId)

    # Giving the new current player the choice.
    currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    emit('give player choice', currentPlayerId, room=roomId)

@socketio.on('cut card')
def cutCard():

    roomId = session.get('roomId')

    # Cut the deck for another card.
    Action.cutTheDeck(roomId)

    # Increments the player too match stick card functionality to line up ending the round regardless of choice.
    Action.updateCurrentPlayer(roomId)

    # Gets the player list to extract the playerData and send a json.
    playerList = dbUtils.getPlayerList(roomId)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room=roomId)

    # Dealer just stuck so end round.
    emit('reveal cards and trigger results', playersJson, room=roomId)

    endRound(roomId)

@socketio.on('delete all player cards')
def deletePlayerCardsDisplay():

    # Get room and send update to delete the all cards from previous round displayed by the playerList
    roomId = session.get('roomId')
    emit('delete player cards', room=roomId)


def jsonifyPlayerData(playerList, playersJson):
    for i in range(len(playerList)):
        player = playerList[i]
        playerData =\
            {'id': player.generatedPlayerId,
             'name': player.name,
             'card': player.card,
             'lives': player.lives,
             'outOfGame': player.outOfGame}
        jsonData = json.dumps(playerData)
        playersJson.append(jsonData)

def endRound(roomId):
    # Calculate the winner and adjust lives accordingly.
    Action.calculateWinner(roomId)

    # Extracts the playerData and to send a json.
    playerList = dbUtils.getPlayerList(roomId)
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Update players with their live count.
    emit('update player lives', playersJson, room=roomId)

    # Updates the dealer and sends it to all clients.
    Action.updateCurrentDealer(roomId)

    currentDealer = dbUtils.getDealerId(roomId)
    emit('setDealer', currentDealer, roomId)

    # Display new round button for the player to the left.
    emit('display new round button', room=roomId)

    #     NEED CONTINGENCY FOR WHEN BOTH PLAYER HAVE THE SAME CARD ON THE LAST ROUND AND BOTH LOSE.

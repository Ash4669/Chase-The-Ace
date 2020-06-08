from flask import url_for, session
from ... import socketio, send, emit
from ... import models
from ... import db
import random
from ...classes.chase_the_ace.databaseUtils import DatabaseUtils

dbUtils = DatabaseUtils()

def generateRoomId():
    return random.randint(1, 999)

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
    newGame = models.Room(roomId=roomId, gameType='chase_the_ace', currentPlayerId=None, hostPlayerId=None, winningPlayerId=None)
    db.session.add(newGame)
    db.session.commit()

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId=roomId)})


# Join an already initialised game room.
@socketio.on('join game send')
def JoinGameRedirect(roomId):

    room = dbUtils.getRoom(roomId)
    if room == None:
        emit("game doesn't exist")
    elif room.locked == True:
        emit("game has already started")
    else:
        # Emit the redirect for the client to redirect with javascript.
        emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId=roomId)})
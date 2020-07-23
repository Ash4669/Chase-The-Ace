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
def generateAndHostRedirect(password, lives):

    # Stores password set by host in session to check host against own password.
    session['ChaseTheAcePassword'] = password

    roomId = generateRoomId()

    # Checking to see if room exists, and if so, generate a new id and retry.
    room = dbUtils.getRoom(roomId)
    while room is not None:
        roomId = generateRoomId()
        room = dbUtils.getRoom(roomId)

    # Instantiate the Room with the room id as game id and store it within the database.
    newGame = models.Room(roomId=roomId, password=password, gameType='chase_the_ace', numberOfLivesSet=lives, currentPlayerId=None, hostPlayerId=None, winningPlayerId=None)
    db.session.add(newGame)
    db.session.commit()

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId=roomId)})


# Join an already initialised game room.
@socketio.on('join game send')
def joinGameRedirect(roomId, password):

    # Checking to see if room exists, and if so, check it isn't locked and join otherwise.
    room = dbUtils.getRoom(roomId)
    if room is None:
        emit("game doesn't exist")
    elif room.locked is True:
        emit("game has already started")
    else:
        if password != room.password and password is not None:
            emit("incorrect password")
        else:
            session['ChaseTheAcePassword'] = password
            # Emit the redirect for the client to redirect with javascript.
            emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', roomId=roomId)})


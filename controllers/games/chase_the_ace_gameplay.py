from flask import url_for, session
from __main__ import socketio
from __main__ import send, emit
from __main__ import join_room, leave_room
import random
from flask_login import current_user
from classes.Room import Room

gameInstances = {}

def generateId():
    return random.randint(100,999)

@socketio.on('host game send')
def generate_and_host_redirect():
    gameId = generateId()
    gameInstances[str(gameId)] = Room(gameId)
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', gameId = gameId)})

@socketio.on('join chase the ace')
def on_join():
    room = session.get('gameId')
    playerName = session.get('playerName')
    emit('joined chase the ace announcement', playerName + ' has entered the room.', room = room)

    roomPlayerList = gameInstances[str(room)].playerList
    roomPlayerList.append(session.get('playerName'))
    join_room(room)
    emit('update chase the ace playerList', roomPlayerList, room = room)

@socketio.on('quit chase the ace')
def on_quit():
    room = session.get('gameId')
    playerName = session.get('playerName')
    roomPlayerList = gameInstances[str(room)].playerList
    roomPlayerList.remove(playerName)
    emit('update chase the ace playerList', roomPlayerList, room = room)
    leave_room(room)
    # can't emit to room since thte connection has dropped.

# careful with removing players from playerList as they may have the same name.

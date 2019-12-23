from flask import url_for, session
from __main__ import socketio
from __main__ import send, emit
from __main__ import join_room, leave_room
import random
from flask_login import current_user

def generateId():
    return random.randint(100,999)

@socketio.on('host game send')
def generate_and_host_redirect():
    gameId = generateId()
    session['gameId'] = gameId
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', gameId = gameId)})

@socketio.on('join')
def on_join():
    room = session.get('gameId')
    join_room(room)
    playerName = session.get('playerName')
    # roomData['players'].push(playerName);
    emit('joined', playerName + ' has entered the room.', room = room)

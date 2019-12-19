from flask import url_for
from __main__ import socketio
from __main__ import send, emit
import random


def generateid():
    return random.randint(100,999)

@socketio.on('host game send')
def generate_and_host_redirect():
    game_id = generateid()
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', game_id = game_id)})

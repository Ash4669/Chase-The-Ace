# chase_the_ace.py

from flask import Blueprint, render_template, redirect, url_for
# from pusher import pusher
# from flask_socketio import SocketIO, emit
import configparser
from __main__ import socketio
from flask_socketio import send, emit
from controllers.auth import auth as auth_blueprint
import random

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():
    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<game_id>')
def chase_the_ace_instance(game_id):
    return render_template('games/chase_the_ace/index.html', game_id = game_id)

def generateid():
    return random.randint(100,999)

@socketio.on('host game send')
def generate_and_host_redirect():
    game_id = generateid()
    socketio.emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', game_id = game_id)})

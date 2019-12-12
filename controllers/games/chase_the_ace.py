# chase_the_ace.py

from flask import Blueprint, render_template, redirect, url_for
# from pusher import pusher
# from flask_socketio import SocketIO, emit
import configparser
from __main__ import socketio

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():

    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<game_id>')
def chase_the_ace_instance(game_id):
    # pusher_client.trigger('my-channel', 'first-alert', {'message': 'hello world' + str(game_id)})
    return render_template('games/chase_the_ace/index.html', game_id = game_id)

@chase_the_ace.route('/play/chase_the_ace/redirect<game_id>')
def chase_the_ace_redirect(game_id):
    redirect('http://127.0.0.1:5000/play/chase_the_ace/' + str(game_id))

def generateid():
    print('Game id generated.')
    return 1

@socketio.on('host game send')
def generate_and_host_redirect(json):
    print('here')
    gameId = generateid()
    return redirect(url_for('chase_the_ace.chase_the_ace_instance', game_id = 1))

# chase_the_ace.py

from flask import Blueprint, render_template
# from pusher import pusher
# from flask_socketio import SocketIO, emit
import configparser
from app import socketio

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():

    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<int:game_id>')
def chase_the_ace_instance(game_id):
    # pusher_client.trigger('my-channel', 'first-alert', {'message': 'hello world' + str(game_id)})
    return render_template('games/chase_the_ace/index.html', id = game_id, pusher_key = config.get('PUSHERDETAILS','key'), pusher_cluster = config.get('PUSHERDETAILS','cluster'))


def generateid():
    print('Game id generated.')

@socketio.on('host game send')
def generate_and_host_redirect(json):
    print('here')
    gameId = generateid()
    return redirect(url_for('chase_the_ace.chase_the_ace_instance', game_id = gameId))

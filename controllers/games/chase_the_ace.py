# chase_the_ace.py

from flask import Blueprint, render_template
# from pusher import pusher
# import socketio
import configparser

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

# # create a Socketio Server
# sio = socketio.AsyncClient()
#
# @sio.event
# def connect():
#     print('connection established')
#
# @sio.event
# def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})
#
# @sio.event
# def disconnect():
#     print('disconnected from server')

# sio.connect('http://127.0.0.1:5000/play/chase_the_ace/1')
# print('my sid is', sio.sid)

# pusher = pusher_client = pusher.Pusher(
#   app_id  = config.get('PUSHERDETAILS','app_id'),
#   key     = config.get('PUSHERDETAILS','key'),
#   secret  = config.get('PUSHERDETAILS','secret'),
#   cluster = config.get('PUSHERDETAILS','cluster'),
#   ssl     = bool(config.get('PUSHERDETAILS','ssl'))
# )

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():

    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<int:game_id>')
def chase_the_ace_instance(game_id):
    # pusher_client.trigger('my-channel', 'first-alert', {'message': 'hello world' + str(game_id)})
    return render_template('games/chase_the_ace/index.html', id = game_id, pusher_key = config.get('PUSHERDETAILS','key'), pusher_cluster = config.get('PUSHERDETAILS','cluster'))

# @sio.on('message')
# def handle_message(message):
#     print('received message: ' + message)


# def connect_handler():
#     if current_user.is_authenticated:
#         emit('my response',
#              {'message': '{0} has joined'.format(current_user.name)},
#              broadcast=True)
#     else:
#         return False  # not allowed here

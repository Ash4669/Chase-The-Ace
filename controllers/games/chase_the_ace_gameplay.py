from flask import url_for, session
from __main__ import socketio
from __main__ import send, emit
from __main__ import join_room, leave_room
import random
from flask_login import current_user
from classes.Room import Room
from classes.player import Player
from classes.card import Card
import string

gameInstances = {}

def generateGameId():
    return random.randint(100,999)

def generatePlayerId():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

@socketio.on('host game send')
def generate_and_host_redirect():

    # Generate a game id.
    gameId = generateGameId()

    # Instantiate the instace of room with the game id as the room id.
    gameInstances[str(gameId)] = Room(gameId)

    # Emit the redirect for the client to redirect with javascript.
    emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_instance', gameId = gameId)})

@socketio.on('join chase the ace')
def on_join():

    # Generating a player id for the player.
    session['playerId'] = generatePlayerId()

    # Pulling game id, player id and player name from session.
    room = session.get('gameId')
    playerId = session['playerId']
    playerName = session.get('playerName')

    # Send update to say who joined the room.
    emit('joined chase the ace announcement', playerName + ' has entered the room.', room = room)

    # Setting player list for code simplicity and cleanliness.
    playerList = gameInstances[str(room)].playerList

    # Setting the first player as the host.
    # Be careful with people joining and quitting the same room.
    # Kick out when host leaves and delete instance.
    if len(playerList) == 0:
        emit('setHost')

    # Append new player into player list in room in game instances.
    playerList.append(Player(playerId, playerName))

    # Initialise playerNames and append on new player.
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Join the flask room.
    join_room(room)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = room)

@socketio.on('quit chase the ace')
def on_quit():

    # Pulling game id, player id and player name from session.
    room = session.get('gameId')
    playerId = session.get("playerId")
    playerName = session.get('playerName')

    # Setting player list for code simplicity and cleanliness.
    playerList = gameInstances[str(room)].playerList

    # Remove the player from playerList that matches their player id.
    for i in range(len(playerList)):
        if playerList[i].id == playerId:
            playerList.pop(i)
            break


    # Initialise playerNames and append on new player.
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room = room)

    # Leave the flask room.
    leave_room(room)


@socketio.on('start game')
def start_game():
    roomPlayerList = gameInstances[str(room)].playerList

# Check signing in quickly and going straight to a game with the url to check an error, but proabbly wouldn't happen.

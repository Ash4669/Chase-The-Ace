from flask import url_for, session
from __main__ import socketio
from __main__ import send, emit
from __main__ import join_room, leave_room
import random
from flask_login import current_user
from classes.Room import Room
from classes.player import Player
from classes.chase_the_ace.action import Action
import string
import json

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
    playerId = session.get('playerId')
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
    emit('receive player id', playerId)

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
    room = session.get('gameId')
    playerList = gameInstances[str(room)].playerList

    # Setting the dealer, lives of the players and their out of game statuses.
    for i in range(len(playerList)):
        playerList[i].dealer = False
        playerList[i].lives = 3
        playerList[i].outOfGame = False

    Action.dealCards(playerList)

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Setting the current player
    currentPlayerId = playerList[getCurrentPlayer(room)].id

    # Updating the player data on client side
    emit('update player data', playersJson, room = room)

    # Giving the current player the choice.
    emit('give player choice', currentPlayerId, room = room)

@socketio.on('stick card')
def stick_card(playerId):

    # incremements the player as their choice doesn't make a change.
    incrementPlayerid(getCurrentPlayer(room))

    # Gets the player list to extract the playerData and send a json.
    playerList = gameInstances[str(room)].playerList

    # Extracts the playerData and to send a json.
    playersJson = []
    jsonifyPlayerData(playerList, playersJson)

    # Updating the player data on client side
    emit('update player data', playersJson, room = room)

    # Setting the new current player
    currentPlayerId = playerList[getCurrentPlayer(room)].id

    # Giving the new current player the choice.
    emit('give player choice', currentPlayerId, room = room)

# Check signing in quickly and going straight to a game with the url to check an error, but proabbly wouldn't happen.
def jsonifyPlayerData(playerList, playersJson):
    for i in range(len(playerList)):
        playerData = json.dumps(playerList[i].__dict__)
        playersJson.append(playerData)

def incrementPlayerid(currentPlayerNo):
    playerList = gameInstances[str(room)].playerList

    currentPlayerNo += 1


    if currentPlayerNo == len(PlayerList):
        currentPlayerNo = 0

    # Do something with the database

def getCurrentPlayer(room):
    pass
    # Do something with the database

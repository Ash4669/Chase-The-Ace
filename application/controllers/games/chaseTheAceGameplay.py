from flask import url_for, session
from ... import socketio, send, emit, join_room, leave_room
from flask import request
import random
from ... import models
from ... import db
from ...classes.chase_the_ace.action import Action
from ...classes.chase_the_ace.databaseUtils import DatabaseUtils
from ...classes.utils.jsonUtils import JsonUtils
import string

dbUtils = DatabaseUtils()
jsonUtils = JsonUtils()

def generatePlayerId():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])

# Managing players joining the game.
@socketio.on('join chase the ace')
def onJoin():

    # Generating a player id for the player.
    session['playerId'] = generatePlayerId()
    session['playerSockedId'] = request.sid

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')
    socketId = session.get('playerSockedId')
    # Need a way to allow players to make up a name on the spot if they're not signed in.

    gamePassword = dbUtils.getRoom(roomId).password
    password = session.get('ChaseTheAcePassword')

    if gamePassword != "" and password != gamePassword:
        emit('redirect', {'url': url_for('chase_the_ace.chase_the_ace_index')})

    else:
        # Send update to say who joined the room.
        emit('receive player id', playerId)
        emit('joined chase the ace announcement', playerName + ' has entered the room.', room=roomId)

        # Setting the host if no players are in the game.
        playerList = dbUtils.getPlayerList(roomId)
        if playerList == []:
            room = dbUtils.getRoom(roomId)
            room.hostPlayerId = playerId
            db.session.commit()

        # Added new player to db.
        newPlayer = models.Player(userId=userId, roomId=roomId, generatedPlayerId=playerId, name=playerName, card=None, socketId=socketId)
        db.session.add(newPlayer)
        db.session.commit()

        hostId = dbUtils.getGameHostId(roomId)
        emit('set host', (hostId, roomId, gamePassword))
        emit('set dealer', hostId)

        numberOfLivesSet = dbUtils.getRoom(roomId).numberOfLivesSet
        emit('set max player lives', numberOfLivesSet)

        # Construct playerNames to send to clients.
        playerList = dbUtils.getPlayerList(roomId)
        playerNames = []
        for i in range(len(playerList)):
            playerNames.append(playerList[i].name)

        # Join the flask room.
        join_room(roomId)

        # Emit to the room to update all other players of the change to the player name list.
        emit('update chase the ace playerList', playerNames, room=roomId)

@socketio.on('quit chase the ace')
def onQuit():

    # Pulling game id, player id and player name from session.
    roomId = session.get('roomId')
    userId = session.get('userId')
    playerId = session.get('playerId')
    playerName = session.get('userFullName')

    hostId = dbUtils.getGameHostId(roomId)
    if playerId == hostId:
        # Emit the redirect for the client to redirect with javascript.
        emit('close game', {'url': url_for('chase_the_ace.chase_the_ace_index')}, room=roomId)

    # Remove the player from playerList that matches their player id.
    quittingPlayer = models.Player.query.filter_by(userId=userId, roomId=roomId, generatedPlayerId=playerId, name=playerName).one()
    db.session.delete(quittingPlayer)
    db.session.commit()

    # Construct playerNames to send to clients.
    playerList = dbUtils.getPlayerList(roomId)
    playerNames = []
    for i in range(len(playerList)):
        playerNames.append(playerList[i].name)

    # Emit to the room to update all other players of the change to the player name list.
    emit('update chase the ace playerList', playerNames, room=roomId)

    # Leave the flask room.
    leave_room(roomId)


@socketio.on('start game')
def startGame():

    roomId = session.get('roomId')

    if dbUtils.getRoom(roomId).locked != True:
        # locking the game in the db to not allow others to join mid game.
        room = dbUtils.getRoom(roomId)
        room.locked = True
        db.session.commit()

        # Setting the lives of the players and their out of game statuses.
        playerList = dbUtils.getPlayerList(roomId)
        numberOfLivesSet = dbUtils.getRoom(roomId).numberOfLivesSet
        for i in range(len(playerList)):
            playerList[i].lives = numberOfLivesSet
            playerList[i].outOfGame = False
        db.session.commit()

        # Setting the host as the dealer and current player.
        roomHost = dbUtils.getGameHostId(roomId)
        room = dbUtils.getRoom(roomId)
        room.dealerPlayerId = roomHost
        room.currentPlayerId = roomHost
        db.session.commit()

    # Dealing the cards to the players.
    Action.dealCards(roomId)

    # Updating the player data on client side.
    playerList = dbUtils.getPlayerList(roomId)
    for player in playerList:
        playerJson = jsonUtils.jsonifyPlayerData(player)
        emit('update player data', playerJson, room=player.socketId)

    # Updating all players on client side.
    playerListJson = jsonUtils.jsonifyPlayerListData(playerList)

    emit('update player lives', playerListJson, room=roomId)

    # Updating the current player as it cannot be the dealer
    Action.updateCurrentPlayer(roomId, previousPlayer='dealer')

    handleKingAndGiveChoice(roomId)

@socketio.on('stick card')
def stickCard():

    roomId = session.get('roomId')
    currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    dealerId = dbUtils.getDealerId(roomId)

    if currentPlayerId == dealerId:
        endRound(roomId)
    else:
        # increments the player as their choice doesn't make a change.
        Action.updateCurrentPlayer(roomId, previousPlayer='player')

        handleKingAndGiveChoice(roomId)

@socketio.on('trade card')
def tradeCard():

    roomId = session.get('roomId')

    # Trades cards with the next person in the game.
    Action.tradeCards(roomId)

    # Updating the player data on client side
    playerList = dbUtils.getPlayerList(roomId)
    for player in playerList:
        playerJson = jsonUtils.jsonifyPlayerData(player)
        emit('update player data', playerJson, room=player.socketId)

    # Increments the player as their choice doesn't make a change.
    Action.updateCurrentPlayer(roomId, previousPlayer='player')

    handleKingAndGiveChoice(roomId)

@socketio.on('cut card')
def cutCard(cardIndex):

    roomId = session.get('roomId')

    # Cut the deck for another card.
    Action.cutTheDeck(roomId, cardIndex)

    # Increments the player too match stick card functionality to line up ending the round regardless of choice.
    Action.updateCurrentPlayer(roomId, previousPlayer='player')

    # Updating the player data on client side
    playerList = dbUtils.getPlayerList(roomId)
    for player in playerList:
        playerJson = jsonUtils.jsonifyPlayerData(player)
        emit('update player data', playerJson, room=player.socketId)

    endRound(roomId)

@socketio.on('reveal king')
def revealKing():
    roomId = session.get('roomId')
    playerId = session.get('playerId')

    # Prepare player data to emit it to all players.
    playerList = dbUtils.getPlayerList(roomId)
    playerListJson = jsonUtils.jsonifyPlayerListData(playerList)

    emit('reveal king of playerId', (playerListJson, playerId), room=roomId)

@socketio.on('delete all player cards')
def deletePlayerCardsDisplay():

    # Get room and send update to delete the all cards from previous round displayed by the playerList
    roomId = session.get('roomId')
    emit('delete player cards', room=roomId)

def endRound(roomId):
    # Prepare player data to emit it to all players.
    playerList = dbUtils.getPlayerList(roomId)
    playerListJson = jsonUtils.jsonifyPlayerListData(playerList)

    emit("delete dealer title", room=roomId)

    # Revealing all the cards at the end of the round.
    emit('reveal all cards', playerListJson, room=roomId)

    # Calculate the winner and adjust lives accordingly.
    Action.calculateRoundWinner(roomId)

    # Extracts the playerData and to send a json.
    playerList = dbUtils.getPlayerList(roomId)
    playerListJson = jsonUtils.jsonifyPlayerListData(playerList)

    # Update players with their live count.
    emit('update player lives', playerListJson, room=roomId)

    # If a winner isn't set, continue, otherwise send winner to all players
    room = dbUtils.getRoom(roomId)
    if room.winningPlayerId is None:

        # Updates the dealer and sends it to all clients.
        Action.updateCurrentDealer(roomId)

        currentDealer = dbUtils.getDealerId(roomId)
        emit('set dealer', currentDealer, roomId)

        # Display new round button for the player to the left.
        emit('display new round button', room=roomId)

    else:
        winningId = room.winningPlayerId
        emit('trigger winner', winningId, room=roomId)
        dbUtils.addWinToUser(winningId)

def handleKingAndGiveChoice(roomId):
    # Giving the current player the choice.
    currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
    dealerPlayerId = dbUtils.getDealerId(roomId)
    currentPlayerCard = dbUtils.getPlayerCard(roomId, currentPlayerId)

    while 'king' in currentPlayerCard:
        # Destroy the reveal button since the player's king is revealed when they skip their go.
        emit('delete reveal button for player', currentPlayerId, room=roomId)
        if currentPlayerId == dealerPlayerId:
            emit("reveal dealer king", room=roomId)
            endRound(roomId)
            break
        else:
            Action.updateCurrentPlayer(roomId, previousPlayer='player')
            currentPlayerId = dbUtils.getCurrentPlayerId(roomId)
            currentPlayerCard = dbUtils.getPlayerCard(roomId, currentPlayerId)

    # If the player has a king, they would be skipped regardless, but if the dealer has a king when the round ends
    # the current player is on round end and the dealer mustn't get a choice.
    if 'king' not in currentPlayerCard:
        emit('give player choice', currentPlayerId, room=roomId)

from ..card import Card
import random
from ... import db
from .databaseUtils import DatabaseUtils
from ast import literal_eval
from ... import socketio, send, emit

dbUtils = DatabaseUtils()


class Action:

    def dealCards(roomId):
        # Makes copy of cards deck to deal to the players (always using a new full deck.)
        currentDeck = Card.cards[:]

        # Shuffle the deck of cards.
        random.shuffle(currentDeck)

        # Retrieving the list of players.
        playerList = dbUtils.getPlayerList(roomId)
        room = dbUtils.getRoom(roomId)

        # If the player isn't out of the game, then give them the top card off the deck.
        for player in playerList:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = None

        # Store a serialised version of the deck for later use.
        room.deck = repr(currentDeck)

        # Commit changes
        db.session.commit()

    def updateCurrentPlayer(roomId, previousPlayer):
        # Retrieving the list of players and the room data.
        playerList = dbUtils.getPlayerList(roomId)
        room = dbUtils.getRoom(roomId)

        if previousPlayer == 'dealer':
            currentPlayerId = room.dealerPlayerId
        elif previousPlayer == 'player':
            currentPlayerId = room.currentPlayerId

        for i in range(len(playerList)):
            player = playerList[i]

            # Getting the generated id of the next player who is still in the game.
            if player.generatedPlayerId == currentPlayerId:
                while True:
                    if i == len(playerList) - 1:
                        i -= len(playerList)
                    nextPlayer = playerList[i + 1]
                    if not nextPlayer.outOfGame:
                        break
                    i += 1
                room.currentPlayerId = nextPlayer.generatedPlayerId
                break

        # Commit changes
        db.session.commit()

    def updateCurrentDealer(roomId):
        # Retrieving the list of players and the room data.
        playerList = dbUtils.getPlayerList(roomId)
        room = dbUtils.getRoom(roomId)

        for i in range(len(playerList)):
            player = playerList[i]

            # Getting the generated id of the next player to the dealer who is still in the game.
            if player.generatedPlayerId == room.dealerPlayerId:
                while True:
                    if i == len(playerList) - 1:
                        i -= len(playerList)
                    nextPlayer = playerList[i + 1]
                    if not nextPlayer.outOfGame:
                        break
                    i += 1
                room.dealerPlayerId = nextPlayer.generatedPlayerId
                break

        # Commit changes
        db.session.commit()

    def tradeCards(roomId):
        # Retrieving the list of players and the room data.
        playerList = dbUtils.getPlayerList(roomId)
        room = dbUtils.getRoom(roomId)

        for i in range(len(playerList)):
            # Getting the current player.
            player = playerList[i]

            # Getting the generated id of the player next to the player.
            if player.generatedPlayerId == room.currentPlayerId:

                # If the current player is at the edge of the array, then set it back to
                # before the start so the next player is then the first in the array.
                while True:
                    if i == len(playerList) - 1:
                        i -= len(playerList)
                    nextPlayer = playerList[i + 1]
                    if not nextPlayer.outOfGame:
                        break
                    i += 1

                playerCard = player.card
                nextPlayerCard = nextPlayer.card

                if 'king' in nextPlayerCard and nextPlayer.generatedPlayerId != room.dealerPlayerId:
                    emit('next player has a king')
                    # Add reveal king emit here for entire room. send position in list ?
                else:
                    player.card = nextPlayerCard
                    nextPlayer.card = playerCard
                break

        # Commit changes
        db.session.commit()

    def cutTheDeck(roomId, cardIndex):
        # Retrieving the list of players and the room data.
        playerList = dbUtils.getPlayerList(roomId)
        room = dbUtils.getRoom(roomId)

        # Retrieve the current deck.
        currentDeck = literal_eval(room.deck)

        # Loop over all players, find the dealer give them a new card of the top of the deck.
        for i in range(len(playerList)):
            player = playerList[i]

            if player.generatedPlayerId == room.dealerPlayerId:
                player.card = currentDeck.pop(int(cardIndex))
                break

        # Commit changes
        db.session.commit()

    def calculateRoundWinner(roomId):
        # Get the list of players
        playerList = dbUtils.getPlayerList(roomId)

        # Create storage for the playerIds and the card values.
        idsAndCards = {}

        # Setting the dictionary key as the playerId and value as the card numerical value
        # by parsing the string to an int and adjusting for special cards.
        for i in range(len(playerList)):

            # If the player is not in the game then ignore their (unset) card
            if not playerList[i].outOfGame:
                card = playerList[i].card
                id = playerList[i].generatedPlayerId

                if 'ace' in card:
                    idsAndCards[id] = 1
                elif 'jack' in card:
                    idsAndCards[id] = 11
                elif 'queen' in card:
                    idsAndCards[id] = 12
                elif 'king' in card:
                    idsAndCards[id] = 13
                elif '10' in card:
                    idsAndCards[id] = 10
                else:
                    idsAndCards[id] = int(card[0])

        # Getting the minimum of the card values.
        minimumCardValue = idsAndCards[min(idsAndCards.keys(), key=(lambda k: idsAndCards[k]))]

        # Check whether the round is a draw.
        allEqual = True
        for cardValue in idsAndCards.values():
            if cardValue != minimumCardValue:
                allEqual = False
                break

        if allEqual:
            for i in range(len(playerList)):
                player = playerList[i]
                if not player.outOfGame:
                    if player.lives != 1:
                        allEqual = False
                        break

        # If the game is not a draw or the players have more than one life each then calculate the loser/s
        if not allEqual:
            # Subtracting a life off of all players with lowest cards.
            for playerId, cardValue in idsAndCards.items():
                if cardValue == minimumCardValue:
                    player = dbUtils.getSpecificPlayer(roomId, playerId)
                    player.lives -= 1

                    # If the player has no lives left, they are set as out of the game.
                    if player.lives == 0:
                        player.outOfGame = True
                    db.session.commit()

            # Checking for a winner.
            Action.checkForGameWinner(roomId)

    def checkForGameWinner(roomId):
        idsAndLives = {}
        playerList = dbUtils.getPlayerList(roomId)
        for i in range(len(playerList)):
            outOfGame = playerList[i].outOfGame
            playerId = playerList[i].generatedPlayerId
            idsAndLives[playerId] = outOfGame

        # Checking only one is still in the game.
        counter = 0
        for playerId, outOfGame in idsAndLives.items():
            if not outOfGame:
                counter += 1

        # Set the last surviving player as the winner.
        if counter == 1:
            for playerId, outOfGame in idsAndLives.items():
                if not outOfGame:
                    winningPlayer = playerId
                    break
            room = dbUtils.getRoom(roomId)
            room.winningPlayerId = winningPlayer
            db.session.commit()

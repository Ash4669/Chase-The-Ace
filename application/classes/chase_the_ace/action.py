from ..card import Card
import random
from ... import models
from ... import db

class Action():

    def dealCards(roomId):

        # Makes copy of cards deck to deal to the players (always using a new full deck.)
        currentDeck = Card.cards[:]

        # Shuffle the deck of cards.
        random.shuffle(currentDeck)

        # Retrieving the list of players.
        playerList = models.Player.query.filter_by(roomId = roomId).all()

        # If the player isn't out of the game, then give them the top card off the deck.
        for player in playerList:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = None

        # Commit changes
        db.session.commit()

    def updateCurrentPlayer(roomId):

        # Retrieving the list of players and the room data.
        playerList = models.Player.query.filter_by(roomId = roomId).all()
        room = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first()

        for i in range(len(playerList)):
            player = playerList[i]

            # Getting the generated id of the player next to the dealer.
            if player.generatedPlayerId == room.currentPlayerId:
                if i == len(playerList) - 1:
                    i -= len(playerList)
                nextPlayerId = playerList[i+1].generatedPlayerId
                room.currentPlayerId = nextPlayerId
                break
        db.session.commit()

    def tradeCards(roomId):

        # Retrieving the list of players and the room data.
        playerList = models.Player.query.filter_by(roomId = roomId).all()
        room = models.Room.query.filter_by(roomId = roomId, gameType = 'chase_the_ace').first()

        for i in range(len(playerList)):
            # Getting the current player.
            player = playerList[i]

            # Getting the generated id of the player next to the dealer.
            if player.generatedPlayerId == room.currentPlayerId:

                # If the current player is at the edge of the array, then set it back to
                # before the start so the next player is then the first in the array.
                if i == len(playerList) - 1:
                    i -= len(playerList)

                nextPlayer = playerList[i+1]

                playerCard = player.card
                nextPlayerCard = nextPlayer.card

                player.card = nextPlayerCard
                nextPlayer.card = playerCard
                break

        db.session.commit()

    def cutCard(roomId):

        # Makes copy of cards deck to deal to the players (always using a new full deck.)
        currentDeck = Card.cards[:]

        # Shuffle the deck of cards.
        random.shuffle(currentDeck)

        # Retrieving the list of players.
        playerList = models.Player.query.filter_by(roomId = roomId).all()

        # If the player isn't out of the game, then give them the top card off the deck.
        for player in playerList:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = None

        # Commit changes
        db.session.commit()

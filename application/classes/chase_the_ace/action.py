from ..card import Card
import random

class Action():

    def dealCards(players):

        # Makes copy of cards deck to deal to the players (always using a new full deck.)
        currentDeck = Card.cards[:]

        # Shuffle the deck of cards.
        random.shuffle(currentDeck)

        # If the player isn't out of the game, then give them the top card off the deck.
        for player in players:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = None

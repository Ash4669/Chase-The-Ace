from classes.card import Card
from classes.player import Player
import random

class Action():

    def dealCards(players):
        # print(Card.cards) NEEDS FIXING. Takes card out of original array. Not temporary array. Depletes all original cards.
        currentDeck = Card.cards
        random.shuffle(currentDeck)
        for player in players:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = ""

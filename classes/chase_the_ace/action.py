from classes.card import Card
from classes.player import Player
import random

class Action():

    def dealCards(players):
        currentDeck = Card.cards
        random.shuffle(currentDeck)
        print(Card.cards)
        for player in players:
            if player.outOfGame == False:
                player.card = currentDeck.pop(0)
            else:
                player.card = ""

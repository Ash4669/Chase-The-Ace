import random

class Suit(object):

    def getSuit():
        suitNumber = round(random.random()*3)
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        suit = suits[suitNumber]
        return suit

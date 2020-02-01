from classes.cards.number import Number
from classes.cards.suit import Suit

class Card(object):

    outOfDeck = list()

    def getCard():
        return [Suit.getSuit(), Number.getNumber()]

    def inPlay(card):
        Card.outOfDeck.append(card)

    def clearInPlay():
        Card.outOfDeck = list()

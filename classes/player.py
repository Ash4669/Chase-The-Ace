class Player(object):

    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @id.deleter
    def id(self):
        del self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        del self._name

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        self._card = card

    @card.deleter
    def card(self):
        del self._card

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, choice):
        self._choice = choice

    @choice.deleter
    def choice(self):
        del self._choice

    @property
    def dealer(self):
        return self._dealer

    @dealer.setter
    def dealer(self, dealer):
        self._dealer = dealer

    @dealer.deleter
    def dealer(self):
        del self._dealer

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, lives):
        self._lives = lives

    @lives.deleter
    def lives(self):
        del self._lives

    @property
    def outOfGame(self):
        return self._outOfGame

    @outOfGame.setter
    def outOfGame(self, outOfGame):
        self._outOfGame = outOfGame

    @outOfGame.deleter
    def outOfGame(self):
        del self._outOfGame

    def getActivePlayer():
        print("This is a list of the players.")

    def decision():
        print("This is the decision the player made.")

    def dealerDecision():
        print("This is the dealers decision.")

class Room(object):

    def __init__(self, id):
        self.id = id
        self._playerList = []

    @property
    def playerList(self):
        return self._playerList

    @playerList.setter
    def playerList(self, playerList):
        self._playerList = playerList

    @playerList.deleter
    def playerList(self):
        del self._playerList

    # @property
    # def player(self):
    #     return self._player
    #
    # @player.setter
    # def player(self, player):
    #     self._player = player
    #
    # @player.deleter
    # def player(self):
    #     del self._player

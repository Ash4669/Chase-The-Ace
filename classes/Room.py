class Room(object):

    def __init__(self, id):
        self.id = id
        self.playerList = []

    @property
    def playerList(self):
        return self._playerList

    @playerList.setter
    def playerList(self, playerList):
        self._playerList = playerList

    @playerList.deleter
    def playerList(self):
        del self._playerList

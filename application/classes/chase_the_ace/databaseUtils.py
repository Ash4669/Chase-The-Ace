from ... import models

class DatabaseUtils():

    def getRoom(self, roomId):
        return models.Room.query.filter_by(roomId=roomId, gameType='chase_the_ace').first()

    def getPlayerList(self, roomId):
        return models.Player.query.filter_by(roomId=roomId).all()
    #     Need to be careful because shed players could have the same room id. Need gameType parameter. Or make roomId very unique.

    def getSpecificPlayer(self, roomId, playerId):
        return models.Player.query.filter_by(roomId=roomId, generatedPlayerId=playerId).first()

    def getGameHostId(self, roomId):
        return self.getRoom(roomId).hostPlayerId

    def getCurrentPlayerId(self, roomId):
        return self.getRoom(roomId).currentPlayerId

    def getDealerId(self, roomId):
        return self.getRoom(roomId).dealerPlayerId
# Refactor to be generic so I can pass in game type.
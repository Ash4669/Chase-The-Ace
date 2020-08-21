from ... import models
from ... import db


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

    def getSpecificPlayerSocketId(self, roomId, playerId):
        return self.getSpecificPlayer(roomId, playerId).socketId

    def getCurrentPlayerId(self, roomId):
        return self.getRoom(roomId).currentPlayerId

    def getDealerId(self, roomId):
        return self.getRoom(roomId).dealerPlayerId

    def getPlayerCard(self, roomId, playerId):
        return self.getSpecificPlayer(roomId, playerId).card

    # Make more generic later when new games are added.
    def addWinToUser(self, winningPlayerId):
        userId = models.Player.query.filter_by(generatedPlayerId=winningPlayerId).first().userId
        user = models.User.query.filter_by(id=userId).first()
        user.chaseTheAceWins += 1
        db.session.commit()


# Refactor to be generic so I can pass in game type.

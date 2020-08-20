import json


class JsonUtils:

    def jsonifyPlayerListData(self, playerList):
        playerListJson = []
        for i in range(len(playerList)):
            player = playerList[i]
            playerData = \
                {'id': player.generatedPlayerId,
                 'name': player.name,
                 'card': player.card,
                 'lives': player.lives,
                 'outOfGame': player.outOfGame}
            jsonData = json.dumps(playerData)
            playerListJson.append(jsonData)
        return playerListJson

    def jsonifyPlayerData(self, player):
        playerData = \
            {'id': player.generatedPlayerId,
             'name': player.name,
             'card': player.card,
             'lives': player.lives,
             'outOfGame': player.outOfGame}
        return json.dumps(playerData)

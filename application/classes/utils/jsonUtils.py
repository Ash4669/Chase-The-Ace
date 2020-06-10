import json


class JsonUtils:

    def jsonifyPlayerData(self, playerList, playersJson):
        for i in range(len(playerList)):
            player = playerList[i]
            playerData = \
                {'id': player.generatedPlayerId,
                 'name': player.name,
                 'card': player.card,
                 'lives': player.lives,
                 'outOfGame': player.outOfGame}
            jsonData = json.dumps(playerData)
            playersJson.append(jsonData)

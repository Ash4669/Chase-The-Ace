from action import Action
from player import Player
from card import Card
import argparse

def main():
    # getPlayersList
    playerNames = ["Yinka","Zac","Jozef","Tom","Louis"]
    playerList = list()
    for i in range(len(playerNames)):
        playerList.append(Player(playerNames[i]))
        playerList[i].dealer = False
        playerList[i].lives = 3
        playerList[i].outOfGame = False
    while playerList[0].lives + playerList[1].lives + playerList[2].lives + playerList[3].lives + playerList[4].lives > 1:

        Action.checkWinner(playerList)
        break

        noOneToTrade = False

        # setDealer
        playerList[len(playerList)-1].dealer = True
        Action.dealCards(playerList)

        for i in range(len(playerNames)):
            print("Name: " + str(playerList[i].name) + ", card: " + str(playerList[i].card) + ", lives: " + str(playerList[i].lives))
        print("")
        print(Card.outOfDeck)

        for i in range(len(playerNames)):
            if playerList[i].outOfGame == False:
                playerCurrent = playerList[i]
                if i < len(playerNames) - 1:
                    while i < len(playerNames) - 1 and playerList[i+1].outOfGame == True:
                        print("here")
                        if i == len(playerNames) - 2:
                            break
                        i = i + 1
                    if i == len(playerNames) - 2:
                        noOneToTrade = True
                    else:
                        playerLeft = playerList[i+1]

                    if noOneToTrade == False:
                        # getPlayerChoice
                        playerCurrent.choice = "trade"
                        if playerCurrent.dealer == False:
                            Action.tradeOrStick(playerCurrent,playerLeft)
                        elif playerCurrent.dealer == True:

                            # delete when getPlayerChoice written
                            playerCurrent.choice = "don't cut"
                            Action.cutTheDeck(playerCurrent)

        Action.endRound(playerList)

        for i in range(len(playerNames)):
            print("Name: " + str(playerList[i].name) + ", card: " + str(playerList[i].card) + ", lives: " + str(playerList[i].lives))
        print("")

        for player in playerList:
            if player.lives == 0:
                player.outOfGame = True

    # Action.announceWinner(playerList)

main();

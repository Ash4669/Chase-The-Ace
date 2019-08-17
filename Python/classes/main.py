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

    while playerList[0].lives>1 or playerList[1].lives>1 or playerList[2].lives>1 or playerList[3].lives>1 or playerList[4].lives>1: 

        # setDealer
        playerList[len(playerList)-1].dealer = True
        Action.dealCards(playerList)

        for i in range(len(playerNames)):
            print(playerList[i].name)
            print(playerList[i].card)
        print(Card.outOfDeck)

        for i in range(len(playerNames)):
            playerCurrent = playerList[i]
            if i<4:
                playerLeft = playerList[i+1]

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
            print(playerList[i].name)
            print(playerList[i].card)
            print(playerList[i].lives)

    Action.announceWinner(playerList)

main();

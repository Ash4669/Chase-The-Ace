from card import Card
from player import Player

class Action():

    def dealCards(players):
        for player in players:
            if player.outOfGame == False:
                currentCard = Card.getCard()
                while currentCard in Card.outOfDeck:
                    currentCard = Card.getCard()
                player.card = currentCard
                Card.inPlay(currentCard)
            else:
                player.card = ""

    def tradeOrStick(player1, player2):
        if player1.choice == "trade":
            if player2.card[1] != 13 and player1.card[1] != 13:
                card1 = player1.card
                card2 = player2.card
                player1.card = card2
                player2.card = card1
            else: print("Gotta King bitch!")
        elif player1.choice == "stick":
            pass
        else :
            print("Should have made a choice")

    def cutTheDeck(player):
        if player.dealer == True:
            if player.choice == "cut":
                cutCard = Card.getCard()
                while cutCard in Card.outOfDeck:
                    cutCard = Card.getCard()
                player.card = cutCard
                Card.inPlay(cutCard)
            elif player.choice == "don't cut":
                pass
            else :
                print("Should have made cut choice")
        else :
            print("Not dealer")

    def endRound(players):
        numbers = list()
        for player in players:
            if player.outOfGame == False:
                numbers.append(player.card[1])
        lowestCard = min(numbers)
        for player in players:
            if player.outOfGame == False:
                if player.card[1] == lowestCard:
                    Action.loseALife(player)
        Card.clearInPlay()

    def loseALife(player):
        player.lives = player.lives - 1

    def checkWinner(players):
        winnerArray = ["null"]*len(players)
        winnerMatrix = [winnerArray]*len(players)
        for i in range(len(players)):
            for j in range(len(players)):
                winnerMatrix[i][j] = 0
        print(winnerMatrix)
        for i in range(len(players)):
            print("here")
            winnerMatrix[i][i] = 1

    def announceWinner(players):
        for player in players:
            if player.lives > 0:
                print("Well done! " + player.name +  ", won!")

from card import Card
from player import Player

class Action():

    def dealCards(players):
        for i in range(len(players)):
            currentCard = Card.getCard()
            while currentCard in Card.outOfDeck:
                currentCard = Card.getCard()
            players[i].card = currentCard
            Card.inPlay(currentCard)

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
        for i in range(len(players)):
            numbers.append(Card.outOfDeck[i][1])
        lowestCard = min(numbers)
        for i in range(len(players)):
            if players[i].card[1] == lowestCard:
                Action.loseALife(players[i])
        Card.clearInPlay()

    def loseALife(player):
        player.lives = player.lives - 1

    def announceWinner(players):
        for player in players:
            if player.lives > 0:
                print("Well done! " + player.name +  ", won!")

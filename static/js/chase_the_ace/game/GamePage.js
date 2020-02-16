class GamePage extends Phaser.Scene {
    constructor() {
        super({ key: "GamePage" });
    }
    preload() {
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
        this.load.image("startButton","../../static/images/playbutton.png");
        this.load.image("tradeButton","../../static/images/playbutton.png");
        this.load.image("stickButton","../../static/images/optionsbutton.png");

        const suits = ["Clubs", "Spades", "Hearts", "Diamonds"];
        const numbers = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack", "Queen", "King"];

        for (var i = 0; i < suits.length; i++) {
            for (var j = 0; j < numbers.length; j++) {
                this.load.image(numbers[j] + suits[i], "../../static/images/cards/" + numbers[j] + suits[i] + ".png");
            }
        }
    }
    create() {

        // Lobbying
        const gamepage = this;
        var host = false;
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);

        backgroundImage.setDisplaySize(1000, 600);

        var playersNamesBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01);
        playersNamesBox.setStrokeStyle(2, 0x000000)

        this.add.text(820, 20, 'Players');


        self.socket = io();


        socket.on('connect', function() {
            socket.emit('join chase the ace');
        });

        console.log(host);

        socket.on('setHost', function() {
            host = true;
            displayStartButton(gamepage);
        });


        socket.on('joined chase the ace announcement', function(response) {
            console.log(response);
        })

        socket.on('update chase the ace playerList', function(response) {

            // Setting the player names equal to the server player names.
            playerNames = response

            // Reupdate the player names
            deletePlayerNames();
            writePlayerNames(gamepage);
        })

        socket.on('receive player id', function (response) {
            playerId = response
            console.log(playerId);
        })

        socket.on('update player data', function(playerJson) {
            for (var i = 0; i < playerNames.length; i++) {

                var playerData = JSON.parse(playerJson[i])

                if (playerData._id == playerId) {
                    playerCardValue = playerData._card;
                }

            }

            updateCards(gamepage);

        })

        socket.on('give player choice', function(currentPlayerId) {

            if (currentPlayerId == playerId) {
                playerStickButton = this.add.image(300, 400, "stickButton").setOrigin(0, 0);
                playerTradeButton = this.add.image(600, 400, "tradeButton").setOrigin(0, 0);

                playerStickButton.setInteractive().on('pointerdown', () => this.onStickButtonClicked());
                playerTradeButton.setInteractive().on('pointerdown', () => this.onTradeButtonClicked());

            }

        })
    }
}

window.onunload = quit;

function quit() {
    socket.emit('quit chase the ace');
};

var playerNames = new Array();
var playerNamesVariables = new Array();

var playerId = null;
var playerCardValue = null;
var playerCardDisplay = null;

var startButton;
var playerStickButton;
var playerTradeButton;


function writePlayerNames(game) {
    for (var i = 0; i < playerNames.length; i++) {
        playerNamesVariables[i] = game.add.text(820, 50 + (i * 40), playerNames[i]);
    }
}

function deletePlayerNames() {
    for (var i = 0; i < playerNamesVariables.length; i++) {
        playerNamesVariables[i].destroy();
    }
}

function updateCards(game) {
    try {
      playerCardDisplay.destroy();
    } catch (e) {
      console.log("card not set yet.");
    }
    console.log(playerCardValue);
    if (playerCardValue != null) {
        playerCardDisplay = game.add.image(300, 150, playerCardValue).setOrigin(0, 0).setDisplaySize(200, 320);
        // FIX CARD PIXELATION
    }
}

function displayStartButton(game) {
  startButton = game.add.image(300, 400, "startButton").setOrigin(0, 0);
  startButton.setDisplaySize(200, 100);
  startButton.setInteractive().on('pointerdown', () => this.onStartButtonClicked());
}

function onStartButtonClicked() {
    startButton.destroy();
    socket.emit('start game');
}

function onStickButtonClicked() {
    playerStickButton.destroy();
    socket.emit('stick card', playerId)
}

function onTradeButtonClicked() {
    playerTradeButton.destroy();
    socket.emit('trade card', playerId)
}

class GamePage extends Phaser.Scene {
    constructor() {
        super({ key: "GamePage" });
    }
    preload()
    {
        // Setting up suits and cards numbers to loop over for loading.
        const suits = ["Clubs", "Spades", "Hearts", "Diamonds"];
        const numbers = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack", "Queen", "King"];

        // Loading the game buttons, background and all of the cards.
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
        this.load.image("startButton","../../static/images/playbutton.png");
        this.load.image("stickButton","../../static/images/playbutton.png");
        this.load.image("tradeButton","../../static/images/optionsbutton.png");
        this.load.image("cutButton","../../static/images/optionsbutton.png");

        for (var i = 0; i < suits.length; i++)
        {
            for (var j = 0; j < numbers.length; j++)
            {
                this.load.image(numbers[j] + suits[i], "../../static/images/cards/" + numbers[j] + suits[i] + ".png");
            }
        }
    }
    create(){

        // Lobbying
        const gamepage = this;
        self.socket = io();
        var hostId = null;
        var dealerId = null;

        // Setting up the initial game screen: Background, players and player title.
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);
        backgroundImage.setDisplaySize(1000, 600);
        var playersNamesBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01);
        playersNamesBox.setStrokeStyle(2, 0x000000)
        this.add.text(820, 20, 'Players');

        socket.on('connect', function(){
            socket.emit('join chase the ace');
        });

        socket.on('setHost', function(hostId){
            this.hostId = hostId
            if (playerId == this.hostId)
            {
                displayStartButton(gamepage);
            }
        });

        socket.on('setDealer', function(dealerId){
            this.dealerId = dealerId;
        });

        socket.on('close game', function(data){
            window.location = data.url;
        });

        socket.on('receive player id', function (response){
            playerId = response
        })

        socket.on('joined chase the ace announcement', function(response){
            console.log(response);
            // need to have popup for a few seconds and destory it.
        })

        socket.on('update chase the ace playerList', function(response){
            // Setting the player names equal to the server player names.
            playerNames = response

            // Reupdate the player names
            deletePlayerNames();
            writePlayerNames(gamepage);
        })

        socket.on('update player data', function(playerJson)
        {
            for (var i = 0; i < playerNames.length; i++)
            {
                var playerData = JSON.parse(playerJson[i])
                if (playerData.id == playerId)
                {
                    playerCardValue = playerData.card;
                }
            }
            updateCards(gamepage);
        })

        socket.on('give player choice', function(currentPlayerId)
        {
            if (currentPlayerId == playerId)
            {
                if (currentPlayerId == this.dealerId)
                {
                    displayStickButton(gamepage);
                    displayCutButton(gamepage);
                }
                else
                {
                    displayStickButton(gamepage);
                    displayTradeButton(gamepage);
                }
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
var stickButton;
var tradeButton;
var cutButton;


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
        playerCardDisplay = game.add.image(340, 80, playerCardValue).setOrigin(0, 0).setDisplaySize(200, 320);
        // FIX CARD PIXELATION
    }
}

function displayStartButton(game) {
  startButton = game.add.image(340, 430, "startButton").setOrigin(0, 0);
  startButton.setDisplaySize(200, 100);
  startButton.setInteractive().on('pointerdown', () => this.onStartButtonClicked());
}

function displayStickButton(game) {
  stickButton = game.add.image(215, 430, "stickButton").setOrigin(0, 0);
  stickButton.setDisplaySize(200, 100);
  stickButton.setInteractive().on('pointerdown', () => this.onStickButtonClicked());
}

function displayTradeButton(game) {
  tradeButton = game.add.image(465, 430, "tradeButton").setOrigin(0, 0);
  tradeButton.setDisplaySize(200, 100);
  tradeButton.setInteractive().on('pointerdown', () => this.onTradeButtonClicked());
}

function displayCutButton(game) {
  cutButton = game.add.image(465, 430, "cutButton").setOrigin(0, 0);
  cutButton.setDisplaySize(200, 100);
  cutButton.setInteractive().on('pointerdown', () => this.onCutButtonClicked());
}

function onStartButtonClicked() {
    startButton.destroy();
    socket.emit('start game');
}

function onStickButtonClicked() {
    stickButton.destroy();
    tradeButton.destroy();
    socket.emit('stick card', playerId)
    if (playerId == dealerId) {
        //  Need something for ending the game for final stick or cut
    }
}

function onTradeButtonClicked() {
    stickButton.destroy();
    tradeButton.destroy();
    socket.emit('trade card', playerId)
}

function onCutButtonClicked() {
    stickButton.destroy();
    cutButton.destroy();
    socket.emit('cut card', playerId)
}

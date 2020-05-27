class GamePage extends Phaser.Scene {

    // Game Role Ids
    hostId;
    dealerId;
    playerId;

    // Player Names
    playerNames = new Array();
    playerNamesDisplays = new Array();

    // Player Lives
    maxPlayerLives = 3;
    playerLives;
    playerLivesDisplays = new Array();

    // Player Cards
    playerCardValue;
    playerCardDisplay;
    allPlayerCardDisplays = new Array();

    // Game Buttons
    startButton;
    stickButton;
    tradeButton;
    cutButton;

    // Phaser structure for constructor, preload and create methods.
    constructor()
    {
        super({ key: "GamePage" });
    }
    preload()
    {
        // Setting up suits and cards numbers to loop over for loading.
        const suits = ["Clubs", "Spades", "Hearts", "Diamonds"];
        const numbers = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10","jack", "queen", "king"];

        // Loading the game buttons, background and all of the cards.
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
        this.load.image("startButton","../../static/images/playbutton.png");
        this.load.image("stickButton","../../static/images/playbutton.png");
        this.load.image("tradeButton","../../static/images/optionsbutton.png");
        this.load.image("cutButton","../../static/images/cutButton.png");
        this.load.image("heart","../../static/images/heart.png");
        this.load.image("emptyHeart","../../static/images/heart-empty.png");

        for (var i = 0; i < suits.length; i++)
        {
            for (var j = 0; j < numbers.length; j++)
            {
                this.load.image(numbers[j] + suits[i], "../../static/images/cards/" + numbers[j] + suits[i] + ".png");
            }
        }
    }
    create()
    {
        // Storing GamePage this variable for methods to call to access class variables and methods.
        const gamePage = this;

        // Initialisation of socket variable into the global scope.
        self.socket = io();

        // Setting up the initial game screen: background, players and player title.
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0).setDisplaySize(1000, 600);
        var playersNamesBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01).setStrokeStyle(2, 0x000000)
        this.add.text(820, 20, 'Players');

        // Triggering server response to someone joining the game.
        socket.on('connect', function()
        {
            socket.emit('join chase the ace');
        });

        // Setting the host id for the client to display the start button.
        socket.on('setHost', function(hostId)
        {
            gamePage.hostId = hostId
            if (gamePage.playerId == gamePage.hostId)
            {
                gamePage.displayStartButton();
            }
        });

        // Setting the dealer of the round.
        socket.on('setDealer', function(response)
        {
            gamePage.dealerId = response;
        });

        // Closing the game
        socket.on('close game', function(data)
        {
            /* Create popup instead which then redirects after */
            window.location = data.url;
        });

        // Setting playerId for this client.
        socket.on('receive player id', function (response)
        {
            gamePage.playerId = response
        })

        // Letting other plays know when someone else has joined the game.
        socket.on('joined chase the ace announcement', function(response)
        {
            /* Need to have popup for a few seconds and destroy it. */
            console.log(response);
        })

        // Updating the player list of the game when people join or quit the game.
        socket.on('update chase the ace playerList', function(response)
        {
            // Setting the player names equal to the server player names.
            gamePage.playerNames = response

            // Re-update the player names
            gamePage.deletePlayerNames();
            gamePage.writePlayerNames();
        })

        // Updating the player's card and displaying it.
        socket.on('update player data', function(playerJson)
        {
            for (var i = 0; i < gamePage.playerNames.length; i++)
            {
                var playerData = JSON.parse(playerJson[i])
                if (playerData.id == gamePage.playerId)
                {
                    gamePage.playerCardValue = playerData.card;
                }
            }
            gamePage.updateCards();
        })

        // Updating the lives of the player and displaying them.
        socket.on('update player lives', function(playerJson)
        {
            for (var i = 0; i < gamePage.playerNames.length; i++)
            {
                var playerData = JSON.parse(playerJson[i])
                if (playerData.id == gamePage.playerId)
                {
                    gamePage.playerLives = playerData.lives;
                }
            }
            gamePage.updateLives();
        })

        // Displaying the correct game buttons for the player.
        socket.on('give player choice', function(currentPlayerId)
        {
            if (currentPlayerId == gamePage.playerId)
            {
                if (currentPlayerId == gamePage.dealerId)
                {
                    gamePage.displayStickButton();
                    gamePage.displayCutButton();
                }
                else
                {
                    gamePage.displayStickButton();
                    gamePage.displayTradeButton();
                }
            }
        })

        // Reveals all cards to everyone by the player names after the dealer's decision is made.
        socket.on('reveal cards and trigger results', function(playerData)
        {
            gamePage.displayAllPlayerCards(playerData)
        })

        // Deletes all the card displayed next to the player list after the round starts.
        socket.on('delete player cards', function()
        {
            gamePage.deleteAllPlayerCards();
        })

        // Displays start button for the dealer.
        socket.on('display new round button', function()
        {
            if (gamePage.playerId == gamePage.dealerId)
            {
                gamePage.displayStartButton();
            }
        })
    }

    displayStartButton()
    {
        this.startButton = this.add.image(340, 430, "startButton").setOrigin(0, 0);
        this.startButton.setDisplaySize(200, 100);
        this.startButton.setInteractive().on('pointerdown', () => this.onStartButtonClicked());
    }

    onStartButtonClicked()
    {
        this.startButton.destroy();
        socket.emit('delete all player cards')
        socket.emit('start game');
    }

    deletePlayerNames()
    {
        for (var i = 0; i < this.playerNamesDisplays.length; i++)
        {
            this.playerNamesDisplays[i].destroy();
        }
    }

    writePlayerNames()
    {
        for (var i = 0; i < this.playerNames.length; i++)
        {
            this.playerNamesDisplays[i] = this.add.text(820, 50 + (i * 40), this.playerNames[i]);
        }
    }

    updateCards()
    {
        try
        {
            this.playerCardDisplay.destroy();
        }
        catch (e)
        {
            console.log("card not set yet.");
        }
        if (this.playerCardValue != null)
        {
            // FIX CARD PIXELATION
            this.playerCardDisplay = this.add.image(340, 80, this.playerCardValue).setOrigin(0, 0).setDisplaySize(200, 320);
        }
    }

    updateLives(game)
    {
        try
        {
            for (var i = 0; i < this.maxPlayerLives; i++)
            {
                this.playerLivesDisplays[i].destroy();
            }
        }
        catch (e)
        {
          console.log("lives not set yet.");
        }
        for (var i = 0; i < this.maxPlayerLives; i++)
        {
            if (i < this.playerLives)
            {
                this.playerLivesDisplays[i] = this.add.image(40 + (i * 50), 40, 'heart').setDisplaySize(40, 40);
            }
            else
            {
                this.playerLivesDisplays[i] = this.add.image(40 + (i * 50), 40, 'emptyHeart').setDisplaySize(40, 40);
            }
        }
    }

    displayStickButton()
    {
        this.stickButton = this.add.image(215, 430, "stickButton").setOrigin(0, 0);
        this.stickButton.setDisplaySize(200, 100);
        this.stickButton.setInteractive().on('pointerdown', () => this.onStickButtonClicked());
    }

    displayTradeButton()
    {
        this.tradeButton = this.add.image(465, 430, "tradeButton").setOrigin(0, 0);
        this.tradeButton.setDisplaySize(200, 100);
        this.tradeButton.setInteractive().on('pointerdown', () => this.onTradeButtonClicked());
    }

    displayCutButton()
    {
        this.cutButton = this.add.image(465, 430, "cutButton").setOrigin(0, 0);
        this.cutButton.setDisplaySize(200, 100);
        this.cutButton.setInteractive().on('pointerdown', () => this.onCutButtonClicked());
    }

    onStickButtonClicked(game)
    {
        this.stickButton.destroy();
        if (this.playerId == this.dealerId)
        {
            this.cutButton.destroy();
        }
        else
        {
            this.tradeButton.destroy();
        }
        socket.emit('stick card')
    }

    onTradeButtonClicked()
    {
        this.stickButton.destroy();
        this.tradeButton.destroy();
        socket.emit('trade card')
    }

    onCutButtonClicked()
    {
        this.stickButton.destroy();
        this.cutButton.destroy();
        socket.emit('cut card')
    }

    displayAllPlayerCards(playerData)
    {
        if (this.playerCardValue != null)
        {
            for (var i = 0; i < this.playerNames.length; i++)
            {
                this.playerCard = JSON.parse(playerData[i]).card
                this.allPlayerCardDisplays[i] = this.add.image(800, 60 + (i * 40), this.playerCard).setDisplaySize(20, 32);
            }
        }
    }

    deleteAllPlayerCards()
    {
        try
        {
            for (var i = 0; i < this.playerNames.length; i++)
            {
                this.allPlayerCardDisplays[i].destroy();
            }
        }
        catch (e)
        {
          console.log("all player cards not set yet.");
        }
    }
}

window.onunload = quit;

function quit()
{
    socket.emit('quit chase the ace');
};

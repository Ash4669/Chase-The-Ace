class GamePage extends Phaser.Scene {

    roomNumber;
    gameStarted;
    hideDealerCard;
    dealerDisplay;

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
    revealedKingsDisplays = new Array();

    // Game Buttons
    startButton;
    stickButton;
    tradeButton;
    cutButton;
    revealKingButton;

    nextPlayerHasKingText;
    kingNotRevealed = true;

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
        this.load.image("revealKingButton","../../static/images/cutButton.png");
        this.load.image("heart","../../static/images/heart.png");
        this.load.image("emptyHeart","../../static/images/heart-empty.png");
        this.load.image("greenBack","../../static/images/cards/green_back.png");

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
        socket.on('set host', function(hostId, roomId)
        {
            gamePage.hostId = hostId
            if (gamePage.playerId == gamePage.hostId)
            {
                gamePage.gameStarted = false;
                gamePage.displayStartButton(gamePage);
                gamePage.roomNumber = gamePage.add.text(20, 70, "Room Number: " + roomId)
            }
        });

        // Setting the dealer of the round.
        socket.on('set dealer', function(response)
        {
            gamePage.dealerId = response;
        });

        // Deleting dealer display text
        socket.on('delete dealer title', function()
        {
            if (gamePage.playerId == gamePage.dealerId)
            {
                gamePage.dealerDisplay.destroy();
            }
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
            gamePage.playerId = response;
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
            gamePage.playerNames = response;

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
                    if (playerData.card != null)
                    {
                        if (playerData.card.includes('king') && gamePage.kingNotRevealed)
                        {
                            gamePage.displayRevealKingButton();
                        }
                    }
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
                    // When the dealer is given their choice, finally display their card.
                    gamePage.hideDealerCard = false;
                    gamePage.updateCards();
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
        socket.on('reveal all cards', function(playerData)
        {
            gamePage.displayAllPlayerCards(playerData)

            // Just on the edge case that a user swaps a king from the dealer.
            try
            {
                gamePage.onRevealKingButtonClicked()
            }
            catch(e)
            {
            }
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
                gamePage.displayStartButton(gamePage);
            }
        })

        // Displays winner text for the winning player.
        socket.on('trigger winner', function(winnerId)
        {
            for (var i = 0; i < gamePage.playerNames.length; i++)
            {
                if (gamePage.playerId == winnerId)
                {
                    gamePage.displayWin();
                }
            }
        })

        socket.on('next player has a king', function()
        {
            gamePage.displayNextPlayerHasKing()
        })

        socket.on('reveal king of playerId', function(playerData, playerId)
        {
            for (var i = 0; i < gamePage.playerNames.length; i++)
            {
                if (JSON.parse(playerData[i]).id == playerId)
                {
                    gamePage.playerCard = JSON.parse(playerData[i]).card
                    gamePage.revealedKingsDisplays.push(gamePage.add.image(800, 60 + (i * 40), gamePage.playerCard).setDisplaySize(20, 32));
                }
            }
        })

        socket.on('delete reveal button for player', function(currentPlayerId)
        {
            if (currentPlayerId == gamePage.playerId)
            {
                gamePage.onRevealKingButtonClicked();
            }
        })
    }

    displayStartButton(game)
    {
        this.startButton = this.add.image(340, 450, "startButton").setOrigin(0, 0);
        this.startButton.setDisplaySize(200, 100);
        this.startButton.setInteractive().on('pointerdown', () => this.onStartButtonClicked(game));
    }

    onStartButtonClicked(game)
    {
        this.startButton.destroy();
        socket.emit('delete all player cards');
        socket.emit('start game');
        if (this.gameStarted == false)
        {
            this.roomNumber.destroy();
            this.gameStarted = true;
        }
        // Hide the dealer's card and reset the king reveal.
        this.hideDealerCard = true;
        this.kingNotRevealed = true;
        if (this.playerId == this.dealerId)
        {
            this.dealerDisplay = game.add.text(350, 50, "You are the dealer!");
        }
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
            if (this.dealerId == this.playerId)
            {
                if (this.hideDealerCard == true)
                {
                    this.playerCardDisplay = this.add.image(340, 110, "greenBack").setOrigin(0, 0).setDisplaySize(200, 320);
                }
                else
                {
                    this.playerCardDisplay = this.add.image(340, 110, this.playerCardValue).setOrigin(0, 0).setDisplaySize(200, 320);
                }
            }
            else
            {
                this.playerCardDisplay = this.add.image(340, 110, this.playerCardValue).setOrigin(0, 0).setDisplaySize(200, 320);
            }
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
        this.stickButton = this.add.image(215, 450, "stickButton").setOrigin(0, 0);
        this.stickButton.setDisplaySize(200, 100);
        this.stickButton.setInteractive().on('pointerdown', () => this.onStickButtonClicked());
    }

    displayTradeButton()
    {
        this.tradeButton = this.add.image(465, 450, "tradeButton").setOrigin(0, 0);
        this.tradeButton.setDisplaySize(200, 100);
        this.tradeButton.setInteractive().on('pointerdown', () => this.onTradeButtonClicked());
    }

    displayCutButton()
    {
        this.cutButton = this.add.image(465, 450, "cutButton").setOrigin(0, 0);
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
        for (var i = 0; i < this.playerNames.length; i++)
        {
            // If a player is out of the game, don't display their card.
            if (JSON.parse(playerData[i]).outOfGame == false)
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
            for (var i = 0; i < this.allPlayerCardDisplays.length; i++)
            {
                this.allPlayerCardDisplays[i].destroy();
            }
        }
        catch (e)
        {
          console.log("all player cards not set yet.");
        }
        try
        {
            for (var i = 0; i < this.revealedKingsDisplays.length; i++)
            {
                this.revealedKingsDisplays[i].destroy();
            }
        }
        catch (e)
        {
          console.log("all player cards not set yet.");
        }
    }

    displayWin()
    {
        this.add.text(400, 80, 'Winner!')
    }

    displayNextPlayerHasKing()
    {
        this.nextPlayerHasKingText = this.add.text(360, 80, 'Other player has a king!');
        this.add.tween(
        {
            targets: this.nextPlayerHasKingText,
            ease: 'Sine.easeInOut',
            duration: 1000,
            delay: 1000,
            alpha: 0,
            onComplete: () =>
            {
                this.nextPlayerHasKingText.destroy();
            }
        });
    }

    displayRevealKingButton()
    {
        if (this.playerId != this.dealerId)
        {
            this.kingNotRevealed = false;
            this.revealKingButton = this.add.image(100, 250, "revealKingButton").setOrigin(0, 0);
            this.revealKingButton.setDisplaySize(200, 100);
            this.revealKingButton.setInteractive().on('pointerdown', () => this.onRevealKingButtonClicked());
        }

    }

    onRevealKingButtonClicked()
    {
        if (this.playerId != this.dealerId)
        {
            this.revealKingButton.destroy();
            socket.emit('reveal king')
        }
    }
}

window.onunload = quit;

function quit()
{
    socket.emit('quit chase the ace');
};

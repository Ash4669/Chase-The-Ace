class JoinPage extends Phaser.Scene {

    gameDoesNotExistText;
    gameAlreadyStartedText;

    constructor()
    {
        super({ key: "JoinPage" });
    }
    preload()
    {
        this.load.image("casinoRoom", "../../static/images/casinoRoom.jpg");
        this.load.image("backButton","../../static/images/playbutton.png");
        this.load.image("joinButton","../../static/images/optionsbutton.png");
    }
    create()
    {
        // Storing GamePage this variable for methods to call to access class variables and methods.
        const gamePage = this;

        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);
        backgroundImage.setDisplaySize(1000, 600);

        // Creating and attaching an input field onto the dom.
        var attributes = {"type":"text", "id":"join-input", "zIndex":"0", "style":"font-size:32px", "placeholder":"Enter Room Number Here"}
        var element = document.createElement("INPUT");
        for (var i = 0; i < Object.keys(attributes).length; i++)
        {
            element.setAttribute(Object.keys(attributes)[i], Object.values(attributes)[i])
        }
        document.getElementById("gameCanvas").appendChild(element);

        // Attaching dom element to phaser.
        var domElement = this.add.dom(500, 300, element);

        var backButton = this.add.image(250, 400, "backButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onBackButtonClicked());

        var joinButton = this.add.image(550, 400, "joinButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onJoinButtonClicked());

        // Triggering server response to someone joining the game.
        socket.on("game doesn't exist", function()
        {
            try
            {
                gamePage.gameDoesNotExistText.destroy();
            }
            catch (e)
            {} // Used for when the player repeatedly clicks the join button.

            gamePage.gameDoesNotExistText = gamePage.add.text(320, 230, 'Room does not exist!', {fontSize: '32px'});
            gamePage.add.tween(
            {
                targets: gamePage.gameDoesNotExistText,
                ease: 'Sine.easeInOut',
                duration: 1500,
                delay: 1000,
                alpha: 0,
            });
        });

        socket.on("game has already started", function()
        {
            try
            {
                gamePage.gameAlreadyStartedText.destroy();
            }
            catch (e)
            {} // Used for when the player repeatedly clicks the join button.

            gamePage.gameAlreadyStartedText = gamePage.add.text(220, 230, 'Game that has already started!', {fontSize: '32px'});
            gamePage.add.tween(
            {
                targets: gamePage.gameAlreadyStartedText,
                ease: 'Sine.easeInOut',
                duration: 1500,
                delay: 1000,
                alpha: 0,
            });
        });
    }

    onJoinButtonClicked()
    {
        let roomId = document.getElementById("join-input").value
        socket.emit('join game send', roomId);
    }
    onBackButtonClicked()
    {
        this.scene.start('StartPage')
    }
}


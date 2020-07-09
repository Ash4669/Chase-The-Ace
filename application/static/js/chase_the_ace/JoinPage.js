class JoinPage extends Phaser.Scene {

    gameDoesNotExistText;
    gameAlreadyStartedText;
    incorrectPasswordText;

    constructor()
    {
        super({ key: "JoinPage" });
    }
    preload()
    {
        this.load.image("backButton","../../static/images/playbutton.png");
        this.load.image("joinButton","../../static/images/optionsbutton.png");
    }
    create()
    {
        // Storing GamePage this variable for methods to call to access class variables and methods.
        const gamePage = this;

        var backgroundImage = this.add.image(0, 0, "casinoRoom")
        .setOrigin(0,0)
        .setDisplaySize(1000, 600);

        var backButton = this.add.image(250, 400, "backButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onBackButtonClicked());

        var joinButton = this.add.image(550, 400, "joinButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onJoinButtonClicked());

        // Creating and attaching an input field onto the dom.
        var roomNumberAttributes = {"type":"text", "id":"join-input", "zIndex":"0", "style":"font-size:32px", "placeholder":"Enter Room Number Here"}
        this.addInputElementToDom(roomNumberAttributes, 500, 250);

        var passwordAttributes = {"type":"text", "id":"password-input", "zIndex":"0", "style":"font-size:32px", "placeholder":"Enter Password (Optional)"}
        this.addInputElementToDom(passwordAttributes, 500, 325);

        // Triggering server response to someone joining the game.
        socket.on("game doesn't exist", function()
        {
            gamePage.addFadeAndDeleteText(gamePage.gameDoesNotExistText, 'Room does not exist!')
        });

        socket.on("game has already started", function()
        {
            gamePage.addFadeAndDeleteText(gamePage.gameAlreadyStartedText, 'That game has already started!')
        });

        socket.on('incorrect password', function()
        {
            gamePage.addFadeAndDeleteText(gamePage.incorrectPasswordText, 'Incorrect password for that game!')
        })
    }

    addInputElementToDom(attributes, x, y)
    {
        var element = document.createElement("INPUT");
        for (var i = 0; i < Object.keys(attributes).length; i++)
        {
            element.setAttribute(Object.keys(attributes)[i], Object.values(attributes)[i])
        }
        document.getElementById("gameCanvas").appendChild(element);

        // Attaching dom element to phaser.
        var domElement = this.add.dom(x, y, element);
    }

    addFadeAndDeleteText(element, text)
    {
        try
        {
            element.destroy();
        }
        catch (e)
        {} // Used for when the player repeatedly clicks the join button.

        element = this.add.text(220, 170, text, {fontSize: '32px'});
        this.add.tween(
        {
            targets: element,
            ease: 'Sine.easeInOut',
            duration: 1500,
            delay: 1000,
            alpha: 0,
        });
    }

    onJoinButtonClicked()
    {
        let roomId = document.getElementById("join-input").value
        let password = document.getElementById("password-input").value
        socket.emit('join game send', roomId, password);
    }

    onBackButtonClicked()
    {
        this.scene.start('StartPage')
    }
}


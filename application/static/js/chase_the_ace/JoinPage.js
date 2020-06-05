class JoinPage extends Phaser.Scene {
    constructor()
    {
        super({ key: "JoinPage" });
    }
    preload()
    {
        this.load.image("casinoRoom","../static/images/casinoRoom.jpg");
        this.load.image("joinButton","../static/images/playbutton.png");
    }
    create()
    {
        // Storing GamePage this variable for methods to call to access class variables and methods.
        const gamePage = this;

        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);
        backgroundImage.setDisplaySize(1000, 600);

        var element = document.createElement("INPUT");
        element.setAttribute("type", "text");
        element.setAttribute("id", "join-input");
        element.style.zIndex = "0";
        element.setAttribute("style", "font-size:32px;");
        element.setAttribute("placeholder", "Enter Room Number Here");
        document.getElementById("gameCanvas").appendChild(element);
        var domElement = this.add.dom(500, 300, element);

        var joinButton = this.add.image(400, 400, "joinButton").setOrigin(0, 0)
        joinButton.setDisplaySize(200, 100);;
        joinButton.setInteractive().on('pointerdown', () => this.onJoinButtonClicked());

        // Triggering server response to someone joining the game.
        socket.on("game doesn't exist", function()
        {
            console.log("doesn't exist")
        });

    }

    onJoinButtonClicked()
    {
        let roomId = document.getElementById("join-input").value
        socket.emit('join game send', roomId);
    }
}


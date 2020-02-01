class GamePage extends Phaser.Scene {
    constructor() {
        super({ key: "GamePage" });
    }
    preload() {
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
        this.load.image("startButton","../../static/images/playbutton.png");
    }
    create() {

        // Lobbying
        const gamepage = this;
        var host = false;
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);

        backgroundImage.setDisplaySize(1000, 600);

        var playersListBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01);
        playersListBox.setStrokeStyle(2, 0x000000)

        this.add.text(820, 20, 'Players');


        self.socket = io();


        socket.on('connect', function() {
            socket.emit('join chase the ace');
        });

        console.log(host);

        socket.on('setHost', function(){
            host = true;
            displayStartButton(gamepage);
        });


        socket.on('joined chase the ace announcement', function(response) {
            console.log(response);
        })

        socket.on('update chase the ace playerList', function(response) {

            // Setting the playerlist equal to the server player list.
            playerList = response

            // Reupdate the playerList
            deletePlayerNames();
            writePlayerNames(gamepage);
        })
    }
}

window.onunload = quit;

function quit() {
    socket.emit('quit chase the ace');
};

var playerList = new Array();
var playerListText = new Array();

function writePlayerNames(self) {
    for (var i = 0; i < playerList.length; i++) {
        playerListText[i] = self.add.text(820, 50 + (i * 40), playerList[i]);
    }
}

function deletePlayerNames(){
    for (var i = 0; i < playerListText.length; i++) {
        playerListText[i].destroy();
    }
}

var startButton;

function displayStartButton(game) {
  startButton = game.add.image(300, 400, "startButton").setOrigin(0, 0);
  startButton.setDisplaySize(200, 100);
  startButton.setInteractive().on('pointerdown', () => this.onStartButtonClicked());
}

function onStartButtonClicked(game) {
    startButton.destroy();
    socket.emit('start game');
}

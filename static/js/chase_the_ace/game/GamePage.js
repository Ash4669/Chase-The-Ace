class GamePage extends Phaser.Scene {
    constructor() {
        super({ key: "GamePage" });
    }
    preload() {
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
    }
    create() {

      const gamepage = this
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);

        backgroundImage.setDisplaySize(1000, 600);

        var playersListBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01);
        playersListBox.setStrokeStyle(2, 0x000000)

        this.add.text(820, 20, 'Players');


        self.socket = io();

        socket.on('connect', function() {
            self.socket.emit('join chase the ace');
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

    update() {
    }

}

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


window.onunload = quit;

function quit() {
    socket.emit('quit chase the ace');
};

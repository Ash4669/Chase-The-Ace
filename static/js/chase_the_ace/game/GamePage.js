class GamePage extends Phaser.Scene {
    constructor() {
        super({ key: "GamePage" });
    }
    preload() {
        this.load.image("casinoRoom", "../../static/images/greentable1.jpg");
    }
    create() {
        var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);

        backgroundImage.setDisplaySize(1000, 600);

        var playersListBox = this.add.rectangle(900, 0, 200, 500, 0x01DF01);
        playersListBox.setStrokeStyle(2, 0x000000)

        this.add.text(820, 20, 'Players');
    }

    update() {
      this.writePlayerNames()
    }

    playerListText = []

    writePlayerNames() {
        for (var i = 0; i < playerList.length; i++) {
            this.add.text(820, 50 + (i * 40), playerList[i]);
        }
    }

    deletePlayerName() {

    }
}




var playerList = new Array();

socket.on('connect', function() {
    socket.emit('join chase the ace');
});

socket.on('disconnect', function() {
    socket.emit('quit chase the ace');
})

socket.on('joined chase the ace announcement', function(response) {
    console.log(response);
})

socket.on('update chase the ace playerList', function(response) {
    console.log('here2');
    playerList = response
    GamePage.writePlayerNames();
})

// socket.on('getting playerList', function(response) {
//     playerList = response;
// })
//
// socket.on('remove player', function(response) {
//     var index  = playerList.indexOf(response);
//     if (index > -1) {
//       playerList.splice(index, 1);
//     }
// })
// Make a emit that triggers what would have triggered for a normal connect functions. Manually trigger it and get it to send the player data to all players and update their game.

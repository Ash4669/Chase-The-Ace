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
      for (var i = 0; i < players.length; i++) {
        this.add.text(820, 50 + (i * 40), players[i]);
      }
    }

}

var players = new Array();

socket.on('connect', function() {
    socket.emit('join');
});

socket.on('joined', function(response) {
  players.push()
  console.log(response);
})
// Make a emit that triggers what would have triggered for a normal connect functions. Manually trigger it and get it to send the player data to all players and update their game.

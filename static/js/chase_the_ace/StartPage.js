
var socket = io();

class StartPage extends Phaser.Scene {
    constructor() {
        super({ key: "StartPage" });
    }
    preload() {
      this.load.image("casinoRoom", "../../static/images/casinoRoom.jpg");
      this.load.image("hostButton","../../static/images/playbutton.png");
      this.load.image("joinButton","../../static/images/optionsbutton.png");
    }
    create() {
      var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);
      var hostButton = this.add.image(300, 400, "hostButton").setOrigin(0, 0);
      var joinButton = this.add.image(600, 400, "joinButton").setOrigin(0, 0);

      backgroundImage.setDisplaySize(1000, 600);
      hostButton.setDisplaySize(200, 100);
      joinButton.setDisplaySize(200, 100);

      hostButton.setInteractive().on('pointerdown', () => this.onHostButtonClicked());
      joinButton.setInteractive().on('pointerdown', () => this.onJoinButtonClicked());
    }

    onHostButtonClicked() {
      socket.emit('host game send');
    }

    onJoinButtonClicked() {
      this.scene.start("JoinPage")
    }
}
socket.on('redirect', function (data) {
  console.log('here');
  window.location = data.url;
});

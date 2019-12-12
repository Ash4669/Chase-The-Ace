class JoinPage extends Phaser.Scene {
    constructor() {
        super({ key: "JoinPage" });
    }
    preload() {
      this.load.image("casinoRoom","../static/images/casinoRoom.jpg");
    }
    create() {
      var backgroundImage = this.add.image(0, 0, "casinoRoom").setOrigin(0,0);

      backgroundImage.setDisplaySize(1000, 600);
    }
}

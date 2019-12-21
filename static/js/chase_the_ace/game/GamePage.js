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

    }

}

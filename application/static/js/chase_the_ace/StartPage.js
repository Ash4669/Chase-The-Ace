class StartPage extends Phaser.Scene {
    constructor()
    {
        super({ key: "StartPage" });
    }
    preload()
    {
        this.load.image("casinoRoom", "../../static/images/casinoRoom.jpg");
        this.load.image("hostButton","../../static/images/playbutton.png");
        this.load.image("joinButton","../../static/images/optionsbutton.png");
    }
    create()
    {
        var backgroundImage = this.add.image(0, 0, "casinoRoom")
        .setOrigin(0,0)
        .setDisplaySize(1000, 600)

        var hostButton = this.add.image(250, 400, "hostButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onHostButtonClicked());

        var joinButton = this.add.image(550, 400, "joinButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onJoinButtonClicked());
    }

    onHostButtonClicked()
    {
        this.scene.start("HostPage")
    }

    onJoinButtonClicked()
    {
        this.scene.start("JoinPage");
    }
}

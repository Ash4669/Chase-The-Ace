var config = {
    type: Phaser.WEBGL,
    parent: 'gameCanvas',
    width: 1000,
    height: 600,
    backgroundColor: "#6495ed",
    audio: {
        disableWebAudio: true
    },
    physics: {
        default: "arcade",
        arcade: {
            gravity: { x: 0, y: 0 }
        }
    },
    scene: [
        StartPage
    ],
    pixelArt: true,
    roundPixels: true
};
var game = new Phaser.Game(config);

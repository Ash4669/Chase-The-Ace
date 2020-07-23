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
    dom: {
        createContainer: true
    },
    scene: [
        StartPage,
        HostPage,
        JoinPage
    ],
    pixelArt: true,
    roundPixels: true
};
var game = new Phaser.Game(config);

// Initialising socket variable for all js on page.
self.socket = io();

socket.on('redirect', function (data)
{
    window.location = data.url;
});

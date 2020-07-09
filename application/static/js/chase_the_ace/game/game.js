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
        GamePage
    ],
    pixelArt: true,
    roundPixels: true
};
var game = new Phaser.Game(config);

// Initialisation of socket variable into the global scope.
self.socket = io();

socket.on('redirect', function (data)
{
window.location = data.url;
});
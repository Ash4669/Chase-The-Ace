class HostPage extends Phaser.Scene {

    gameDoesNotExistText;
    gameAlreadyStartedText;
    passwordInput;
    livesInput;

    constructor()
    {
        super({ key: "HostPage" });
    }
    preload()
    {
        this.load.image("hostButton","../../static/images/playbutton.png");
        this.load.image("backButton","../../static/images/optionsbutton.png");
    }
    create()
    {
        var backgroundImage = this.add.image(0, 0, "casinoRoom")
        .setOrigin(0,0)
        .setDisplaySize(1000, 600);

        var backButton = this.add.image(250, 400, "backButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onBackButtonClicked());

        var hostButton = this.add.image(550, 400, "hostButton")
        .setOrigin(0, 0)
        .setDisplaySize(200, 100)
        .setInteractive().on('pointerdown', () => this.onHostButtonClicked());

        // Creating and attaching an input field onto the dom.
        var inputAttributes = {"type":"text", "id":"password-input", "zIndex":"0", "size":"27", "style":"font-size:32px",
         "placeholder":"Set Room Password (optional)", "maxlength":"40"};
        this.passwordInput = this.addInputElementToDom(inputAttributes);
        this.add.dom(game.canvas.width/2, game.canvas.height/2 - 50, this.passwordInput).setOrigin(0, 0);

        var dropDownAttributes = {"id":"lives-input", "style":"font-size:20px"};
        var options = ["1","2","3","4","5","6","7","8","9","10"];
        this.livesInput = this.addDropDownElementToDom(dropDownAttributes, options);
        this.add.dom(game.canvas.width/2, game.canvas.height/2 + 50, this.livesInput)
        .setOrigin(0, 0);

        var livesText = this.add.text(360, 313, "lives:", {fontSize: '32px'})
        .setOrigin(0, 0);
    }

    addInputElementToDom(attributes)
    {
        var element = document.createElement("input");
        for (var i = 0; i < Object.keys(attributes).length; i++)
        {
            element.setAttribute(Object.keys(attributes)[i], Object.values(attributes)[i]);
        }
        document.getElementById("gameCanvas").appendChild(element);
        return element
    }

    addDropDownElementToDom(attributes, optionValues)
    {
        var dropDown = document.createElement("select");
        this.attachAttributesToElement(dropDown, attributes)
        for (var i = 0; i < 10; i++)
        {
            var option = document.createElement("option");
            option.value = optionValues[i];
            option.selected = "";
            option.innerHTML = optionValues[i];
            dropDown.appendChild(option);
        }
        document.getElementById("gameCanvas").appendChild(dropDown);
        return dropDown
    }

    attachAttributesToElement(element, attributes)
    {
        for (var i = 0; i < Object.keys(attributes).length; i++)
        {
            element.setAttribute(Object.keys(attributes)[i], Object.values(attributes)[i]);
        }
    }

    onHostButtonClicked()
    {
        let password = document.getElementById("password-input").value;
        let livesElement = document.getElementById("lives-input");
        let lives = livesElement.options[livesElement.selectedIndex].value;
        socket.emit('host game send', password, lives);
    }

    onBackButtonClicked()
    {
        this.scene.start('StartPage')
    }
}

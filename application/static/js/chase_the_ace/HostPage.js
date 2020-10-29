class HostPage extends Phaser.Scene {

    gameDoesNotExistText;
    gameAlreadyStartedText;
    nameInput;
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
        // Storing GamePage this variable for methods to call to access class variables and methods.
        const gamePage = this;

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
        var nameInputAttributes = {"type":"text", "id":"name-input", "zIndex":"0", "size":"27", "style":"font-size:32px",
         "placeholder":"Enter name", "value":window.name, "maxlength":"40"};
        this.nameInput = this.addInputElementToDom(nameInputAttributes);
        this.add.dom(500, 172, this.nameInput);

        var passwordInputAttributes = {"type":"text", "id":"password-input", "zIndex":"0", "size":"27", "style":"font-size:32px",
         "placeholder":"Set Room Password (optional)", "maxlength":"40"};
        this.passwordInput = this.addInputElementToDom(passwordInputAttributes);
        this.add.dom(500, 250, this.passwordInput);

        var dropDownAttributes = {"id":"lives-input", "style":"font-size:20px"};
        var options = ["1","2","3","4","5","6","7","8","9","10"];
        this.livesInput = this.addDropDownElementToDom(dropDownAttributes, options);
        this.add.dom(540, 328, this.livesInput);

        var livesText = this.add.text(360, 313, "lives:", {fontSize: '32px'});

        socket.on("no name entered", function()
        {
            gamePage.addFadeAndDeleteText(gamePage.gameDoesNotExistText, 'No player name entered!')
        });
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

    addFadeAndDeleteText(element, text)
    {
        try
        {
            element.destroy();
        }
        catch (e)
        {} // Used for when the player repeatedly clicks the join button.

        element = this.add.text(280, 100, text, {fontSize: '32px'});
        this.add.tween(
        {
            targets: element,
            ease: 'Sine.easeInOut',
            duration: 1500,
            delay: 1000,
            alpha: 0,
        });
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
        let name = document.getElementById("name-input").value;
        let password = document.getElementById("password-input").value;
        let livesElement = document.getElementById("lives-input");
        let lives = livesElement.options[livesElement.selectedIndex].value;
        socket.emit('host game send', name, password, lives);
    }

    onBackButtonClicked()
    {
        this.scene.start('StartPage')
    }
}

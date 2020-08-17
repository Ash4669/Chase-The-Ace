var scrolled = false;
var messageSent = true;
document.getElementById("chatCentre").addEventListener("scroll", function()
{
    scrolled = true;
    var element = document.getElementById("chatCentre");
    if (element.scrollTop + element.clientHeight == element.scrollHeight)
    {
        scrolled = false;
    }
})

// Letting other plays know when someone else has joined the game.
socket.on('joined chase the ace announcement', function(announcement)
{
    attachMessage("chatCentre", announcement);
})

socket.on("append on chat", function(playerName, message)
{
    attachMessage("chatCentre", playerName + ": " + message)
})

function sendMessage()
{
    let element = document.getElementById("chatMessage");
    let message = element.value;
    socket.emit("send chat message", message);
    element.value='';
    messageSent = true;
}

function attachMessage(elementId, message)
{
    element = document.getElementById(elementId);
    let div = document.createElement("div")
    div.innerHTML = message;
    div.setAttribute("class", "chatMessage")
    element.appendChild(div);
    updateScroll(elementId);
}

function updateScroll(elementId){
    if(!scrolled || messageSent)
    {
        var element = document.getElementById(elementId);
        element.scrollTop = element.scrollHeight;
        messageSent = false;
    }
}

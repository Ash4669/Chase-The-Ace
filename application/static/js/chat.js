// Letting other plays know when someone else has joined the game.
socket.on('joined chase the ace announcement', function(announcement)
{
    let chatContainer = document.getElementById("chatContainer");
    attachMessage(chatContainer, announcement);
})

socket.on("append on chat", function(playerName, message)
{
    let chatContainer = document.getElementById("chatContainer");
    attachMessage(chatContainer, playerName + ": " + message)
})

function sendMessage()
{
    let element = document.getElementById("chatMessage");
    let message = element.value;
    socket.emit("send chat message", message);
    element.value='';
    return false;
}

function attachMessage(chatContainer, message)
{
    let div = document.createElement("div")
    div.innerHTML = message;
    div.setAttribute("class", "chatMessage")
    chatContainer.appendChild(div);
}

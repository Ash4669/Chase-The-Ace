from flask import session
from .. import socketio, send, emit

@socketio.on("send chat message")
def manageMessage(chatMessage):
    roomId = session.get("roomId")
    playerName = session.get("userFullName")
    emit("append on chat", (playerName, chatMessage), room=roomId)

> To do

- Use Ionic framework to get the game onto mobile for the app store.
- create a chat feature with pusher to allow players to talk to each other
- Set up email confirmation later on.
- Add matchmaking system where it can get a game_id that is created but game not ready yet and people can join (do public and private games) (Public games are without signing in. Private is with signing in.) Add in private tickbox to not allow others to join.
- Need database markers to say if game is public or private and locked or not.

- SignalR for game chat?


> Switching to python 3/ Setup

- pip3 install virtualenv
- If wanted, set up virtual environment with "python3 -m virtualenv path_to_environment".
- Activate environment with "source path_to_environment/bin/activate" on mac or "path_to_environment\Scripts\activate" for windows.
- pip3 install flask, flask_login, flask-sqlalchemy, configparser and pusher using "pip3 install 'module_name'".
- use "export FLASK_APP=project_folder_name" for mac, "set FLASK_APP=project_folder_name" for command line or "$env:FLASK_APP='foo'" for powershell. I believe this is correct.
- Create the database using the following python code in the python REPL.
```
>>> from app.py import db
>>> db.create_all()
```
Note: might need to comment out chase the ace imports in the blueprints in app.py. This requires running __main__ variable and it can't be imported. Easier to comment out for creation.

- install windows visual studio and C++ build tools inside it.
(Windows Python needs Visual C++ libraries installed via the SDK to build code, such as via setuptools.extension.Extension or numpy.distutils.core.Extension. On Linux and Mac, the C++ libraries are installed with the compiler.)
- install pytest to run unit tests.

> Notes about SocketIO

https://socket.io/docs/emit-cheatsheet/
https://socket.io/get-started/chat
- For server side javascript:
- io.on(connection(socket.emit)) - self
- io.on(connection(socket.broadcast.emit)) - all but self
- io.on(conection(io.emit)) - all including self

- User flask's request.sid to get session id and target individual clients.
https://flask-socketio.readthedocs.io/en/latest/ - use Rooms section to group together for games. Send and Emit functions also accept room argument to broadcast to just that room. Using room = sid when passing the room argument can emit something to a specific client.

Add client sid to store in rooms to then loop over for the game. io.to(room/socketId).emit(). The actual game mechanics can just send with sid that are stored within the room. use socket.emit within connection to send to specific clients and use broadcasts when sending the information to everyone to update. Need to map out types of connections that need to happen when.
- for Flask, use emit but set room=sid_id. get sessionid with request.sid.

- Note for disconnecting: Have it where the pop up appears before they leave the page and then record the page url. If they click leave the page, it triggers them leaving the room or just have the pop up as something to stall while the url is recorded and then on disconnect, they can remove themselves, update the others in the room and then leave the room.

> Notes for self
- Use Page Objects method of testing. Not UI JourneySteps. Read into it.


> Game Notes

When first person joins, set as host in db.
When someone joins they are given a player id which is stored in the db.
When host clicks start, set the room current player
When game starts, lock down joining.
When someone quits, they are deleted from the database
When host quits, boot everyone
When person wins, if signed in, add one to their count with their userId.

> Functionality left to implement

- Cut for the dealer
- Saying you're the dealer when you are.
- passing over to the next dealer and deleting last one.
- Checking who the winner is per round and taking off a life.
- Displaying of lives.
- Selection for how many lives you want
- Displaying whos go it is on player list.
- Awarding score for winner if they are signed in.
- Displaying a next round screen and a count down.
- Add rotating effect on card and display back of card, at 90 degrees, delete and create actual card and rotate rest of 180. Also add a sound effect in when the card reaches 90 degrees.

> To do

- Use Ionic framework to get the game onto mobile for the app store.
- create authentication page
- create database to use and look into how to connect that when hosting OR look at using a file which can be treated like a database. (will upload and run from the python imports so it is simpler.)
- create a chat feature with pusher to allow players to talk to each other
- do full database and have them sign in and store their wins at different games.
- Change sign up to redirect to profile and sign them in. - at least for the moment. Set up email confirmation later on.
- add matchmaking system where it can get a game_id that is created but game not ready yet and people can join (do public and private games) (Public games are without signing in. Private is with signing in.)
- Creating variable pages for game id use url_for('method_name', variable=foo) for url and call method def method_name(variable)
- yield code in multiple places from the base page or the game pages.


- SignalR for game chat?

- NAME ALL IMAGES BY THE NAME THEY WILL USE IN THE END SO THE IMAGE JUST NEEDS SWITCHING OUT, NOT THE CODE AS WELL.


- USE JSON TO KEEP THE GAME STATE AND HAVE THE CLIENTS POLL FOR A CHANGE IN THE GAME (UP IN VERSION?) AND THE MAKE A GET FOR THE INFORMATION AND UPDATE THEIR PERSON GAME STATE.
 - Regarding polling, simplest way is a while loop that polls, checks for change, renders change, and keeps going. Either throw the whole client logic in a while(true), or break out of it when it's your turn, take your go, and go back into the loop when you've taken your turn

 - make the HTTP request to the site end point and handle that in the controller. Set up the controller for that game to handle everything. Each controller should be spanned off its own game id.

> Switching to python 3/ Setup

- pip3 install virtualenv
- If wanted, set up virtual environment with "python3 -m virtualenv path_to_environment".
- Activate environment with "source path_to_environment/bin/activate" on mac or "path_to_environment\Scripts\activate" for windows.
- pip3 install flask, flask_login, flask-sqlalchemy, configparser and pusher using "pip3 install 'module_name'".
- use "export FLASK_APP=project_folder_name" for mac, "set FLASK_APP=project_folder_name" for command line or "$env:FLASK_APP='foo'" for powershell. I believe this is correct.

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

Add client sid to store in rooms to then loop over for the game. io.to(room/socketId).emit(). The actual game mechanics can just send with sid that are stored within the room. use socket.emit within connection to send to specific clients and use broadcasts when sending the information to everyone to update. Need to map out types fo connections that need to happen when.
- for Flask, use emit but set room=sid_id. get sessionid with request.sid.

- Note for disconnecting: Have it where the pop up appears before they leave the page and then record the page url. If they click leave the page, it triggers them leaving the room or just have the pop up as something to stall while the url is recorded and then on disconnect, they can remove themselves, update the others in the room and then leave the room.

> Notes for self

- Use Page Objects method of testing. Not UI JourneySteps. Read into it.

> To do
- Use Ionic framework to get the game onto mobile for the app store.
- SignalR for game chat?
- Set up email confirmation later on.
- Add matchmaking system where it can get a game_id that is created but game not ready yet and people can join (do public and private games) (Public games are without signing in. Private is with signing in.) Add in private tickbox to not allow others to join.

> Switching to python 3/ Setup

- pip3 install virtualenv
- If wanted, set up virtual environment with "python3 -m virtualenv path_to_environment".
- Activate environment with "source path_to_environment/bin/activate" on mac or "path_to_environment\Scripts\activate" for windows.
- pip3 install flask, flask_login, flask-sqlalchemy, configparser and pusher using "pip3 install 'module_name'".
- use "export FLASK_APP=project_folder_name" for mac, "set FLASK_APP=project_folder_name" for command line or "$env:FLASK_APP='foo'" for powershell. I believe this is correct.
- Create the database using the following python code in the python REPL.
- Install pytest to run unit tests.
```
>>> from application import db, create_app
>>> db.create_all(app=create_app())
```
> For windows computers
- install windows visual studio and C++ build tools inside it.
(Windows Python needs Visual C++ libraries installed via the SDK to build code, such as via setuptools.extension.Extension or numpy.distutils.core.Extension. On Linux and Mac, the C++ libraries are installed with the compiler.)

> Notes about SocketIO
- https://socket.io/docs/emit-cheatsheet/
- https://socket.io/get-started/chat
- For server side javascript:
- io.on(connection(socket.emit)) - self
- io.on(connection(socket.broadcast.emit)) - all but self
- io.on(connection(io.emit)) - all including self

> Notes for self
- Use Page Objects method of testing. Not UI JourneySteps. Read into it.


> Functionality left to implement
>> High priority
- Saying you're the dealer when you are.
- Refactor the host page to go to a separate scene and have both a choice of lives and password to set and if left black then leave unset. 
- Selection for how many lives you want.
- Add passcode for joining games

>> Medium Priority
- Display the dealer for all people to see on the right?
- Displaying who's go it is on player list. (display 'Playing' when their go is triggered. After clicking something, the text is deleted.)
- Once a king is flipped, the previous person doesn't have the trade option anymore. 
- Have it so if a player is not authenticated (not logged in and so missing a name), they have a text box pop up where they enter their name, store it in the session and on clicking confirmation for name, send redirect from there. Use this for both start and joining a game. If they do have a name, give them the option but autofill it with their name stored in the session. Should be easy enough to implement. Send it in the socket. 
- Add rotating effect on card and display back of card, at 90 degrees, delete and create actual card and rotate rest of 180. Also add a sound effect in when the card reaches 90 degrees.

>> Lower Priority
- When the host quits a game, have a popup and on clicking 'ok' then redirect.
- When a host quits the game (happens eventually), delete the room record out of the room db.
- Add message and redirect for those trying to join a game that doesn't exist from the URL.
- Add gameType to Player model and adjust getPlayerList and relevant methods. Needed for adding shed game. 
- Maybe change display to have it across the top.
- Give options to choose the card they want to cut to? A button from 1 to 52 - len(players) for them to choose their card? Think of ways to do this. May just be creating 52 - players of card displays on the screen and they choose one, it then finds which one of the array it was, gets the array number and send that to the serve and they get the relevant card.
Or add a randomiser before pulling off the card. (Not difficult to display 52 cards and then the ith one they choose is the value sent back to the database and pop off that value.)


> Testing notes
- Look at setting the card object in the card class. Add a set method but don't use it in the main code. Just have the setting for instigating very specific scenarios.

> Bugs
- Clear at the moment.
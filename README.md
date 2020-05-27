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


> Game Notes

When first person joins, set as host in db.
When someone joins they are given a player id which is stored in the db.
When host clicks start, set the room current player
When game starts, lock down joining.
When someone quits, they are deleted from the database
When host quits, boot everyone
When person wins, if signed in, add one to their count with their userId.

> Functionality left to implement
- Winning scenario
- Cannot swap a king.
- Dealer shouldn't see their card.
- Can swap a king if it's the dealers card because they haven't see it.
  So if not equal to dealer then don't swap and give a message back, or don't give option.
  Check next card in deck and if king then skip options and update current player.
- Add gameType to Player model and adjust getPlayerList and relevant methods. Needed for adding shed game. 

- Awarding score for winner if they are signed in.
- Saying you're the dealer when you are.
- Selection for how many lives you want
- Displaying whos go it is on player list.
- Maybe change display to have it across the top and display the current player for all players to see.
- Display start new round button and dealer icon above name which moves after finishing the previous round.
- Add rotating effect on card and display back of card, at 90 degrees, delete and create actual card and rotate rest of 180. Also add a sound effect in when the card reaches 90 degrees.
- Give options to choose the card they want to cut to? A button from 1 to 52 - len(players) for them to choose their card? Think of ways to do this. May just be creating 52 - players of card displays on the screen and they choose one, it then finds which one of the array it was, gets the array number and send that to the serve and they get the relevant card.
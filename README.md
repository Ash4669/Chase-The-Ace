# To do
- Use Ionic framework to get the game onto mobile for the app store.
- Set up email confirmation later on.
- Add matchmaking system where it can get a game_id that is created but game not ready yet and people can join (do public and private games) (Public games are without signing in. Private is with signing in.) Add in private tickbox to not allow others to join.

# Switching to python 3/ Setup

- pip3 install virtualenv
- If wanted, set up virtual environment with "python3 -m virtualenv path_to_environment".
- Activate environment with "source path_to_environment/bin/activate" on mac or "path_to_environment\Scripts\activate" for windows.
- pip3 install flask, flask_login, flask-sqlalchemy, configparser and flask_session, using "pip3 install 'module_name'".
- use "export FLASK_APP=project_folder_name" for mac, "set FLASK_APP=project_folder_name" for command line or "$env:FLASK_APP='foo'" for powershell. I believe this is correct.
- Create the database using the following python code in the python REPL.
- Install pytest to run unit tests.
```
>>> from application import db, create_app
>>> db.create_all(app=create_app())
```
# For windows computers
- install windows visual studio and C++ build tools inside it.
(Windows Python needs Visual C++ libraries installed via the SDK to build code, such as via setuptools.extension.Extension or numpy.distutils.core.Extension. On Linux and Mac, the C++ libraries are installed with the compiler.)

# Notes about SocketIO
- https://socket.io/docs/emit-cheatsheet/
- https://socket.io/get-started/chat
- For server side javascript:
- io.on(connection(socket.emit)) - self
- io.on(connection(socket.broadcast.emit)) - all but self
- io.on(connection(io.emit)) - all including self

# Notes for self
- Use Page Objects method of testing. Not UI JourneySteps. Read into it.
- Unit test the site.


# Functionality left to implement

## Website whole functionality
- Change login over to auth0 as it is safer.
- Sort out CSS styling for the site
  - Home
  - Login and sign up page
  - Profile page
  - Games page
  - Chat

## Game specific functionality
#### Chase the ace
### High Priority
- When they aren't signed in, they can still add a name and play, just add if logged in then +1 to score but otherwise ignore.
- Need on page checks for sign up and log in.
- Need way of having dealer tell players they are cutting
- Need displays for everyone's lives. Maybe a number and a heart by their name.

### Medium Priority
- Display to host that they are the host.
- Display the dealer for all people to see on the right?
- Displaying who's go it is on player list. (display 'Playing' when their go is triggered. After clicking something, the text is deleted.)
- Once a king is flipped, the previous person doesn't have the trade option anymore. 
- Have it so if a player is not authenticated (not logged in and so missing a name), they have a text box pop up where they enter their name, store it in the session and on clicking confirmation for name, send redirect from there. Use this for both start and joining a game. If they do have a name, give them the option but autofill it with their name stored in the session. Should be easy enough to implement. Send it in the socket. 
- Add rotating effect on card and display back of card, at 90 degrees, delete and create actual card and rotate rest of 180. Also add a sound effect in when the card reaches 90 degrees.
- Give players ability to start a new game in the same lobby.

### Lower Priority
- Add message and redirect for those trying to join a game that doesn't exist from the URL. - use alert.
- Add gameType to Player model and adjust getPlayerList and relevant methods. Needed for adding shed game. 
- Maybe change display to have it across the top.

# Testing notes
- Look at setting the card object in the card class. Add a set method but don't use it in the main code. Just have the setting for instigating very specific scenarios.

# Bugs
- Firefox doesn't support the beforeunload event listener and so preventDefault() is used in the function instead to force it to use the eventListener and trigger the unload and emit. However, they does cause them to confirm their leave which is deemed acceptable, but if they navigate anywhere via the url, the event does not get triggered and the game breaks before the client isn't deleted from the game. Also, if the user tries to leaves and chooses not to then it causes the player to delete but remain on the page. Fix is unknown at this point.
- Need to look at error handling. Happens when trying to retrieve db records that are already deleted. App doesn't suffer though.
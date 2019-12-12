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

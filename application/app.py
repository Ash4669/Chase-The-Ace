#!/usr/bin/python3
# maybe delete above line
# app.py

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import configparser
from flask_socketio import SocketIO, emit, send, join_room, leave_room


config = configparser.ConfigParser()
config.read("../settings.conf")

app = Flask(__name__)

# Ignores slashes on the end of URLs.
app.url_map.strict_slashes = False

app.config['SECRET_KEY'] = config.get('SQLALCHEMY','secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY','sqlalchemy_database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init SQLAlchemy so we can use it later
db = SQLAlchemy(app)

socketio = SocketIO()

socketio.init_app(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))



# blueprint for auth routes in our app
from controllers.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from controllers.main import main as main_blueprint
app.register_blueprint(main_blueprint)

# blueprint for chase_the_ace parts of app
from controllers.games.chase_the_ace import chase_the_ace as chase_the_ace_blueprint
app.register_blueprint(chase_the_ace_blueprint)

# blueprint for shed parts of app
from controllers.games.shed import shed as shed_blueprint
app.register_blueprint(shed_blueprint)


# Game sockets import game mechanics and socketio listeners.
from controllers.games import chase_the_ace_gameplay

@socketio.on('connect')
def handle_my_connect_event():
    print('connected')

@socketio.on('disconnect')
def handle_my_disconnect_event():
    print('disconnected')

# If running app.py, then run app itself.
if __name__ == '__main__':
    socketio.run(app)

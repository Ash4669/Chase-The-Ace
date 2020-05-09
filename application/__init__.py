#!/usr/bin/python3

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import configparser
from flask_socketio import SocketIO, emit, send, join_room, leave_room

config = configparser.ConfigParser()
config.read("settings.conf")

# init SQLAlchemy so we can use it later
db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

from . import models

# Game sockets import game mechanics and socketio listeners.
from .controllers.games import chase_the_ace_gameplay


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.get('SQLALCHEMY','secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY','sqlalchemy_database_uri')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    db.init_app(app)
    socketio.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # If running app.py, then run app itself.
    if __name__ == '__main__':
        socketio.run(app)

    registerBlueprints(app)

    return app


def registerBlueprints(app):
    # blueprint for auth routes in our app
    from .controllers.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .controllers.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for chase_the_ace parts of app
    from .controllers.games.chase_the_ace import chase_the_ace as chase_the_ace_blueprint
    app.register_blueprint(chase_the_ace_blueprint)

    # blueprint for shed parts of app
    from .controllers.games.shed import shed as shed_blueprint
    app.register_blueprint(shed_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@socketio.on('connect')
def handle_my_connect_event():
    print('connected')

@socketio.on('disconnect')
def handle_my_disconnect_event():
    print('disconnected')
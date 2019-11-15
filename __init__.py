#!/usr/bin/python3
# maybe delete above line
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pusher import pusher
import configparser

# init SQLAlchemy so we can use it later

db = SQLAlchemy()

pusher = pusher_client = pusher.Pusher(
  app_id  = config.get('PUSHERDETAILS','app_id'),
  key     = config.get('PUSHERDETAILS','key'),
  secret  = config.get('PUSHERDETAILS','secret'),
  cluster = config.get('PUSHERDETAILS','cluster'),
  ssl     = bool(config.get('PUSHERDETAILS','ssl'))
)

def create_app():

    config = configparser.ConfigParser()
    config.read("settings.conf")

    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbs/db.sqlite' # change after I have it working and inputting data
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .controllers.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    return app

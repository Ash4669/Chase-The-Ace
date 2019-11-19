#!/usr/bin/python3
# maybe delete above line
# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import configparser

# init SQLAlchemy so we can use it later

db = SQLAlchemy()

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = config.get('SQLALCHEMY','secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY','sqlalchemy_database_uri')
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

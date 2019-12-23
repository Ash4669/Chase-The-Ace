# chase_the_ace.py

from flask import Blueprint, render_template, redirect, url_for, session
import configparser
from controllers.auth import auth as auth_blueprint
from flask_login import current_user

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():
    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<gameId>')
def chase_the_ace_instance(gameId):
    playerData = {"playerName": session.get('playerName')}
    return render_template('games/chase_the_ace/game.html', gameId = gameId, data = playerData)

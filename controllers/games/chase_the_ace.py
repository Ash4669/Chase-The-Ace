# chase_the_ace.py

from flask import Blueprint, render_template, redirect, url_for
import configparser
from controllers.auth import auth as auth_blueprint

config = configparser.ConfigParser()
config.read("card_games_website/settings.conf")

chase_the_ace = Blueprint('chase_the_ace',__name__)

@chase_the_ace.route('/play/chase_the_ace')
def chase_the_ace_index():
    return render_template('games/chase_the_ace/index.html')

@chase_the_ace.route('/play/chase_the_ace/<game_id>')
def chase_the_ace_instance(game_id):
    return render_template('games/chase_the_ace/game.html', game_id = game_id)
